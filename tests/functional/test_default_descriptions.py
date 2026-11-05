"""
Functional tests checking that a parameter whose default value is a constant gives this value in its description.

Editors show the name of the constant in the signature, so the description is where a reader finds its value.

.. versionadded:: 0.1.0
"""

import ast
import importlib
import inspect
import re
from dataclasses import dataclass
from pathlib import Path

import pytest

SOURCE_FOLDER = Path(__file__).parent.parent.parent / "src" / "numdaplot"
PACKAGE_NAME = "numdaplot"
MODULE_SUFFIX = ".py"
CONSTANT_NAME = re.compile(r"[A-Z][A-Z0-9_]{2,}")
DEFAULT_SENTENCE = r"{value}`*(?: \w+)? by default"
CASE_ID = "{file_name}:{owner_name}.{parameter_name}"
CLEANED_INDENTATION = " "
EXPECTED_CASE_ID = "preview.py:Preview.count"
TRUE_DESCRIPTION = "The number of rows, 5 by default."
WRONG_DESCRIPTION = "The number of rows, 6 by default."
SILENT_DESCRIPTION = "The number of rows."
UNIT_DESCRIPTION = "The width, 6.4 inches by default."
QUOTED_DESCRIPTION = 'The character, ``","`` by default.'
BARE_DESCRIPTION = "The character, ``,`` by default."
COUNT_VALUE = "5"
WIDTH_VALUE = "6.4"
SEPARATOR_VALUE = '","'
DOCSTRING = "Summary.\n\nParameters\n----------\ncount\n\tThe number,\n\t5 by default.\nside\n\tThe side.\n"
EXPECTED_DESCRIPTION = "The number, 5 by default."


@dataclass(frozen=True)
class ConstantDefault:
	"""
	A parameter whose default value names a constant.

	.. versionadded:: 0.1.0

	Parameters
	----------
	case_id
		The name of the case, such as ``preview.py:Preview.count``.
	parameter_name
		The name of the parameter.
	default_text
		The default value with the value of its constant, such as ``BinCount(10)``.
	docstring
		The docstring describing the parameter.
	"""

	case_id: str
	parameter_name: str
	default_text: str
	docstring: str


def write_value(value: object) -> str:
	"""
	Return a value as a description writes it, a text between double quotes.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The value of a constant.

	Returns
	-------
	str
		The written value.
	"""
	if isinstance(value, str):
		return f'"{value}"'

	return str(value)


def write_default(default: ast.expr, module_values: dict[str, object]) -> str | None:
	"""
	Return a default value with the value of the constant it names, if it names one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	default
		The default value in the source.
	module_values
		The values of the module defining it, by name.

	Returns
	-------
	str or None
		The default value as written in a description, ``None`` when it names no constant.
	"""
	names = [node.id for node in ast.walk(default) if isinstance(node, ast.Name)]
	constant_names = [name for name in names if CONSTANT_NAME.fullmatch(name) and name in module_values]
	if not constant_names:
		return None

	default_text = ast.unparse(default)

	for name in constant_names:
		written_value = write_value(module_values[name])
		default_text = default_text.replace(name, written_value)

	return default_text


def find_class_defaults(node: ast.ClassDef, file_name: str, module_values: dict[str, object]) -> list[ConstantDefault]:
	"""
	Return the fields of a class whose default value names a constant.

	.. versionadded:: 0.1.0

	Parameters
	----------
	node
		The class in the source.
	file_name
		The name of its file.
	module_values
		The values of its module, by name.

	Returns
	-------
	list[ConstantDefault]
		The fields found.
	"""
	defaults = list[ConstantDefault]()
	docstring = ast.get_docstring(node) or ""

	for statement in node.body:
		if not isinstance(statement, ast.AnnAssign) or statement.value is None:
			continue

		default_text = write_default(statement.value, module_values)
		if default_text is None or not isinstance(statement.target, ast.Name):
			continue

		parameter_name = statement.target.id
		case_id = CASE_ID.format(file_name=file_name, owner_name=node.name, parameter_name=parameter_name)
		defaults.append(ConstantDefault(case_id, parameter_name, default_text, docstring))

	return defaults


def find_function_defaults(
	node: ast.FunctionDef, file_name: str, module_values: dict[str, object]
) -> list[ConstantDefault]:
	"""
	Return the parameters of a function whose default value names a constant.

	.. versionadded:: 0.1.0

	Parameters
	----------
	node
		The function in the source.
	file_name
		The name of its file.
	module_values
		The values of its module, by name.

	Returns
	-------
	list[ConstantDefault]
		The parameters found.
	"""
	defaults = list[ConstantDefault]()
	docstring = ast.get_docstring(node) or ""
	positional_count = len(node.args.defaults)
	positional_parameters = node.args.args[-positional_count:] if positional_count else []
	positional_pairs = list(zip(positional_parameters, node.args.defaults, strict=True))
	keyword_pairs = list(zip(node.args.kwonlyargs, node.args.kw_defaults, strict=True))

	for parameter, default in positional_pairs + keyword_pairs:
		default_text = None if default is None else write_default(default, module_values)
		if default_text is None:
			continue

		case_id = CASE_ID.format(file_name=file_name, owner_name=node.name, parameter_name=parameter.arg)
		defaults.append(ConstantDefault(case_id, parameter.arg, default_text, docstring))

	return defaults


def find_file_defaults(path: Path) -> list[ConstantDefault]:
	"""
	Return the fields and parameters of a source file whose default value names a constant.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		A source file of the package.

	Returns
	-------
	list[ConstantDefault]
		The fields and parameters found.
	"""
	relative_path = path.relative_to(SOURCE_FOLDER).with_suffix("")
	module_name = ".".join((PACKAGE_NAME, *relative_path.parts))
	module = importlib.import_module(module_name.removesuffix(".__init__"))
	module_values = vars(module)
	source = path.read_text()
	tree = ast.parse(source)
	defaults = list[ConstantDefault]()

	for node in ast.walk(tree):
		if isinstance(node, ast.ClassDef):
			class_defaults = find_class_defaults(node, path.name, module_values)
			defaults.extend(class_defaults)

		if isinstance(node, ast.FunctionDef):
			function_defaults = find_function_defaults(node, path.name, module_values)
			defaults.extend(function_defaults)

	return defaults


def find_all_defaults() -> list[ConstantDefault]:
	"""
	Return the fields and parameters of the whole package whose default value names a constant.

	.. versionadded:: 0.1.0

	Returns
	-------
	list[ConstantDefault]
		The fields and parameters, in the order of the files.
	"""
	defaults = list[ConstantDefault]()
	source_paths = sorted(SOURCE_FOLDER.rglob("*" + MODULE_SUFFIX))

	for source_path in source_paths:
		file_defaults = find_file_defaults(source_path)
		defaults.extend(file_defaults)

	return defaults


def read_parameter_description(docstring: str, parameter_name: str) -> str:
	"""
	Return the description of a parameter in a NumPy docstring, on one line.

	.. versionadded:: 0.1.0

	Parameters
	----------
	docstring
		The docstring.
	parameter_name
		The name of the parameter.

	Returns
	-------
	str
		The description, empty when the parameter is not described.
	"""
	cleaned_docstring = inspect.cleandoc(docstring)
	lines = cleaned_docstring.splitlines()
	if parameter_name not in lines:
		return ""

	description_lines = list[str]()
	first_position = lines.index(parameter_name) + 1

	for line in lines[first_position:]:
		stripped_line = line.strip()
		is_indented = line.startswith(CLEANED_INDENTATION)
		if not is_indented:
			break

		description_lines.append(stripped_line)

	description = " ".join(description_lines)

	return description


def gives_default(description: str, default_text: str) -> bool:
	"""
	Return whether a description says that a value is the default one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	description
		The description of a parameter.
	default_text
		The default value as a description writes it.

	Returns
	-------
	bool
		True when the description holds the value followed by ``by default``, a unit being allowed between them.
	"""
	escaped_value = re.escape(default_text)
	default_sentence = DEFAULT_SENTENCE.format(value=escaped_value)
	sentence_match = re.search(default_sentence, description)
	has_default = sentence_match is not None

	return has_default


CONSTANT_DEFAULTS = find_all_defaults()
CASE_IDS = [constant_default.case_id for constant_default in CONSTANT_DEFAULTS]


def test_constant_defaults_are_found() -> None:
	"""
	Check that the search finds the default values naming a constant, Preview.count among them.

	.. versionadded:: 0.1.0
	"""
	assert EXPECTED_CASE_ID in CASE_IDS


@pytest.mark.parametrize("constant_default", CONSTANT_DEFAULTS, ids=CASE_IDS)
def test_description_gives_the_value_of_the_constant(constant_default: ConstantDefault) -> None:
	"""
	Check that the description of the parameter gives the current value of its constant.

	.. versionadded:: 0.1.0
	"""
	description = read_parameter_description(constant_default.docstring, constant_default.parameter_name)

	has_default = gives_default(description, constant_default.default_text)

	assert has_default, f"{constant_default.default_text} is missing from: {description}"


def test_gives_default_accepts_the_true_value() -> None:
	"""
	Check a description with the value of the constant.

	.. versionadded:: 0.1.0
	"""
	has_default = gives_default(TRUE_DESCRIPTION, COUNT_VALUE)

	assert has_default


def test_gives_default_refuses_another_value() -> None:
	"""
	Check a description that still gives an old value.

	.. versionadded:: 0.1.0
	"""
	has_default = gives_default(WRONG_DESCRIPTION, COUNT_VALUE)

	assert not has_default


def test_gives_default_refuses_a_description_without_value() -> None:
	"""
	Check a description that gives no default value.

	.. versionadded:: 0.1.0
	"""
	has_default = gives_default(SILENT_DESCRIPTION, COUNT_VALUE)

	assert not has_default


def test_gives_default_accepts_a_unit_after_the_value() -> None:
	"""
	Check a value followed by its unit.

	.. versionadded:: 0.1.0
	"""
	has_default = gives_default(UNIT_DESCRIPTION, WIDTH_VALUE)

	assert has_default


def test_gives_default_accepts_a_text_between_quotes() -> None:
	"""
	Check a text written as code and between quotes.

	.. versionadded:: 0.1.0
	"""
	has_default = gives_default(QUOTED_DESCRIPTION, SEPARATOR_VALUE)

	assert has_default


def test_gives_default_refuses_a_text_without_quotes() -> None:
	"""
	Check that a text must be written between quotes.

	.. versionadded:: 0.1.0
	"""
	has_default = gives_default(BARE_DESCRIPTION, SEPARATOR_VALUE)

	assert not has_default


def test_read_parameter_description_joins_its_lines_and_stops_at_the_next_parameter() -> None:
	"""
	Check a description written on two lines, followed by another parameter.

	.. versionadded:: 0.1.0
	"""
	description = read_parameter_description(DOCSTRING, "count")

	assert description == EXPECTED_DESCRIPTION
