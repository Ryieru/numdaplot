"""
Drawing of the PlotStyle of a Plot: title, axis labels, rotation of the values, grid lines and legend.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from operator import itemgetter
from typing import Any, Literal, cast

from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection
from matplotlib.container import Container
from matplotlib.figure import Figure
from matplotlib.transforms import ScaledTranslation, Transform

from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.grid_axes import GridAxes
from numdaplot.plots.drawing.plot_axes import PlotAxes
from numdaplot.plots.drawing.tick_rotation import rotate_x_labels, rotate_y_labels
from numdaplot.plots.style.grid_lines import GridLines
from numdaplot.plots.style.legend_position import LegendPosition
from numdaplot.plots.style.plot_style import PlotStyle

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
LEGEND_POINT_OPACITY = 1.0


def apply_style(plot_axes: PlotAxes, drawn_chart: DrawnChart, style: PlotStyle) -> None:
	"""
	Draw the title, the axis labels, the rotation of the values, the grid lines and the legend of a Plot.

	.. versionadded:: 0.1.0

	Parameters
	----------
	plot_axes
		The matplotlib axes of the Plot, with the ones on the right if any.
	drawn_chart
		The default labels and axis directions of its first chart.
	style
		The look of the Plot.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.drawn_chart import DrawnChart
	>>> from numdaplot.plots.drawing.grid_axes import GridAxes
	>>> from numdaplot.plots.drawing.plot_axes import PlotAxes
	>>> from numdaplot.plots.drawing.style_drawing import apply_style
	>>> axes = Figure().add_subplot()
	>>> drawn_chart = DrawnChart("day", "price", False, GridAxes.BOTH, None)
	>>> apply_style(PlotAxes(axes, None, None), drawn_chart, ndp.PlotStyle(title="Sales"))
	>>> axes.get_title(), axes.get_xlabel(), axes.get_ylabel()
	('Sales', 'day', 'price')
	"""
	axes = plot_axes.left
	if style.title is not None:
		axes.set_title(style.title)

	write_axis_labels(axes, drawn_chart, style)
	write_right_label(plot_axes, style)
	rotate_x_labels(axes, drawn_chart, style.x_tick_rotation)
	rotate_y_labels(axes, drawn_chart, style.y_tick_rotation)
	if style.grid_lines == GridLines.SHOWN:
		draw_grid_lines(axes, drawn_chart)

	if style.legend != LegendPosition.HIDDEN:
		place_legend(plot_axes, drawn_chart, style.legend)


def write_axis_labels(axes: Axes, drawn_chart: DrawnChart, style: PlotStyle) -> None:
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
	>>> from numdaplot.plots.drawing.grid_axes import GridAxes
	>>> from numdaplot.plots.drawing.style_drawing import write_axis_labels
	>>> axes = Figure().add_subplot()
	>>> drawn_chart = DrawnChart("city", "price", True, GridAxes.VALUES, None)
	>>> write_axis_labels(axes, drawn_chart, ndp.PlotStyle(y_label="Euros"))
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
	Draw light grid lines across the axes the chart asks for: both, the axis of the values only, or none.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes of the Plot.
	drawn_chart
		The axes crossed by the grid lines, and where the ``x`` values are.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.drawn_chart import DrawnChart
	>>> from numdaplot.plots.drawing.grid_axes import GridAxes
	>>> from numdaplot.plots.drawing.style_drawing import draw_grid_lines
	>>> axes = Figure().add_subplot()
	>>> draw_grid_lines(axes, DrawnChart(None, None, False, GridAxes.VALUES, None))
	>>> axes.yaxis.get_gridlines()[0].get_visible(), axes.xaxis.get_gridlines()[0].get_visible()
	(True, False)
	"""
	if drawn_chart.grid_axes == GridAxes.NONE:
		return

	if drawn_chart.grid_axes == GridAxes.BOTH:
		axes.grid(True)
		return

	value_axis = VALUE_GRID_AXES[drawn_chart.x_on_vertical_axis]
	axes.grid(True, axis=value_axis)


def write_right_label(plot_axes: PlotAxes, style: PlotStyle) -> None:
	"""
	Write the label of the axis on the right, the style one or else the default one, when the Plot has that axis.

	.. versionadded:: 0.1.0

	Parameters
	----------
	plot_axes
		The matplotlib axes of the Plot.
	style
		The label chosen, None for the default.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.plot_axes import PlotAxes
	>>> from numdaplot.plots.drawing.style_drawing import write_right_label
	>>> axes = Figure().add_subplot()
	>>> right_axes = axes.twinx()
	>>> write_right_label(PlotAxes(axes, right_axes, "price"), ndp.PlotStyle())
	>>> right_axes.get_ylabel()
	'price'
	"""
	if plot_axes.right is None:
		return

	right_label = choose_label(style.right_label, plot_axes.right_label)
	plot_axes.right.set_ylabel(right_label)


def place_legend(plot_axes: PlotAxes, drawn_chart: DrawnChart, legend_position: LegendPosition) -> None:
	"""
	Draw the legend naming the series of every chart, when there are at least two of them.

	The series are named in the order they are drawn, the ones of the left axes first. The legend is drawn over
	the axes on the right if any, so their charts never hide it. With these axes, ``BEST`` and ``OUTSIDE_RIGHT`` place
	it past their axis: ``BEST`` would only avoid their charts, not the ones of the left axes. Points sized by
	``size_by`` are all shown with the same size in the legend, which names their colors.

	.. versionadded:: 0.1.0

	Parameters
	----------
	plot_axes
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
	>>> from numdaplot.plots.drawing.grid_axes import GridAxes
	>>> from numdaplot.plots.drawing.plot_axes import PlotAxes
	>>> from numdaplot.plots.drawing.style_drawing import place_legend
	>>> axes = Figure().add_subplot()
	>>> price_lines = axes.plot([1.0, 2.0], label="price")
	>>> right_axes = axes.twinx()
	>>> cost_lines = right_axes.plot([3.0, 1.0], label="cost")
	>>> drawn_chart = DrawnChart(None, None, False, GridAxes.BOTH, None)
	>>> place_legend(PlotAxes(axes, right_axes, None), drawn_chart, ndp.LegendPosition.UPPER_LEFT)
	>>> [text.get_text() for text in right_axes.get_legend().get_texts()]
	['price', 'cost']
	"""
	handles, labels = list_legend_entries(plot_axes.left)
	legend_axes = plot_axes.left
	if plot_axes.right is not None:
		right_handles, right_labels = list_legend_entries(plot_axes.right)
		handles = [*handles, *right_handles]
		labels = [*labels, *right_labels]
		legend_axes = plot_axes.right

	label_count = len(labels)
	if label_count < MINIMUM_LEGEND_ENTRIES:
		return

	location = LEGEND_LOCATIONS[legend_position]
	anchor = None
	anchor_transform = None
	has_right_axes = plot_axes.right is not None
	best_goes_outside = has_right_axes and legend_position == LegendPosition.BEST
	is_outside = best_goes_outside or legend_position == LegendPosition.OUTSIDE_RIGHT
	if is_outside:
		location = LEGEND_LOCATIONS[LegendPosition.OUTSIDE_RIGHT]
		anchor = OUTSIDE_ANCHOR

	if is_outside and plot_axes.right is not None:
		anchor_transform = find_transform_past_right_axis(plot_axes.right)

	legend = legend_axes.legend(
		handles,
		labels,
		loc=location,
		bbox_to_anchor=anchor,
		bbox_transform=anchor_transform,
		title=drawn_chart.legend_title,
	)

	for handle in legend.legend_handles:
		if isinstance(handle, PathCollection):
			handle.set_sizes([LEGEND_POINT_AREA])
			handle.set_alpha(LEGEND_POINT_OPACITY)


def find_transform_past_right_axis(right_axes: Axes) -> Transform:
	"""
	Return the coordinates of the axes shifted past the values and the label of their axis on the right.

	The shift is a fixed distance on the page, which stays right when the layout then narrows the axes.

	.. versionadded:: 0.1.0

	Parameters
	----------
	right_axes
		The axes on the right, with their label and their ticks.

	Returns
	-------
	matplotlib.transforms.Transform
		The coordinates to anchor the legend with.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.style_drawing import find_transform_past_right_axis
	>>> axes = Figure().add_subplot()
	>>> right_axes = axes.twinx()
	>>> transform = find_transform_past_right_axis(right_axes)
	>>> bool(transform.transform((1.0, 0.0))[0] > right_axes.transAxes.transform((1.0, 0.0))[0])
	True
	"""
	axes_box = right_axes.get_window_extent()
	axis_box = right_axes.yaxis.get_tightbbox()
	axis_width = 0.0
	if axis_box is not None:
		axis_width = axis_box.x1 - axes_box.x1

	figure = cast(Figure, right_axes.get_figure(root=True))
	shift_inches = axis_width / figure.dpi
	shift = ScaledTranslation(shift_inches, 0.0, figure.dpi_scale_trans)
	transform = right_axes.transAxes + shift

	return transform


def list_legend_entries(axes: Axes) -> tuple[list[Any], list[str]]:
	"""
	Return the legend entries of matplotlib axes in the order their series were drawn.

	matplotlib lists bars and boxes after lines and points, whatever their order: each entry is placed back at
	the position of its first drawn shape.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes.

	Returns
	-------
	tuple[list[Any], list[str]]
		The handles drawn in the legend, and the label of each one.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.style_drawing import list_legend_entries
	>>> axes = Figure().add_subplot()
	>>> bars = axes.bar([0.0, 1.0], [3.0, 4.0], label="sales")
	>>> lines = axes.plot([0.0, 1.0], [2.0, 5.0], label="target")
	>>> list_legend_entries(axes)[1]
	['sales', 'target']
	"""
	handles, labels = axes.get_legend_handles_labels()
	children = axes.get_children()
	child_positions = {id(child): i for i, child in enumerate(children)}
	child_count = len(children)
	entry_positions = list[int]()

	for handle in handles:
		shape_id = find_first_shape_id(handle)
		entry_position = child_positions.get(shape_id, child_count)
		entry_positions.append(entry_position)

	entries = zip(entry_positions, handles, labels, strict=True)
	ordered_entries = sorted(entries, key=itemgetter(0))
	ordered_handles = [handle for _, handle, _ in ordered_entries]
	ordered_labels = [label for _, _, label in ordered_entries]

	return ordered_handles, ordered_labels


def find_first_shape_id(handle: Any) -> int:
	"""
	Return the identity of the first shape drawn for a legend entry.

	.. versionadded:: 0.1.0

	Parameters
	----------
	handle
		A legend handle: a drawn shape, or a container of shapes such as the bars of a series.

	Returns
	-------
	int
		The ``id`` of the shape, or of the first shape of a container that holds one, else of the handle.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.style_drawing import find_first_shape_id
	>>> axes = Figure().add_subplot()
	>>> bars = axes.bar([0.0, 1.0], [3.0, 4.0])
	>>> find_first_shape_id(bars) == id(bars.patches[0])
	True
	"""
	if not isinstance(handle, Container):
		handle_id = id(handle)
		return handle_id

	# The matplotlib stubs leave the shapes of a container untyped.
	shapes = cast(tuple[Artist, ...], handle)
	shape_count = len(shapes)
	if shape_count == 0:
		container_id = id(handle)
		return container_id

	first_shape = shapes[0]
	shape_id = id(first_shape)

	return shape_id
