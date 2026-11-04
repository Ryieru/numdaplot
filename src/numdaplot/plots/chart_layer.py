"""
A chart and the values it draws.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.data.chart_values import ChartValues
from numdaplot.plots.data.point_values import PointValues


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
		The positions and the series.
	points
		The values coloring and sizing the points of a ``ScatterChart``, None for other charts.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> ChartLayer(ndp.LineChart(), read_array_values(prices, "LineChart")).points is None
	True
	"""

	chart: Chart
	values: ChartValues
	points: PointValues | None = None
