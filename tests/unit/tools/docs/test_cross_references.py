"""
Unit tests of the griffe extension linking the names written in code.

.. versionadded:: 0.1.0
"""

import griffe
from cross_references import (
	CrossReferences,
	LinkContext,
	find_class_owners,
	find_identifier,
	find_public_paths,
	link_code_names,
	object_exists,
)

PACKAGE_NAME = "sales"
PACKAGE_FILES = {
	"__init__.py": "from sales.table import Table\nfrom sales.rules import Greater\n",
	"rules.py": 'class Greater:\n    """Keep the values above a limit."""\n',
	"reading.py": (
		"class Reading:\n"
		'    """Reading of a Table."""\n'
		"    def from_csv(self) -> None:\n"
		'        """Read a CSV file, or use ``to_csv`` to write one."""\n'
	),
	"table.py": (
		"from sales.reading import Reading\n"
		"class Table(Reading):\n"
		'    """Create it with ``from_csv``, filter with ``ndp.Greater``, see ``Missing``."""\n'
		"    def to_csv(self) -> None:\n"
		'        """Write a CSV file."""\n'
	),
}
TABLE_PATH = "sales.table.Table"
GREATER_PATH = "sales.rules.Greater"
READING_PATH = "sales.reading.Reading"
FROM_CSV_PATH = "sales.table.Table.from_csv"
TO_CSV_PATH = "sales.table.Table.to_csv"
EXPECTED_PUBLIC_PATHS = {"Table": TABLE_PATH, "Greater": GREATER_PATH}
FROM_CSV_LINK = (
	'<code><span class="api-link api-link-function">'
	'<autoref identifier="sales.table.Table.from_csv" optional>from_csv</autoref></span></code>'
)
GREATER_LINK = (
	'<code><span class="api-link api-link-class">'
	'<autoref identifier="sales.rules.Greater" optional>ndp.Greater</autoref></span></code>'
)
TO_CSV_LINK = (
	'<code><span class="api-link api-link-function">'
	'<autoref identifier="sales.table.Table.to_csv" optional>to_csv</autoref></span></code>'
)
MEMBER_TEXT = "Use ``Table.to_csv``."
MEMBER_LINKS = (
	'<code><span class="api-link api-link-class">'
	'<autoref identifier="sales.table.Table" optional>Table</autoref></span>'
	'.<span class="api-link api-link-function"><autoref identifier="sales.table.Table.to_csv" optional>to_csv'
	"</autoref></span></code>"
)
UNKNOWN_CODE = "``Missing``"
CALL_TEXT = "Call ``from_csv()`` first."
CALL_LINK = (
	'<code><span class="api-link api-link-function">'
	'<autoref identifier="sales.table.Table.from_csv" optional>from_csv()</autoref></span></code>'
)
LITERAL_TEXT = "Separated by ``,`` and ``;``."


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
	context = LinkContext(class_path, public_paths, loader)

	return context


def test_find_public_paths_follows_the_exported_aliases() -> None:
	"""
	Check the path of each name exported by the package.

	.. versionadded:: 0.1.0
	"""
	package, _ = load_package()

	public_paths = find_public_paths(package)

	assert public_paths == EXPECTED_PUBLIC_PATHS


def test_find_class_owners_gives_mixins_to_their_public_class() -> None:
	"""
	Check that the mixin Reading is documented by Table.

	.. versionadded:: 0.1.0
	"""
	package, _ = load_package()
	public_paths = find_public_paths(package)

	class_owners = find_class_owners(package, public_paths)

	assert class_owners[READING_PATH] == TABLE_PATH
	assert class_owners[TABLE_PATH] == TABLE_PATH


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


def test_link_code_names_links_known_names_and_keeps_the_others() -> None:
	"""
	Check the links of a class docstring, an unknown name staying plain code.

	.. versionadded:: 0.1.0
	"""
	context = build_context(TABLE_PATH)
	text = "Create it with ``from_csv``, filter with ``ndp.Greater``, see ``Missing``."

	linked_text = link_code_names(text, context)

	assert FROM_CSV_LINK in linked_text
	assert GREATER_LINK in linked_text
	assert UNKNOWN_CODE in linked_text


def test_link_code_names_keeps_the_parentheses_of_a_call() -> None:
	"""
	Check that a name followed by parentheses links to the function and keeps them in its text.

	.. versionadded:: 0.1.0
	"""
	context = build_context(TABLE_PATH)

	linked_text = link_code_names(CALL_TEXT, context)

	assert CALL_LINK in linked_text


def test_link_code_names_links_a_class_and_its_member_separately() -> None:
	"""
	Check that Table.to_csv links Table as a class and to_csv as a method, inside one code.

	.. versionadded:: 0.1.0
	"""
	context = build_context(None)

	linked_text = link_code_names(MEMBER_TEXT, context)

	assert MEMBER_LINKS in linked_text


def test_link_code_names_leaves_code_that_is_not_a_name() -> None:
	"""
	Check that punctuation written in code is unchanged.

	.. versionadded:: 0.1.0
	"""
	context = build_context(TABLE_PATH)

	linked_text = link_code_names(LITERAL_TEXT, context)

	assert linked_text == LITERAL_TEXT


def test_cross_references_link_the_docstrings_of_a_mixin_to_the_public_class() -> None:
	"""
	Check that to_csv in a method of the mixin links to Table.to_csv.

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package()
	extension = CrossReferences()

	extension.on_package(pkg=package, loader=loader)

	from_csv = package["reading.Reading.from_csv"]
	assert from_csv.docstring is not None
	assert TO_CSV_LINK in from_csv.docstring.value
