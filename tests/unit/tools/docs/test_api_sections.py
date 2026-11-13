"""
Unit tests of the sections of the navigation of the API pages.

.. versionadded:: 0.2.0
"""

import pytest
from api_sections import find_section

FILES_MODULE = "numdaplot.tables.files.csv.csv_read_options"
EXPECTED_FILE_GROUP = "File settings"
UNKNOWN_MODULE = "numdaplot.reports.report"
TABLES_TITLE = "Tables"


def test_find_section_prefers_the_most_precise_prefix() -> None:
	"""
	Check that a file settings module goes to the File settings group of Tables.

	.. versionadded:: 0.1.0
	"""
	section = find_section(FILES_MODULE)

	assert section.title == TABLES_TITLE
	assert section.group == EXPECTED_FILE_GROUP


def test_find_section_rejects_a_module_without_section() -> None:
	"""
	Check that a package missing from SECTIONS raises KeyError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(KeyError):
		find_section(UNKNOWN_MODULE)
