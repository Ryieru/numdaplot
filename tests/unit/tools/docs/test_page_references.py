"""
Unit tests of the MkDocs hook linking the inline code of the pages.

.. versionadded:: 0.1.0
"""

from types import SimpleNamespace

from page_references import find_unique_member_paths, link_inline_code, load_reference_index, on_page_content

ARRAY_CODE = "<p>Create an <code>Array</code>.</p>"
ARRAY_LINK = 'api-link-class"><autoref identifier="numdaplot.arrays.array.Array" optional>Array</autoref>'
MEMBER_CODE = "<code>Table.filter</code>"
TABLE_LINK = '<autoref identifier="numdaplot.tables.table.Table" optional>Table</autoref>'
FILTER_LINK = 'api-link-function"><autoref identifier="numdaplot.tables.table.Table.filter" optional>filter'
UNIQUE_MEMBER_CODE = "<code>from_spacing</code>"
UNIQUE_MEMBER_LINK = '<autoref identifier="numdaplot.arrays.array.Array.from_spacing" optional>'
SHARED_MEMBER_CODE = "<code>to_value</code>"
BLOCK_CODE = "<pre><code>Array\n</code></pre>"
API_PAGE = SimpleNamespace(file=SimpleNamespace(src_uri="api/arrays/array.md"))
CHANGELOG_PAGE = SimpleNamespace(file=SimpleNamespace(src_uri="changelog.md"))


def test_link_inline_code_links_a_public_class() -> None:
	"""
	Check that Array links to the Array class, colored as a class.

	.. versionadded:: 0.1.0
	"""
	index = load_reference_index()

	linked_html = link_inline_code(ARRAY_CODE, index)

	assert ARRAY_LINK in linked_html


def test_link_inline_code_links_a_class_and_its_member() -> None:
	"""
	Check that Table.filter links Table and filter separately.

	.. versionadded:: 0.1.0
	"""
	index = load_reference_index()

	linked_html = link_inline_code(MEMBER_CODE, index)

	assert TABLE_LINK in linked_html
	assert FILTER_LINK in linked_html


def test_link_inline_code_links_a_member_of_a_single_class() -> None:
	"""
	Check that from_spacing, which only Array has, links to Array.from_spacing.

	.. versionadded:: 0.1.0
	"""
	index = load_reference_index()

	linked_html = link_inline_code(UNIQUE_MEMBER_CODE, index)

	assert UNIQUE_MEMBER_LINK in linked_html


def test_link_inline_code_keeps_a_member_shared_by_several_classes() -> None:
	"""
	Check that to_value, which Array and Table both have, stays plain code.

	.. versionadded:: 0.1.0
	"""
	index = load_reference_index()

	linked_html = link_inline_code(SHARED_MEMBER_CODE, index)

	assert linked_html == SHARED_MEMBER_CODE


def test_link_inline_code_keeps_blocks_of_code() -> None:
	"""
	Check that a block of code is not linked.

	.. versionadded:: 0.1.0
	"""
	index = load_reference_index()

	linked_html = link_inline_code(BLOCK_CODE, index)

	assert linked_html == BLOCK_CODE


def test_find_unique_member_paths_leaves_out_shared_names() -> None:
	"""
	Check that from_spacing is kept and to_value is left out.

	.. versionadded:: 0.1.0
	"""
	index = load_reference_index()

	member_paths = find_unique_member_paths(index.context.public_paths, index.context.loader)

	assert "from_spacing" in member_paths
	assert "to_value" not in member_paths


def test_on_page_content_leaves_the_api_pages_to_their_docstrings() -> None:
	"""
	Check that an API page is unchanged and the changelog gets links.

	.. versionadded:: 0.1.0
	"""
	api_html = on_page_content(ARRAY_CODE, API_PAGE)
	changelog_html = on_page_content(ARRAY_CODE, CHANGELOG_PAGE)

	assert api_html == ARRAY_CODE
	assert ARRAY_LINK in changelog_html
