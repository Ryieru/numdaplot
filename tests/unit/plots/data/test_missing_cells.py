"""
Unit tests of the reading of the missing values of a Table.

.. versionadded:: 0.1.0
"""

import pandas

import numdaplot as ndp
from numdaplot.plots.data.missing_cells import read_missing_cells, read_missing_counts
from numdaplot.plots.data.position_kind import PositionKind

FLATS_FRAME = pandas.DataFrame(
	{
		"city": ["Paris", None, "Pau", "Lyon"],
		"price": [12.0, None, None, 15.5],
		"rooms": [2.0, 3.0, 1.0, 4.0],
	}
)
FLATS = ndp.Table.from_pandas(FLATS_FRAME)
EXPECTED_COLUMNS = ["city", "price", "rooms"]
EXPECTED_COUNTS = [1.0, 2.0, 0.0]
EXPECTED_RATIOS = [0.25, 0.5, 0.0]
EXPECTED_PRICE_CELLS = [0.0, 1.0, 1.0, 0.0]
EXPECTED_ROW_NUMBERS = [0.0, 1.0, 2.0, 3.0]


def test_read_missing_counts_counts_each_column() -> None:
	"""
	Check that each column gets its number of missing values, labeled Missing count.

	.. versionadded:: 0.1.0
	"""
	count_values = read_missing_counts(FLATS, ndp.Measure.COUNT)

	assert count_values.positions.kind == PositionKind.TEXTS
	assert count_values.positions.values.tolist() == EXPECTED_COLUMNS
	assert count_values.series[0].values.tolist() == EXPECTED_COUNTS
	assert count_values.value_name == "Missing count"


def test_read_missing_counts_gives_the_share_of_each_column() -> None:
	"""
	Check that ratios give the share of missing values, labeled Missing ratio.

	.. versionadded:: 0.1.0
	"""
	ratio_values = read_missing_counts(FLATS, ndp.Measure.RATIO)

	assert ratio_values.series[0].values.tolist() == EXPECTED_RATIOS
	assert ratio_values.value_name == "Missing ratio"


def test_read_missing_cells_marks_each_missing_value() -> None:
	"""
	Check that each column is a series of 1 for missing and 0 for present, at the row numbers.

	.. versionadded:: 0.1.0
	"""
	cell_values = read_missing_cells(FLATS)

	names = [series.name for series in cell_values.series]
	assert names == EXPECTED_COLUMNS
	assert cell_values.series[1].values.tolist() == EXPECTED_PRICE_CELLS
	assert cell_values.positions.values.tolist() == EXPECTED_ROW_NUMBERS
