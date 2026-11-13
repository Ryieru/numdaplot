"""
Unit tests of the MkDocs hook generating the API pages and their navigation.

.. versionadded:: 0.1.0
"""

from pathlib import Path
from types import SimpleNamespace
from typing import Any

from api_pages import (
	PublicObject,
	build_api_nav,
	build_member_block,
	build_page_content,
	find_page_path,
	find_public_objects,
	on_config,
	on_files,
	order_public_object,
)
from api_sections import find_section
from mkdocs.structure.files import Files

import numdaplot

RULES_MODULE = "numdaplot.rules.greater"
FILES_MODULE = "numdaplot.tables.files.csv.csv_read_options"
EXPECTED_FILE_GROUP = "File settings"
GREATER_SECTION = find_section(RULES_MODULE)
GREATER = PublicObject("Greater", "numdaplot.rules.greater.Greater", GREATER_SECTION)
RULE = PublicObject("Rule", "numdaplot.rules.rule.Rule", GREATER_SECTION)
TABLE_SECTION = find_section("numdaplot.tables.table")
TABLE = PublicObject("Table", "numdaplot.tables.table.Table", TABLE_SECTION)
CSV_SECTION = find_section(FILES_MODULE)
CSV_OPTIONS = PublicObject("CsvReadOptions", "numdaplot.tables.files.csv.csv_read_options.CsvReadOptions", CSV_SECTION)
EXPECTED_GREATER_PATH = "api/rules/greater.md"
EXPECTED_GREATER_PAGE = "::: numdaplot.rules.greater.Greater\n    options:\n      heading_level: 1\n"
TABLE_SECTION_TITLE = "## Reading files { .api-section }"
TABLE_MEMBER_LINE = "::: numdaplot.tables.table.Table.from_csv"
ATTRIBUTE_OPTION = "show_signature_annotations: true"
HOME_ENTRY = {"Home": "index.md"}
CHANGELOG_ENTRY = {"Changelog": "changelog.md"}
API_TITLE = "API"
FIRST_PUBLIC_NAME = "Array"
ROW_COUNT_NAME = "row_count"
FILTER_NAME = "filter"
EXPECTED_VALUE_TYPES_SECTION = {"Types": [{"Value types": "api/types/value_types.md"}]}


def test_find_public_objects_gives_every_public_name() -> None:
	"""
	Check that every name of ndp.__all__ gets a page, Array first.

	.. versionadded:: 0.1.0
	"""
	public_objects = find_public_objects()

	names = [public_object.name for public_object in public_objects]
	sorted_names = sorted(names)
	sorted_public_names = sorted(numdaplot.__all__)
	assert sorted_names == sorted_public_names
	assert names[0] == FIRST_PUBLIC_NAME


def test_order_public_object_puts_the_main_classes_first() -> None:
	"""
	Check that Rule comes before Greater although it comes after it alphabetically.

	.. versionadded:: 0.1.0
	"""
	rule_key = order_public_object(RULE)
	greater_key = order_public_object(GREATER)

	assert rule_key < greater_key


def test_find_page_path_names_the_page_after_its_module() -> None:
	"""
	Check the path of the page of Greater.

	.. versionadded:: 0.1.0
	"""
	page_path = find_page_path(GREATER)

	assert page_path == EXPECTED_GREATER_PATH


def test_build_page_content_gives_the_class_as_page_title() -> None:
	"""
	Check the page of a class without sections.

	.. versionadded:: 0.1.0
	"""
	page_content = build_page_content(GREATER)

	assert page_content == EXPECTED_GREATER_PAGE


def test_build_page_content_lists_the_members_of_table_in_sections() -> None:
	"""
	Check that the Table page has its sections and members.

	.. versionadded:: 0.1.0
	"""
	page_content = build_page_content(TABLE)

	assert TABLE_SECTION_TITLE in page_content
	assert TABLE_MEMBER_LINE in page_content


def test_build_member_block_shows_the_type_of_an_attribute() -> None:
	"""
	Check that row_count shows its type and filter does not.

	.. versionadded:: 0.1.0
	"""
	attribute_block = build_member_block(TABLE, ROW_COUNT_NAME)
	method_block = build_member_block(TABLE, FILTER_NAME)

	assert ATTRIBUTE_OPTION in attribute_block
	assert ATTRIBUTE_OPTION not in method_block


def test_build_api_nav_groups_settings_inside_their_section() -> None:
	"""
	Check that CsvReadOptions sits in the File settings group of Tables, after Table.

	.. versionadded:: 0.1.0
	"""
	api_nav = build_api_nav([TABLE, CSV_OPTIONS])

	assert api_nav == [
		{
			"Tables": [
				{"Table": "api/tables/table.md"},
				{EXPECTED_FILE_GROUP: [{"CsvReadOptions": "api/tables/csv_read_options.md"}]},
			]
		},
		EXPECTED_VALUE_TYPES_SECTION,
	]


def test_on_config_places_the_api_after_the_home_page() -> None:
	"""
	Check that the API section is inserted between Home and Changelog.

	.. versionadded:: 0.1.0
	"""
	config = {"nav": [HOME_ENTRY, CHANGELOG_ENTRY]}

	updated_config = on_config(config)

	navigation = updated_config["nav"]
	assert navigation[0] == HOME_ENTRY
	assert API_TITLE in navigation[1]
	assert navigation[2] == CHANGELOG_ENTRY


def test_on_files_adds_one_page_per_public_object(tmp_path: Path) -> None:
	"""
	Check that a generated page exists for Greater, with its content.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary site folder.
	"""
	plugins = SimpleNamespace(_current_plugin=None)
	site_folder = str(tmp_path)
	config = SimpleNamespace(site_dir=site_folder, use_directory_urls=True, plugins=plugins)
	files = Files([])

	generated_files = on_files(files, cast_config(config))

	greater_file = generated_files.get_file_from_path(EXPECTED_GREATER_PATH)
	assert greater_file is not None
	assert greater_file.content_string == EXPECTED_GREATER_PAGE


def cast_config(config: SimpleNamespace) -> Any:
	"""
	Return a fake MkDocs configuration typed as the hook expects it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	config
		The fake configuration.

	Returns
	-------
	Any
		The same object.
	"""
	return config
