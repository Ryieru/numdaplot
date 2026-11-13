"""
A chart and the values it draws.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.value_axis import ValueAxis
from numdaplot.plots.data.chart_values import ChartValues
from numdaplot.plots.data.point_values import PointValues
from numdaplot.plots.data.sample_values import SampleValues


@dataclass(frozen=True, eq=False)
class ChartLayer:
	"""
	A chart and the values it draws, read when the Plot is created.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart
		The chart settings.
	values
		The positions and the series, or for a ``HistogramChart`` and a ``BoxChart`` the columns and their groups.
	points
		The values coloring and sizing the points of a ``ScatterChart``, None for other charts.
	value_axis
		The vertical axis the chart is measured on, ``ValueAxis.LEFT`` unless added on the right.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.layers.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> ChartLayer(ndp.LineChart(), read_array_values(prices, "LineChart")).points is None
	True
	"""

	chart: Chart
	values: ChartValues | SampleValues
	points: PointValues | None = None
	value_axis: ValueAxis = ValueAxis.LEFT
