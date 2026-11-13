"""
Unit tests of the MkDocs hook linking each object of the API pages to its source on GitHub.

.. versionadded:: 0.2.0
"""

from pathlib import Path
from types import SimpleNamespace

import griffe
import pytest
import source_links
from source_links import (
	ICON_PATH,
	SourceLines,
	SourceSite,
	add_source_links,
	find_object,
	find_source_lines,
	find_theme_file,
	load_package,
	on_page_content,
	read_version_tag,
	write_source_link,
)

PROJECT_TEXT = '[project]\nname = "sales"\nversion = "1.2.3"\n'
EXPECTED_TAG = "v1.2.3"
REPOSITORY_URL = "https://github.com/Ryieru/numdaplot"
FAKE_ICON = "<svg></svg>"
SITE = SourceSite(REPOSITORY_URL, "v0.2.0", FAKE_ICON)
ARRAY_LINES = SourceLines("src/numdaplot/arrays/array.py", 23, 64)
EXPECTED_ARRAY_LINK = (
	'<a class="source-link" '
	'href="https://github.com/Ryieru/numdaplot/blob/v0.2.0/src/numdaplot/arrays/array.py#L23-L64" '
	'title="Source of Array on GitHub" target="_blank" rel="noopener"><svg></svg><span>Source</span></a>'
)
INHERITED_METHOD_PATH = "arrays.array.Array.convert"
DEFINING_CLASS = "ArrayTypeChange"
GROUP_PATH = "arrays.array.Array--creation"
ENUM_MEMBER_PATH = "types.type.Type.INT8"
TYPE_FILE = "src/numdaplot/types/type.py"
ATTRIBUTE_NAME = "price"
CONVERT_HEADING = (
	'<h3 id="numdaplot.arrays.array.Array.convert" class="doc doc-heading"><code>convert</code>'
	'<a href="#numdaplot.arrays.array.Array.convert" class="headerlink">'
)
CONVERT_SOURCE = "/src/numdaplot/arrays/array_type_change.py#L"
GROUP_HEADING = (
	'<h2 id="numdaplot.arrays.array.Array--creation" class="doc doc-heading">Creation'
	'<a href="#numdaplot.arrays.array.Array--creation" class="headerlink">'
)
API_PAGE = SimpleNamespace(file=SimpleNamespace(src_uri="api/arrays/array.md"))
CHANGELOG_PAGE = SimpleNamespace(file=SimpleNamespace(src_uri="changelog.md"))
CONFIG = {"repo_url": REPOSITORY_URL}
FIELD_PATH = "conversions.array_conversion.ArrayConversion.dtype"
FIND_SPEC_NAME = "find_spec"
LINELESS_HEADING = (
	'<h3 id="numdaplot.price" class="doc doc-heading">price<a href="#numdaplot.price" class="headerlink">'
)


def test_read_version_tag_gives_v_and_the_version(tmp_path: Path) -> None:
	"""
	Check that the tag is v followed by the version of the project file.

	.. versionadded:: 0.2.0

	Parameters
	----------
	tmp_path
		A temporary folder holding the project file.
	"""
	project_file = tmp_path / "pyproject.toml"
	project_file.write_text(PROJECT_TEXT)

	version_tag = read_version_tag(project_file)

	assert version_tag == EXPECTED_TAG


def test_find_theme_file_finds_the_github_icon() -> None:
	"""
	Check that the GitHub icon of the theme is found and is an SVG.

	.. versionadded:: 0.2.0
	"""
	icon_file = find_theme_file(ICON_PATH)

	icon_text = icon_file.read_text()
	assert icon_text.startswith("<svg")


def test_find_object_follows_an_inherited_method_to_its_group() -> None:
	"""
	Check that a method of Array inherited from a group of methods is found in that group.

	.. versionadded:: 0.2.0
	"""
	package = load_package()

	found_object = find_object(package, INHERITED_METHOD_PATH)

	assert found_object is not None
	assert found_object.parent is not None
	assert found_object.parent.name == DEFINING_CLASS


def test_find_object_gives_none_for_a_path_that_is_not_an_object() -> None:
	"""
	Check that the heading of a group of methods is not an object.

	.. versionadded:: 0.2.0
	"""
	package = load_package()

	found_object = find_object(package, GROUP_PATH)

	assert found_object is None


def test_find_source_lines_includes_the_docstring_of_an_attribute() -> None:
	"""
	Check that the lines of an enum member go down to the end of its docstring.

	.. versionadded:: 0.2.0
	"""
	package = load_package()
	int8 = find_object(package, ENUM_MEMBER_PATH)
	assert int8 is not None

	source_lines = find_source_lines(int8)

	assert source_lines is not None
	assert source_lines.file_path == TYPE_FILE
	assert source_lines.last_line > source_lines.first_line


def test_find_source_lines_gives_none_without_lines() -> None:
	"""
	Check that an object griffe knows no line of has no source lines.

	.. versionadded:: 0.2.0
	"""
	attribute = griffe.Attribute(ATTRIBUTE_NAME)

	source_lines = find_source_lines(attribute)

	assert source_lines is None


def test_write_source_link_opens_the_lines_at_the_version_tag() -> None:
	"""
	Check the address, the title, the icon and the word of the link.

	.. versionadded:: 0.2.0
	"""
	source_link = write_source_link(ARRAY_LINES, "Array", SITE)

	assert source_link == EXPECTED_ARRAY_LINK


def test_add_source_links_places_the_link_before_the_permanent_link() -> None:
	"""
	Check that the heading of a method gets a link to the file defining it, before its permanent link.

	.. versionadded:: 0.2.0
	"""
	package = load_package()

	linked_html = add_source_links(CONVERT_HEADING, package, SITE)

	link_position = linked_html.index('class="source-link"')
	permalink_position = linked_html.index('class="headerlink"')
	assert CONVERT_SOURCE in linked_html
	assert link_position < permalink_position


def test_add_source_links_keeps_a_heading_that_is_not_an_object() -> None:
	"""
	Check that the heading of a group of methods stays without link.

	.. versionadded:: 0.2.0
	"""
	package = load_package()

	linked_html = add_source_links(GROUP_HEADING, package, SITE)

	assert linked_html == GROUP_HEADING


def test_on_page_content_links_the_objects_of_an_api_page() -> None:
	"""
	Check that an API page gets its source links.

	.. versionadded:: 0.2.0
	"""
	linked_html = on_page_content(CONVERT_HEADING, API_PAGE, CONFIG)

	assert CONVERT_SOURCE in linked_html


def test_on_page_content_keeps_a_page_outside_the_api_reference() -> None:
	"""
	Check that a page outside the API reference is left unchanged.

	.. versionadded:: 0.2.0
	"""
	linked_html = on_page_content(CONVERT_HEADING, CHANGELOG_PAGE, CONFIG)

	assert linked_html == CONVERT_HEADING


def find_no_spec(name: str) -> None:
	"""
	Fake search of a package that finds none.

	.. versionadded:: 0.2.0

	Parameters
	----------
	name
		The name of the package, ignored.
	"""


def test_find_theme_file_fails_without_the_theme(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that a missing theme raises ModuleNotFoundError.

	.. versionadded:: 0.2.0

	Parameters
	----------
	monkeypatch
		Replaces the search of packages with one that finds none.
	"""
	monkeypatch.setattr(source_links, FIND_SPEC_NAME, find_no_spec)

	with pytest.raises(ModuleNotFoundError):
		find_theme_file(ICON_PATH)


def test_find_source_lines_keeps_the_line_of_a_field_without_docstring() -> None:
	"""
	Check that a field of a setting object, without docstring, links to its own line.

	.. versionadded:: 0.2.0
	"""
	package = load_package()
	field = find_object(package, FIELD_PATH)
	assert field is not None

	source_lines = find_source_lines(field)

	assert source_lines is not None
	assert source_lines.last_line == source_lines.first_line


def test_add_source_links_keeps_a_heading_of_an_object_without_lines() -> None:
	"""
	Check that the heading of an object griffe knows no line of stays without link.

	.. versionadded:: 0.2.0
	"""
	package = griffe.Module(source_links.PACKAGE_NAME)
	price_attribute = griffe.Attribute(ATTRIBUTE_NAME)
	package.set_member(ATTRIBUTE_NAME, price_attribute)

	linked_html = add_source_links(LINELESS_HEADING, package, SITE)

	assert linked_html == LINELESS_HEADING
