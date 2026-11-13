"""
Unit tests of the default labels of a chart.

.. versionadded:: 0.2.0
"""

import numpy

import numdaplot as ndp
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.data.chart_values import Positions
from numdaplot.plots.data.position_kind import PositionKind
from numdaplot.plots.data.table_values import read_table_values
from numdaplot.plots.drawing.default_labels import ROW_LABEL, find_position_label, find_value_label

PRICES = ndp.Array.from_list([12.0, 15.5])
COSTS = ndp.Array.from_list([8.0, 9.0])
SALES = ndp.Table.from_arrays({"price": PRICES, "cost": COSTS})
PRICE_COLUMN = "price"
VALUE_LABEL = "Value"
GRID = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
CHART_NAME = "LineChart"
ORIGIN = numpy.array([0.0])
UNNAMED_POSITIONS = Positions(PositionKind.NUMBERS, ORIGIN, None)
NAMED_POSITIONS = Positions(PositionKind.NUMBERS, ORIGIN, PRICE_COLUMN)


def test_find_value_label_names_a_single_series() -> None:
	"""
	Check that a single column names the axis of the values.

	.. versionadded:: 0.2.0
	"""
	values = read_table_values(SALES, None, [PRICE_COLUMN], CHART_NAME)

	value_label = find_value_label(values)

	assert value_label == PRICE_COLUMN


def test_find_value_label_gives_value_to_several_series() -> None:
	"""
	Check that several columns label the axis of the values Value.

	.. versionadded:: 0.2.0
	"""
	values = read_table_values(SALES, None, [PRICE_COLUMN, "cost"], CHART_NAME)

	value_label = find_value_label(values)

	assert value_label == VALUE_LABEL


def test_find_value_label_gives_value_to_an_array() -> None:
	"""
	Check that the columns of an Array label the axis of the values Value.

	.. versionadded:: 0.2.0
	"""
	values = read_array_values(GRID, CHART_NAME)

	value_label = find_value_label(values)

	assert value_label == VALUE_LABEL


def test_find_position_label_names_rows_without_column() -> None:
	"""
	Check that positions without column are labeled Row.

	.. versionadded:: 0.2.0
	"""
	position_label = find_position_label(UNNAMED_POSITIONS)

	assert position_label == ROW_LABEL


def test_find_position_label_names_the_column_of_the_positions() -> None:
	"""
	Check that the column of the positions labels their axis.

	.. versionadded:: 0.2.0
	"""
	position_label = find_position_label(NAMED_POSITIONS)

	assert position_label == PRICE_COLUMN
