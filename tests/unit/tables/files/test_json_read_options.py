"""
Unit tests of JsonReadOptions.

.. versionadded:: 0.1.0
"""

from numdaplot.tables.files.column_names import ColumnNames
from numdaplot.tables.files.json_layout import JsonLayout
from numdaplot.tables.files.json_read_options import JsonReadOptions


def test_json_read_options_use_one_list_of_records_by_default() -> None:
	"""
	Check the default layout.

	.. versionadded:: 0.1.0
	"""
	options = JsonReadOptions()

	assert options.layout == JsonLayout.RECORDS


def test_json_read_options_clean_the_column_names_by_default() -> None:
	"""
	Check that the column names are cleaned by default.

	.. versionadded:: 0.1.0
	"""
	options = JsonReadOptions()

	assert options.column_names == ColumnNames.CLEANED
