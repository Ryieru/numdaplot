"""
Unit tests of ParquetReadOptions.

.. versionadded:: 0.1.0
"""

from numdaplot.tables.files.column_names import ColumnNames
from numdaplot.tables.files.parquet_read_options import ParquetReadOptions


def test_parquet_read_options_clean_the_column_names_by_default() -> None:
	"""
	Check that the column names are cleaned by default.

	.. versionadded:: 0.1.0
	"""
	options = ParquetReadOptions()

	assert options.column_names == ColumnNames.CLEANED


def test_parquet_read_options_keep_their_setting() -> None:
	"""
	Check that a given setting is available as an attribute.

	.. versionadded:: 0.1.0
	"""
	options = ParquetReadOptions(column_names=ColumnNames.KEPT)

	assert options.column_names == ColumnNames.KEPT
