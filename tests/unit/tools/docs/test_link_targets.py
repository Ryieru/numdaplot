"""
Unit tests of what the names written in code can link to.

.. versionadded:: 0.1.0
"""

import griffe
from link_targets import (
	LinkContext,
	find_enum_member_paths,
	find_identifier,
	find_public_paths,
	find_unique_member_paths,
	object_exists,
)

PACKAGE_NAME = "sales"
PACKAGE_FILES = {
	"__init__.py": "from sales.table import Table\nfrom sales.rules import Greater\n",
	"rules.py": 'class Greater:\n    """Keep the values above a limit."""\n    def show(self) -> None: ...\n',
	"reading.py": "class Reading:\n    def from_csv(self) -> None: ...\n",
	"table.py": (
		"from sales.reading import Reading\n"
		"class Table(Reading):\n"
		"    INT64 = 1\n"
		"    def to_csv(self) -> None: ...\n"
		"    def show(self) -> None: ...\n"
	),
}
TABLE_PATH = "sales.table.Table"
GREATER_PATH = "sales.rules.Greater"
FROM_CSV_PATH = "sales.table.Table.from_csv"
TO_CSV_PATH = "sales.table.Table.to_csv"
EXPECTED_PUBLIC_PATHS = {"Table": TABLE_PATH, "Greater": GREATER_PATH}
UNIQUE_MEMBER_PATHS = {"INT64": "sales.table.Table.INT64", "to_csv": TO_CSV_PATH}
EXPECTED_ENUM_MEMBER_PATHS = {"INT64": "sales.table.Table.INT64"}
SHARED_MEMBER_NAME = "show"


def load_package() -> tuple[griffe.Module, griffe.GriffeLoader]:
	"""
	Return a small package with a public class, its mixin and a rule, and a loader that knows it.

	.. versionadded:: 0.1.0

	Returns
	-------
	tuple[griffe.Module, griffe.GriffeLoader]
		The package and its loader.
	"""
	loader = griffe.GriffeLoader()
	with griffe.temporary_visited_package(PACKAGE_NAME, PACKAGE_FILES) as package:
		loader.modules_collection.set_member(package.path, package)
		loader.resolve_aliases()

	return package, loader


def build_context(class_path: str | None) -> LinkContext:
	"""
	Return the link context of a docstring of the small package.

	.. versionadded:: 0.1.0

	Parameters
	----------
	class_path
		The documented class owning the docstring.

	Returns
	-------
	LinkContext
		The context.
	"""
	package, loader = load_package()
	public_paths = find_public_paths(package)
	context = LinkContext(class_path, public_paths, loader, {})

	return context


def test_find_public_paths_follows_the_exported_aliases() -> None:
	"""
	Check the path of each name exported by the package.

	.. versionadded:: 0.1.0
	"""
	package, _ = load_package()

	public_paths = find_public_paths(package)

	assert public_paths == EXPECTED_PUBLIC_PATHS


def test_object_exists_finds_inherited_members() -> None:
	"""
	Check that a member inherited from a mixin exists on the public class, and an unknown one does not.

	.. versionadded:: 0.1.0
	"""
	_, loader = load_package()

	inherited_exists = object_exists(FROM_CSV_PATH, loader)
	unknown_exists = object_exists(TABLE_PATH + ".missing", loader)

	assert inherited_exists
	assert not unknown_exists


def test_find_identifier_prefers_a_member_of_the_class() -> None:
	"""
	Check that from_csv inside Table links to Table.from_csv.

	.. versionadded:: 0.1.0
	"""
	context = build_context(TABLE_PATH)

	identifier = find_identifier("from_csv", context)

	assert identifier == FROM_CSV_PATH


def test_find_identifier_follows_public_names() -> None:
	"""
	Check ndp.Greater, and Table.to_csv written with its class.

	.. versionadded:: 0.1.0
	"""
	context = build_context(None)

	greater_identifier = find_identifier("ndp.Greater", context)
	to_csv_identifier = find_identifier("Table.to_csv", context)

	assert greater_identifier == GREATER_PATH
	assert to_csv_identifier == TO_CSV_PATH


def test_find_identifier_gives_nothing_for_an_unknown_name() -> None:
	"""
	Check that a name matching no object gives None.

	.. versionadded:: 0.1.0
	"""
	context = build_context(TABLE_PATH)

	identifier = find_identifier("Missing", context)

	assert identifier is None


def test_find_unique_member_paths_leaves_out_shared_names() -> None:
	"""
	Check that to_csv is kept and a name that two public classes have is left out.

	.. versionadded:: 0.1.0
	"""
	context = build_context(None)

	member_paths = find_unique_member_paths(context.public_paths, context.loader)

	assert member_paths["to_csv"] == TO_CSV_PATH
	assert SHARED_MEMBER_NAME not in member_paths


def test_find_enum_member_paths_keeps_the_names_in_capital_letters() -> None:
	"""
	Check that INT64 is kept and to_csv is left out.

	.. versionadded:: 0.1.0
	"""
	enum_member_paths = find_enum_member_paths(UNIQUE_MEMBER_PATHS)

	assert enum_member_paths == EXPECTED_ENUM_MEMBER_PATHS
