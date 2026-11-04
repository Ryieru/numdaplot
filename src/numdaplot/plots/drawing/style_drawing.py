"""
Drawing of the Style of a Plot: title, axis labels, grid lines and legend.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from typing import Literal

from matplotlib.axes import Axes
from matplotlib.collections import PathCollection

from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.style.grid_lines import GridLines
from numdaplot.plots.style.legend_position import LegendPosition
from numdaplot.plots.style.style import Style

type LegendLocation = Literal["best", "upper left", "upper right", "lower left", "lower right", "center left"]
"""A legend location matplotlib accepts.

.. versionadded:: 0.1.0
"""

LEGEND_LOCATIONS = dict[LegendPosition, LegendLocation](
	{
		LegendPosition.BEST: "best",
		LegendPosition.UPPER_LEFT: "upper left",
		LegendPosition.UPPER_RIGHT: "upper right",
		LegendPosition.LOWER_LEFT: "lower left",
		LegendPosition.LOWER_RIGHT: "lower right",
		LegendPosition.OUTSIDE_RIGHT: "center left",
	}
)
OUTSIDE_ANCHOR = (1.02, 0.5)
# The grid lines of bars only cross the axis of their values, which depends on their direction.
VALUE_GRID_AXES = dict[bool, Literal["x", "y"]]({True: "x", False: "y"})
MINIMUM_LEGEND_ENTRIES = 2
LEGEND_POINT_AREA = 36.0


def apply_style(axes: Axes, drawn_chart: DrawnChart, style: Style) -> None:
	"""
	Draw the title, the axis labels, the grid lines and the legend of a Plot.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes of the Plot.
	drawn_chart
		The default labels and axis directions of its chart.
	style
		The look of the Plot.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.drawn_chart import DrawnChart
	>>> from numdaplot.plots.drawing.style_drawing import apply_style
	>>> axes = Figure().add_subplot()
	>>> apply_style(axes, DrawnChart("day", "price", False, True, None), ndp.Style(title="Sales"))
	>>> axes.get_title(), axes.get_xlabel(), axes.get_ylabel()
	('Sales', 'day', 'price')
	"""
	if style.title is not None:
		axes.set_title(style.title)

	write_axis_labels(axes, drawn_chart, style)
	if style.grid_lines == GridLines.SHOWN:
		draw_grid_lines(axes, drawn_chart)

	if style.legend != LegendPosition.HIDDEN:
		place_legend(axes, drawn_chart, style.legend)


def write_axis_labels(axes: Axes, drawn_chart: DrawnChart, style: Style) -> None:
	"""
	Write the labels of the axes, the style ones or else the defaults of the chart.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes of the Plot.
	drawn_chart
		The default labels and where the ``x`` values are.
	style
		The labels chosen, None for the defaults.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.drawn_chart import DrawnChart
	>>> from numdaplot.plots.drawing.style_drawing import write_axis_labels
	>>> axes = Figure().add_subplot()
	>>> write_axis_labels(axes, DrawnChart("city", "price", True, False, None), ndp.Style(y_label="Euros"))
	>>> axes.get_xlabel(), axes.get_ylabel()
	('Euros', 'city')
	"""
	x_label = choose_label(style.x_label, drawn_chart.x_label)
	y_label = choose_label(style.y_label, drawn_chart.y_label)
	if drawn_chart.x_on_vertical_axis:
		axes.set_xlabel(y_label)
		axes.set_ylabel(x_label)
		return

	axes.set_xlabel(x_label)
	axes.set_ylabel(y_label)


def choose_label(style_label: str | None, default_label: str | None) -> str:
	"""
	Return the label of an axis.

	.. versionadded:: 0.1.0

	Parameters
	----------
	style_label
		The label chosen in the style, None for the default.
	default_label
		The default label of the chart, None for no label.

	Returns
	-------
	str
		The chosen label, else the default one, else an empty text.

	Examples
	--------
	>>> from numdaplot.plots.drawing.style_drawing import choose_label
	>>> choose_label(None, "price")
	'price'
	"""
	if style_label is not None:
		return style_label

	if default_label is not None:
		return default_label

	return ""


def draw_grid_lines(axes: Axes, drawn_chart: DrawnChart) -> None:
	"""
	Draw light grid lines across both axes, or across the axis of the values only for bars.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes of the Plot.
	drawn_chart
		Whether the chart grids its ``x`` values, and where they are.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.drawn_chart import DrawnChart
	>>> from numdaplot.plots.drawing.style_drawing import draw_grid_lines
	>>> axes = Figure().add_subplot()
	>>> draw_grid_lines(axes, DrawnChart(None, None, False, False, None))
	>>> axes.yaxis.get_gridlines()[0].get_visible(), axes.xaxis.get_gridlines()[0].get_visible()
	(True, False)
	"""
	if drawn_chart.grids_positions:
		axes.grid(True)
		return

	value_axis = VALUE_GRID_AXES[drawn_chart.x_on_vertical_axis]
	axes.grid(True, axis=value_axis)


def place_legend(axes: Axes, drawn_chart: DrawnChart, legend_position: LegendPosition) -> None:
	"""
	Draw the legend naming the series, when there are at least two of them.

	Points sized by ``size_by`` are all shown with the same size in the legend, which names their colors.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes of the Plot.
	drawn_chart
		The title of the legend, if any.
	legend_position
		Where the legend is placed, other than ``HIDDEN``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.drawn_chart import DrawnChart
	>>> from numdaplot.plots.drawing.style_drawing import place_legend
	>>> axes = Figure().add_subplot()
	>>> lines = axes.plot([1, 2], label="price") + axes.plot([2, 1], label="cost")
	>>> place_legend(axes, DrawnChart(None, None, False, True, None), ndp.LegendPosition.UPPER_LEFT)
	>>> [text.get_text() for text in axes.get_legend().get_texts()]
	['price', 'cost']
	"""
	_, labels = axes.get_legend_handles_labels()
	label_count = len(labels)
	if label_count < MINIMUM_LEGEND_ENTRIES:
		return

	location = LEGEND_LOCATIONS[legend_position]
	anchor = None
	if legend_position == LegendPosition.OUTSIDE_RIGHT:
		anchor = OUTSIDE_ANCHOR

	legend = axes.legend(loc=location, bbox_to_anchor=anchor, title=drawn_chart.legend_title)

	for handle in legend.legend_handles:
		if isinstance(handle, PathCollection):
			handle.set_sizes([LEGEND_POINT_AREA])
