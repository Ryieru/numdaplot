"""
Functional tests checking that every optional parameter of the public API describes its default.

A parameter with a value as default says ``... by default``, and a parameter defaulting to None says what happens
``when omitted``.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass
from pathlib import Path

import griffe
import pytest

SOURCE_FOLDER = Path(__file__).parent.parent.parent / "src"
PACKAGE_NAME = "numdaplot"
NONE_DEFAULT = "None"
VALUE_WORDING = "by default"
NONE_WORDING = "when omitted"
PARAMETERS_KIND = griffe.DocstringSectionKind.parameters
VARIADIC_KINDS = {griffe.ParameterKind.var_positional, griffe.ParameterKind.var_keyword}
SKIPPED_NAMES = {"self", "cls"}
CASE_ID = "{path}.{name}"
VALUE_CASE_DESCRIPTION = "The number of rows, 5 by default."
NONE_CASE_DESCRIPTION = "The seed, other rows at each call when omitted."
SILENT_DESCRIPTION = "The number of rows."


@dataclass(frozen=True)
class OptionalParameter:
	"""
	A parameter of the public API with a default, and its description.

	.. versionadded:: 0.1.0

	Parameters
	----------
	case_id
		The path of its owner and its name, such as ``numdaplot.tables.preview.preview.Preview.count``.
	default
		The default as written in the code, such as ``5`` or ``None``.
	description
		The description of the parameter, on one line.
	"""

	case_id: str
	default: str
	description: str


def read_descriptions(docstring: griffe.Docstring | None) -> dict[str, str]:
	"""
	Return the description of each parameter of a docstring, on one line.

	.. versionadded:: 0.1.0

	Parameters
	----------
	docstring
		The docstring, or None.

	Returns
	-------
	dict[str, str]
		The descriptions by parameter name.
	"""
	descriptions = dict[str, str]()
	if docstring is None:
		return descriptions

	for section in docstring.parse(griffe.Parser.numpy):
		if section.kind != PARAMETERS_KIND:
			continue

		for parameter in section.value:
			words = parameter.description.split()
			descriptions[parameter.name] = " ".join(words)

	return descriptions


def list_function_parameters(function: griffe.Function, descriptions: dict[str, str]) -> list[OptionalParameter]:
	"""
	Return the parameters of a function that have a default.

	.. versionadded:: 0.1.0

	Parameters
	----------
	function
		The function or method.
	descriptions
		The descriptions to use, from the function or from its class.

	Returns
	-------
	list[OptionalParameter]
		The optional parameters, variadic ones excluded.
	"""
	parameters = list[OptionalParameter]()

	for parameter in function.parameters:
		is_skipped = parameter.name in SKIPPED_NAMES or parameter.kind in VARIADIC_KINDS
		if is_skipped or parameter.default is None:
			continue

		case_id = CASE_ID.format(path=function.path, name=parameter.name)
		description = descriptions.get(parameter.name, "")
		default = str(parameter.default)
		optional_parameter = OptionalParameter(case_id, default, description)
		parameters.append(optional_parameter)

	return parameters


def list_class_parameters(public_class: griffe.Class) -> list[OptionalParameter]:
	"""
	Return the optional parameters of a class: its constructor and its public methods, inherited ones included.

	griffe builds the constructor of a dataclass from its fields.

	.. versionadded:: 0.1.0

	Parameters
	----------
	public_class
		The class.

	Returns
	-------
	list[OptionalParameter]
		The optional parameters.
	"""
	parameters = list[OptionalParameter]()
	class_descriptions = read_descriptions(public_class.docstring)
	constructor = public_class.all_members.get("__init__")
	if isinstance(constructor, griffe.Function):
		constructor_descriptions = read_descriptions(constructor.docstring)
		merged_descriptions = class_descriptions | constructor_descriptions
		constructor_parameters = list_function_parameters(constructor, merged_descriptions)
		parameters.extend(constructor_parameters)

	for member in public_class.all_members.values():
		if member.name.startswith("_"):
			continue

		method = member
		if isinstance(member, griffe.Alias):
			method = member.final_target

		if not isinstance(method, griffe.Function):
			continue

		method_descriptions = read_descriptions(method.docstring)
		method_parameters = list_function_parameters(method, method_descriptions)
		parameters.extend(method_parameters)

	return parameters


def list_public_parameters() -> list[OptionalParameter]:
	"""
	Return every optional parameter of the objects numdaplot exports.

	.. versionadded:: 0.1.0

	Returns
	-------
	list[OptionalParameter]
		The optional parameters, each owner once.
	"""
	package = griffe.load(PACKAGE_NAME, search_paths=[SOURCE_FOLDER])
	parameters = dict[str, OptionalParameter]()

	for member in package.members.values():
		if member.name.startswith("_") or not isinstance(member, griffe.Alias):
			continue

		target = member.final_target
		if isinstance(target, griffe.Class):
			found_parameters = list_class_parameters(target)
		elif isinstance(target, griffe.Function):
			target_descriptions = read_descriptions(target.docstring)
			found_parameters = list_function_parameters(target, target_descriptions)
		else:
			found_parameters = list[OptionalParameter]()

		for parameter in found_parameters:
			parameters[parameter.case_id] = parameter

	public_parameters = list(parameters.values())

	return public_parameters


def describes_its_default(default: str, description: str) -> bool:
	"""
	Return whether a description gives the default with the wording of its kind.

	.. versionadded:: 0.1.0

	Parameters
	----------
	default
		The default as written in the code.
	description
		The description of the parameter.

	Returns
	-------
	bool
		True when a None default says ``when omitted``, or another default says ``by default``.
	"""
	lowered_description = description.lower()
	if default == NONE_DEFAULT:
		has_wording = NONE_WORDING in lowered_description
		return has_wording

	has_wording = VALUE_WORDING in lowered_description

	return has_wording


PUBLIC_PARAMETERS = list_public_parameters()
PARAMETER_IDS = [parameter.case_id for parameter in PUBLIC_PARAMETERS]


@pytest.mark.parametrize("parameter", PUBLIC_PARAMETERS, ids=PARAMETER_IDS)
def test_optional_parameter_describes_its_default(parameter: OptionalParameter) -> None:
	"""
	Check the wording of the default of one optional parameter of the public API.

	.. versionadded:: 0.1.0

	Parameters
	----------
	parameter
		The optional parameter.
	"""
	is_described = describes_its_default(parameter.default, parameter.description)

	assert is_described, parameter.description


def test_public_parameters_are_found() -> None:
	"""
	Check that the search finds optional parameters, such as the count of Preview.

	.. versionadded:: 0.1.0
	"""
	preview_count_ids = [case_id for case_id in PARAMETER_IDS if case_id.endswith("Preview.__init__.count")]

	assert preview_count_ids != []


@pytest.mark.parametrize(
	("default", "description", "expected"),
	[
		("5", VALUE_CASE_DESCRIPTION, True),
		("None", NONE_CASE_DESCRIPTION, True),
		("5", SILENT_DESCRIPTION, False),
		("None", VALUE_CASE_DESCRIPTION, False),
	],
)
def test_describes_its_default_matches_the_wording_to_the_default(
	default: str, description: str, expected: bool
) -> None:
	"""
	Check the accepted and rejected wordings.

	.. versionadded:: 0.1.0

	Parameters
	----------
	default
		The default as written in the code.
	description
		The description.
	expected
		Whether the description is accepted.
	"""
	is_described = describes_its_default(default, description)

	assert is_described == expected
