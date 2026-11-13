"""
Default labels of a chart when its data names no column for an axis, or names several.

.. versionadded:: 0.1.0
"""

from numdaplot.plots.data.array_values import VALUE_LABEL
from numdaplot.plots.data.chart_values import ChartValues, Positions
from numdaplot.plots.data.sample_values import SampleValues

ROW_LABEL = "Row"
COLUMN_LABEL = "Column"


def find_position_label(positions: Positions) -> str:
	"""
	Return the default label of the axis of the positions: the name of their column, else ``Row``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	positions
		The positions of a chart.

	Returns
	-------
	str
		The label of the axis.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.data.chart_values import Positions
	>>> from numdaplot.plots.data.position_kind import PositionKind
	>>> from numdaplot.plots.drawing.default_labels import find_position_label
	>>> find_position_label(Positions(PositionKind.NUMBERS, numpy.array([0.0]), None))
	'Row'
	"""
	if positions.name is None:
		return ROW_LABEL

	return positions.name


def find_value_label(values: ChartValues | SampleValues) -> str | None:
	"""
	Return the default label of the axis of the series: the name of a single series, else ``Value``.

	Several series are named in the legend, so their axis only says that it holds their values. Their names stay in
	the default title.

	.. versionadded:: 0.2.0

	Parameters
	----------
	values
		The series of a chart and the name of their values.

	Returns
	-------
	str or None
		The label of the axis, None when the values have no name.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.table_values import read_table_values
	>>> from numdaplot.plots.drawing.default_labels import find_value_label
	>>> prices = ndp.Array.from_list([12.0])
	>>> costs = ndp.Array.from_list([8.0])
	>>> sales = ndp.Table.from_arrays({"price": prices, "cost": costs})
	>>> find_value_label(read_table_values(sales, None, ["price"], "LineChart"))
	'price'
	>>> find_value_label(read_table_values(sales, None, ["price", "cost"], "LineChart"))
	'Value'
	"""
	series_count = len(values.series)
	if series_count > 1:
		return VALUE_LABEL

	return values.value_name
