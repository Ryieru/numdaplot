"""
Unit tests of the aliases naming the values that the public parameters accept.

.. versionadded:: 0.1.0
"""

import griffe
from value_types import VALUE_TYPE_PATHS, build_value_types_page, find_value_type_paths, link_type_parameters

PACKAGE_NAME = "sales"
PACKAGE_FILES = {
	"__init__.py": "from sales.between import Between\n",
	"values.py": "type OrderedValue = int | str\n",
	"between.py": (
		"from dataclasses import dataclass\n"
		"@dataclass(frozen=True)\n"
		"class Between[OrderedValue: (int, str)]:\n"
		"    low: OrderedValue\n"
		"    bounds: list[OrderedValue]\n"
		"    name: str\n"
	),
}
BETWEEN_PATH = "between.Between"
ALIAS_PATHS = {"OrderedValue": "sales.values.OrderedValue"}
ALIAS_PATH = "sales.values.OrderedValue"
EXPECTED_VALUE_TYPE_COUNT = 6


def load_package() -> tuple[griffe.Module, griffe.GriffeLoader]:
	"""
	Return a small package with a value type and a class whose type parameter has its name, and its loader.

	.. versionadded:: 0.1.0

	Returns
	-------
	tuple[griffe.Module, griffe.GriffeLoader]
		The package and its loader.
	"""
	loader = griffe.GriffeLoader()
	with griffe.temporary_visited_package(PACKAGE_NAME, PACKAGE_FILES) as package:
		loader.modules_collection.set_member(package.path, package)

	return package, loader


def test_build_value_types_page_has_one_block_per_value_type() -> None:
	"""
	Check that each alias is documented on the page.

	.. versionadded:: 0.1.0
	"""
	page_content = build_value_types_page()

	block_count = page_content.count(":::")
	assert block_count == EXPECTED_VALUE_TYPE_COUNT


def test_find_value_type_paths_gives_nothing_for_a_package_without_them() -> None:
	"""
	Check that a loader knowing none of the aliases gives no path.

	.. versionadded:: 0.1.0
	"""
	_, loader = load_package()

	value_type_paths = find_value_type_paths(loader)

	assert value_type_paths == {}


def test_find_value_type_paths_finds_every_alias_of_numdaplot() -> None:
	"""
	Check that the listed paths still match the source.

	.. versionadded:: 0.1.0
	"""
	loader = griffe.GriffeLoader()
	loader.load("numdaplot")

	value_type_paths = find_value_type_paths(loader)

	assert value_type_paths == VALUE_TYPE_PATHS


def test_link_type_parameters_makes_an_annotation_refer_to_the_alias() -> None:
	"""
	Check that the type parameter named after a value type resolves to the alias.

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package()
	between = package[BETWEEN_PATH]

	link_type_parameters(between, ALIAS_PATHS, loader)

	assert between.members["low"].annotation.canonical_path == ALIAS_PATH


def test_link_type_parameters_reaches_a_name_inside_a_list() -> None:
	"""
	Check an annotation such as list[OrderedValue].

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package()
	between = package[BETWEEN_PATH]

	link_type_parameters(between, ALIAS_PATHS, loader)

	names = [part for part in between.members["bounds"].annotation.iterate() if isinstance(part, griffe.ExprName)]
	resolved_paths = {name.canonical_path for name in names}
	assert ALIAS_PATH in resolved_paths


def test_link_type_parameters_leaves_the_other_annotations() -> None:
	"""
	Check that an annotation without the type parameter is unchanged.

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package()
	between = package[BETWEEN_PATH]

	link_type_parameters(between, ALIAS_PATHS, loader)

	assert str(between.members["name"].annotation) == "str"
