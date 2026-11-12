"""
Legends placed with ``LegendPosition.BEST`` that hide values, moved past the axes.

.. versionadded:: 0.2.0
"""

from typing import Any, cast

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.legend import Legend
from matplotlib.transforms import Bbox

from numdaplot.plots.drawing.style_drawing import BEST_LEGEND_ID, LEGEND_LOCATIONS, OUTSIDE_ANCHOR
from numdaplot.plots.style.legend_position import LegendPosition

OUTSIDE_LOCATION = LEGEND_LOCATIONS[LegendPosition.OUTSIDE_RIGHT]


def move_hiding_legends(figure: Figure) -> None:
	"""
	Move past the axes on the right every legend placed with ``BEST`` that hides at least one value.

	The figure is laid out first, so that the legends and the values are at their final places. A figure without
	such a legend is left as it is, without this extra layout.

	.. versionadded:: 0.2.0

	Parameters
	----------
	figure
		A figure whose Plots are drawn.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.legend_overlap import move_hiding_legends
	>>> from numdaplot.plots.drawing.style_drawing import BEST_LEGEND_ID
	>>> figure = Figure()
	>>> axes = figure.add_subplot()
	>>> grid_values = [float(number) for number in range(10)]
	>>> points = axes.scatter(grid_values * 10, sorted(grid_values * 10), label="grid")
	>>> line = axes.plot([0.0, 9.0], [4.5, 4.5], label="middle")
	>>> axes.legend(loc="best").set_gid(BEST_LEGEND_ID)
	>>> move_hiding_legends(figure)
	>>> anchor_box = axes.get_legend().get_bbox_to_anchor()
	>>> bool(anchor_box.x0 > axes.bbox.x1)
	True
	"""
	checked_legends = list[tuple[Axes, Legend]]()

	for axes in figure.axes:
		legend = axes.get_legend()
		if legend is not None and legend.get_gid() == BEST_LEGEND_ID:
			checked_legends.append((axes, legend))

	if not checked_legends:
		return

	figure.draw_without_rendering()

	for axes, legend in checked_legends:
		legend_box = legend.get_window_extent()
		hides_values = covers_values(axes, legend_box)
		if hides_values:
			move_past_axes(axes, legend)


def covers_values(axes: Axes, legend_box: Bbox) -> bool:
	"""
	Return whether a box covers a point, a part of a line or a patch, such as a bar, of the axes.

	.. versionadded:: 0.2.0

	Parameters
	----------
	axes
		The matplotlib axes holding the values.
	legend_box
		The box of the legend, in the coordinates of the page.

	Returns
	-------
	bool
		True when at least one value is under the box.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from matplotlib.transforms import Bbox
	>>> from numdaplot.plots.drawing.legend_overlap import covers_values
	>>> figure = Figure()
	>>> axes = figure.add_subplot()
	>>> points = axes.scatter([0.0, 1.0], [0.0, 1.0])
	>>> figure.draw_without_rendering()
	>>> corner = axes.transData.transform((0.0, 0.0))
	>>> covers_values(axes, Bbox.from_bounds(corner[0] - 5.0, corner[1] - 5.0, 10.0, 10.0))
	True
	"""
	for collection in axes.collections:
		offsets = collection.get_offsets()
		# Some versions of the matplotlib stubs leave the type of the transformed points unknown.
		offset_transform = cast(Any, collection.get_offset_transform())
		page_points = offset_transform.transform(offsets)
		covered_count = legend_box.count_contains(page_points)
		if covered_count > 0:
			return True

	for line in axes.lines:
		line_path = line.get_path()
		line_transform = line.get_transform()
		page_path = line_transform.transform_path(line_path)
		crosses_box = page_path.intersects_bbox(legend_box, filled=False)
		if crosses_box:
			return True

	for patch in axes.patches:
		patch_box = patch.get_window_extent()
		overlaps_box = patch_box.overlaps(legend_box)
		if overlaps_box:
			return True

	return False


def move_past_axes(axes: Axes, legend: Legend) -> None:
	"""
	Place a legend past the axes on the right, as ``LegendPosition.OUTSIDE_RIGHT`` does.

	.. versionadded:: 0.2.0

	Parameters
	----------
	axes
		The matplotlib axes of the legend.
	legend
		The legend moved.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.legend_overlap import move_past_axes
	>>> axes = Figure().add_subplot()
	>>> lines = axes.plot([0.0, 1.0], label="price")
	>>> legend = axes.legend(loc="best")
	>>> move_past_axes(axes, legend)
	>>> anchor_box = legend.get_bbox_to_anchor()
	>>> bool(anchor_box.x0 > axes.bbox.x1)
	True
	"""
	legend.set_loc(OUTSIDE_LOCATION)
	legend.set_bbox_to_anchor(OUTSIDE_ANCHOR, transform=axes.transAxes)
