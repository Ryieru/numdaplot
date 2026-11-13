"""
Title and axis labels of a Plot, chosen between its style and the defaults of its chart.

.. versionadded:: 0.1.0
"""

from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.style.plot_style import PlotStyle

DEFAULT_TITLE = "{y_label} by {x_label}"


def choose_title(drawn_chart: DrawnChart, style: PlotStyle) -> str:
	"""
	Return the title of a Plot: the style one, else the one of the chart, else the ``y`` label by the ``x`` label.

	A label removed with an empty text keeps its default name in the title. The default name of an axis in the title
	is its title name when the chart gives one, such as the names of several series whose axis is labeled ``Value``.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Uses the title names of the chart in place of the default labels of its axes.

	Parameters
	----------
	drawn_chart
		The default title and labels of the chart.
	style
		The title and the labels chosen, None for the default ones.

	Returns
	-------
	str
		The title, empty when the style removes it or when the chart has no label to build it from.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.drawing.drawn_chart import DrawnChart
	>>> from numdaplot.plots.drawing.grid_axes import GridAxes
	>>> from numdaplot.plots.drawing.chart_texts import choose_title
	>>> drawn_chart = DrawnChart("day", "price", False, GridAxes.BOTH, None)
	>>> choose_title(drawn_chart, ndp.PlotStyle())
	'price by day'
	>>> choose_title(drawn_chart, ndp.PlotStyle(x_label="Day"))
	'price by Day'
	>>> several_series = DrawnChart("day", "Value", False, GridAxes.BOTH, None, y_title_name="price, cost")
	>>> choose_title(several_series, ndp.PlotStyle())
	'price, cost by day'
	"""
	if style.title is not None:
		return style.title

	if drawn_chart.title is not None:
		return drawn_chart.title

	x_name = find_title_name(drawn_chart.x_title_name, drawn_chart.x_label)
	y_name = find_title_name(drawn_chart.y_title_name, drawn_chart.y_label)
	x_label = choose_title_label(style.x_label, x_name)
	y_label = choose_title_label(style.y_label, y_name)
	if x_label == "" or y_label == "":
		return ""

	title = DEFAULT_TITLE.format(y_label=y_label, x_label=x_label)

	return title


def find_title_name(title_name: str | None, axis_label: str | None) -> str | None:
	"""
	Return the default name of an axis in the title: its title name, else its default label.

	.. versionadded:: 0.2.0

	Parameters
	----------
	title_name
		The name of the values of the axis in the title, or None when it is the label of the axis.
	axis_label
		The default label of the axis, or None.

	Returns
	-------
	str or None
		The name used in the title, None when the axis has neither.

	Examples
	--------
	>>> from numdaplot.plots.drawing.chart_texts import find_title_name
	>>> find_title_name("price, cost", "Value"), find_title_name(None, "price")
	('price, cost', 'price')
	"""
	if title_name is not None:
		return title_name

	return axis_label


def choose_title_label(style_label: str | None, default_label: str | None) -> str:
	"""
	Return the name of an axis in a title: the style label, else the default label, even for a removed style label.

	.. versionadded:: 0.1.0

	Parameters
	----------
	style_label
		The label chosen in the style, None for the default and an empty text for no label.
	default_label
		The default label of the chart, None for no label.

	Returns
	-------
	str
		The name, empty when there is none.

	Examples
	--------
	>>> from numdaplot.plots.drawing.chart_texts import choose_title_label
	>>> choose_title_label("", "price")
	'price'
	"""
	chosen_label = choose_label(style_label, default_label)
	if chosen_label != "":
		return chosen_label

	default_name = choose_label(None, default_label)

	return default_name


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
	>>> from numdaplot.plots.drawing.chart_texts import choose_label
	>>> choose_label(None, "price")
	'price'
	"""
	if style_label is not None:
		return style_label

	if default_label is not None:
		return default_label

	return ""
