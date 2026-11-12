"""
Axes crossed by the grid lines of a chart.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class GridAxes(Enum):
	"""
	Axes crossed by the grid lines of a chart, when its PlotStyle shows grid lines.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.drawing.line_drawing import draw_line_chart
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> layer = ChartLayer(ndp.LineChart(), read_array_values(prices, "LineChart"))
	>>> draw_line_chart(Figure().add_subplot(), layer).grid_axes
	<GridAxes.BOTH: 1>
	"""

	BOTH = auto()
	"""
	Grid lines across both axes, as for lines and points.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.drawn_chart import DrawnChart
	>>> from numdaplot.plots.drawing.grid_axes import GridAxes
	>>> from numdaplot.plots.drawing.style_drawing import draw_grid_lines
	>>> axes = Figure().add_subplot()
	>>> draw_grid_lines(axes, DrawnChart(None, None, False, GridAxes.BOTH, None))
	>>> axes.xaxis.get_gridlines()[0].get_visible()
	True
	"""

	VALUES = auto()
	"""
	Grid lines across the axis of the values only, as for bars, histograms and boxes.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.drawn_chart import DrawnChart
	>>> from numdaplot.plots.drawing.grid_axes import GridAxes
	>>> from numdaplot.plots.drawing.style_drawing import draw_grid_lines
	>>> axes = Figure().add_subplot()
	>>> draw_grid_lines(axes, DrawnChart(None, None, False, GridAxes.VALUES, None))
	>>> axes.xaxis.get_gridlines()[0].get_visible()
	False
	"""

	NONE = auto()
	"""
	No grid lines, as for pies and heatmaps, whose grid lines would cross the drawing.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.drawn_chart import DrawnChart
	>>> from numdaplot.plots.drawing.grid_axes import GridAxes
	>>> from numdaplot.plots.drawing.style_drawing import draw_grid_lines
	>>> axes = Figure().add_subplot()
	>>> draw_grid_lines(axes, DrawnChart(None, None, False, GridAxes.NONE, None))
	>>> axes.yaxis.get_gridlines()[0].get_visible()
	False
	"""
