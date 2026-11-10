"""
Unit tests of the griffe extension showing the values of the constants used as default values.

.. versionadded:: 0.1.0
"""

import griffe
from default_values import DefaultValues, find_constant_value, is_python_literal, resolve_default_values

PACKAGE_NAME = "sales"
FUNCTION_CODE = "LIMIT = 10\ndef cut(limit: int = LIMIT, other: int = 3) -> int:\n    return limit"
FIELD_CODE = "SEPARATOR = ';'\nclass Options:\n    separator: str = SEPARATOR"
CALL_CODE = "SHAPE = make_shape()\ndef fill(shape: object = SHAPE) -> None:\n    pass"
CONSTANT_CALL_CODE = "COUNT = 10\nclass Chart:\n    bins: object = Bins(COUNT)\n    other: object = Bins(3)"
CONSTANT_CALL_PARAMETER_CODE = "COUNT = 10\ndef draw(bins: object = Bins(COUNT)) -> None:\n    pass"
EXPECTED_CALL = "Bins(10)"
EXPECTED_PLAIN_CALL = "Bins(3)"
EXPECTED_LIMIT = "10"
EXPECTED_OTHER = "3"
EXPECTED_SEPARATOR = "';'"
EXPECTED_SHAPE_NAME = "SHAPE"
LITERAL_SOURCES = ["','", "10", "None", "(2, 3)"]
EXPRESSION_SOURCES = ["Shape([2, 3])", "make_shape()", "values"]
UNKNOWN_NAME = "MISSING"
IMPORT_CODE = "from os import sep\nLIMIT = 10\ndef cut(limit: int = LIMIT) -> int:\n    return limit"
CLASS_DEFAULT_CODE = "class Options:\n    pass\ndef read(options: object = Options) -> None:\n    pass"
EXPECTED_CLASS_NAME = "Options"


def load_package(code: str) -> tuple[griffe.Module, griffe.GriffeLoader]:
	"""
	Return a package holding some code, and a loader that knows it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	code
		The code of the ``__init__.py`` of the package.

	Returns
	-------
	tuple[griffe.Module, griffe.GriffeLoader]
		The package and its loader.
	"""
	loader = griffe.GriffeLoader()
	with griffe.temporary_visited_package(PACKAGE_NAME, {"__init__.py": code}) as package:
		loader.modules_collection.set_member(package.path, package)

	return package, loader


def test_resolve_default_values_replaces_a_constant_default_with_its_value() -> None:
	"""
	Check that LIMIT becomes 10 and a literal default is kept.

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package(FUNCTION_CODE)

	resolve_default_values(package, loader)

	function = package["cut"]
	limit_default = function.parameters["limit"].default
	other_default = function.parameters["other"].default
	limit_text = str(limit_default)
	other_text = str(other_default)
	assert limit_text == EXPECTED_LIMIT
	assert other_text == EXPECTED_OTHER


def test_resolve_default_values_replaces_a_constant_field_value() -> None:
	"""
	Check that a class field naming a constant takes the value of the constant.

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package(FIELD_CODE)

	resolve_default_values(package, loader)

	separator = package["Options.separator"]
	assert separator.value == EXPECTED_SEPARATOR


def test_resolve_default_values_keeps_a_constant_that_is_not_a_literal() -> None:
	"""
	Check that a constant built by a call keeps its name.

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package(CALL_CODE)

	resolve_default_values(package, loader)

	function = package["fill"]
	shape_default = function.parameters["shape"].default
	shape_text = str(shape_default)
	assert shape_text == EXPECTED_SHAPE_NAME


def test_find_constant_value_ignores_an_unknown_name() -> None:
	"""
	Check that a name griffe cannot find gives None.

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package(FUNCTION_CODE)
	unknown_name = griffe.ExprName(UNKNOWN_NAME, parent=package)

	constant_value = find_constant_value(unknown_name, loader)

	assert constant_value is None


def test_is_python_literal_tells_literals_from_expressions() -> None:
	"""
	Check texts, numbers, None and tuples against calls and names.

	.. versionadded:: 0.1.0
	"""
	literal_answers = [is_python_literal(source) for source in LITERAL_SOURCES]
	expression_answers = [is_python_literal(source) for source in EXPRESSION_SOURCES]

	assert all(literal_answers)
	assert not any(expression_answers)


def test_default_values_resolve_the_whole_package() -> None:
	"""
	Check that the extension resolves the defaults of a loaded package.

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package(FUNCTION_CODE)
	extension = DefaultValues()

	extension.on_package(pkg=package, loader=loader)

	function = package["cut"]
	limit_default = function.parameters["limit"].default
	limit_text = str(limit_default)
	assert limit_text == EXPECTED_LIMIT


def test_resolve_default_values_replaces_a_constant_given_to_a_call() -> None:
	"""
	Check that a field holding a call shows the value of the constant given to it.

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package(CONSTANT_CALL_CODE)

	resolve_default_values(package, loader)

	assert str(package["Chart.bins"].value) == EXPECTED_CALL


def test_resolve_default_values_keeps_a_call_without_constant() -> None:
	"""
	Check that a call whose arguments are literals is unchanged.

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package(CONSTANT_CALL_CODE)

	resolve_default_values(package, loader)

	assert str(package["Chart.other"].value) == EXPECTED_PLAIN_CALL


def test_resolve_default_values_replaces_a_constant_in_the_call_of_a_parameter() -> None:
	"""
	Check that a parameter holding a call shows the value of the constant given to it.

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package(CONSTANT_CALL_PARAMETER_CODE)

	resolve_default_values(package, loader)

	assert str(package["draw"].parameters["bins"].default) == EXPECTED_CALL


def test_resolve_default_values_skips_the_imported_names() -> None:
	"""
	Check that a package importing a name still resolves its own constants.

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package(IMPORT_CODE)

	resolve_default_values(package, loader)

	limit_default = package["cut"].parameters["limit"].default
	limit_text = str(limit_default)
	assert limit_text == EXPECTED_LIMIT


def test_resolve_default_values_keeps_a_default_naming_a_class() -> None:
	"""
	Check that a default naming a class, not a constant, keeps its name.

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package(CLASS_DEFAULT_CODE)

	resolve_default_values(package, loader)

	options_default = package["read"].parameters["options"].default
	options_text = str(options_default)
	assert options_text == EXPECTED_CLASS_NAME
