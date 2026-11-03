"""
Unit tests of Region.

.. versionadded:: 0.1.0
"""

from numdaplot.positions.index import Index
from numdaplot.positions.range import Range
from numdaplot.positions.region import Region

COLUMN_NAMES = ["mois", "total"]
ADDED_COLUMN = "prix"
FIRST_ROW = Index(0)
FIRST_ROWS = Range(start=0, stop=4)


def test_region_takes_every_row_and_column_by_default() -> None:
	"""
	Check that rows and columns are None, meaning everything, when omitted.

	.. versionadded:: 0.1.0
	"""
	region = Region()

	assert region.rows is None
	assert region.columns is None


def test_region_keeps_positions_as_given() -> None:
	"""
	Check that an Index and a Range are kept as they are.

	.. versionadded:: 0.1.0
	"""
	region = Region(rows=FIRST_ROWS, columns=FIRST_ROW)

	assert region.rows == FIRST_ROWS
	assert region.columns == FIRST_ROW


def test_region_is_not_changed_by_a_later_change_of_the_given_column_names() -> None:
	"""
	Check that the region holds its own copy of the list of column names.

	.. versionadded:: 0.1.0
	"""
	given_columns = list(COLUMN_NAMES)
	region = Region(columns=given_columns)

	given_columns.append(ADDED_COLUMN)

	assert region.columns == COLUMN_NAMES
