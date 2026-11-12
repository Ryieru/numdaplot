"""
Functional tests of the values written on the bars of a Plot.

.. versionadded:: 0.2.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import warnings

from matplotlib.axes import Axes
from matplotlib.figure import Figure

import numdaplot as ndp

CLUSTERS = ["Noise", "C0", "C1", "C2"]
DIABETIC_SHARES = [0.523, 0.531, 0.18, 0.912]
SENIOR_SHARES = [0.31, 0.27, 0.64, 0.58]
SHARE_CHANGES = [0.31, -0.27, None, -0.58]
ROW_COUNTS = [120, 80, 45, 300]
EXPECTED_SHARE_TEXTS = ["0.52", "0.53", "0.18", "0.91"]
EXPECTED_CHANGE_TEXTS = ["0.31", "-0.27", "-0.58"]
EXPECTED_COUNT_TEXTS = ["120", "80", "45", "300"]
WHITE = "#ffffff"
BLACK = "#000000"
UPRIGHT = 90.0
NARROW_SIZE = ndp.Size(width=4.0, height=4.0)
TINY_SIZE = ndp.Size(width=2.0, height=2.0)
WIDE_VALUE_COUNT = 16
CROWDED_VALUE_COUNT = 120
FIRST_COUNT = 1000.0
COUNT_STEP = 137.25
EXPECTED_HIDDEN_MESSAGE = (
	"The values of 120 bars do not fit their bars and are not written. Give a larger ndp.Size, or fewer decimals in "
	"ValueLabels."
)
TWO_DECIMALS = ndp.ValueLabels(decimals=2)
HIDDEN_VALUES_START = "The values of"


def build_clusters() -> ndp.Table:
	"""
	Return a Table of shares and counts per cluster.

	.. versionadded:: 0.2.0

	Returns
	-------
	ndp.Table
		The columns cluster, diabetic, senior, change and rows.
	"""
	columns = {
		"cluster": ndp.Array.from_list(CLUSTERS),
		"diabetic": ndp.Array.from_list(DIABETIC_SHARES),
		"senior": ndp.Array.from_list(SENIOR_SHARES),
		"change": ndp.Array.from_list(SHARE_CHANGES),
		"rows": ndp.Array.from_list(ROW_COUNTS),
	}
	clusters = ndp.Table.from_arrays(columns)

	return clusters


def build_counts(count: int) -> ndp.Table:
	"""
	Return a Table of growing decimal counts, one per cluster.

	.. versionadded:: 0.2.0

	Parameters
	----------
	count
		The number of clusters.

	Returns
	-------
	ndp.Table
		The columns cluster and count.
	"""
	names = [f"C{i}" for i in range(count)]
	values = [FIRST_COUNT + COUNT_STEP * i for i in range(count)]
	name_array = ndp.Array.from_list(names)
	value_array = ndp.Array.from_list(values)
	counts = ndp.Table.from_arrays({"cluster": name_array, "count": value_array})

	return counts


def draw(plot: ndp.Plot) -> tuple[Figure, Axes]:
	"""
	Return the laid out matplotlib figure of a Plot, and its axes.

	.. versionadded:: 0.2.0

	Parameters
	----------
	plot
		The Plot.

	Returns
	-------
	tuple[Figure, Axes]
		The figure, laid out, and its first axes.
	"""
	figure = plot.to_matplotlib()
	figure.draw_without_rendering()
	axes = figure.axes[0]

	return figure, axes


def read_shown_texts(axes: Axes) -> list[str]:
	"""
	Return the texts shown in an axes, in the order they were written.

	.. versionadded:: 0.2.0

	Parameters
	----------
	axes
		A matplotlib axes.

	Returns
	-------
	list[str]
		The visible texts.
	"""
	shown_texts = [text.get_text() for text in axes.texts if text.get_visible()]

	return shown_texts


def test_shares_are_written_with_two_decimals() -> None:
	"""
	Check that each bar gets its value rounded to two decimals.

	.. versionadded:: 0.2.0
	"""
	clusters = build_clusters()
	chart = ndp.BarChart(x="cluster", y=["diabetic"], value_labels=TWO_DECIMALS)

	_, axes = draw(ndp.Plot.bar(clusters, chart))

	shown_texts = read_shown_texts(axes)
	assert shown_texts == EXPECTED_SHARE_TEXTS


def test_no_value_is_written_by_default() -> None:
	"""
	Check that a BarChart without value_labels writes no value.

	.. versionadded:: 0.2.0
	"""
	clusters = build_clusters()
	chart = ndp.BarChart(x="cluster", y=["diabetic"])

	_, axes = draw(ndp.Plot.bar(clusters, chart))

	shown_texts = read_shown_texts(axes)
	assert shown_texts == []


def test_counts_are_written_without_decimals() -> None:
	"""
	Check that the values of an integer column have no decimals.

	.. versionadded:: 0.2.0
	"""
	clusters = build_clusters()
	chart = ndp.BarChart(x="cluster", y=["rows"], value_labels=TWO_DECIMALS)

	_, axes = draw(ndp.Plot.bar(clusters, chart))

	shown_texts = read_shown_texts(axes)
	assert shown_texts == EXPECTED_COUNT_TEXTS


def test_every_value_stays_inside_the_axes() -> None:
	"""
	Check that values past the end of positive and negative bars stay inside the axes, a missing value unwritten.

	.. versionadded:: 0.2.0
	"""
	clusters = build_clusters()
	chart = ndp.BarChart(x="cluster", y=["change"], value_labels=TWO_DECIMALS)

	_, axes = draw(ndp.Plot.bar(clusters, chart))

	shown_texts = read_shown_texts(axes)
	text_boxes = [text.get_window_extent() for text in axes.texts]
	axes_box = axes.get_window_extent()
	inside_flags = [axes_box.y0 <= text_box.y0 and text_box.y1 <= axes_box.y1 for text_box in text_boxes]
	assert shown_texts == EXPECTED_CHANGE_TEXTS
	assert all(inside_flags)


def test_horizontal_values_stay_inside_the_axes() -> None:
	"""
	Check that values past the end of negative horizontal bars stay inside the axes.

	.. versionadded:: 0.2.0
	"""
	clusters = build_clusters()
	chart = ndp.BarChart(x="cluster", y=["change"], orientation=ndp.Orientation.HORIZONTAL, value_labels=TWO_DECIMALS)

	_, axes = draw(ndp.Plot.bar(clusters, chart))

	text_boxes = [text.get_window_extent() for text in axes.texts]
	axes_box = axes.get_window_extent()
	inside_flags = [axes_box.x0 <= text_box.x0 and text_box.x1 <= axes_box.x1 for text_box in text_boxes]
	assert all(inside_flags)


def test_stacked_values_are_readable_on_their_colors() -> None:
	"""
	Check that the values of stacked bars are white on the dark blue and black on the light orange of the defaults.

	.. versionadded:: 0.2.0
	"""
	clusters = build_clusters()
	chart = ndp.BarChart(x="cluster", y=["diabetic", "senior"], layout=ndp.BarLayout.STACKED, value_labels=TWO_DECIMALS)

	_, axes = draw(ndp.Plot.bar(clusters, chart))

	value_count = len(CLUSTERS)
	text_colors = [text.get_color() for text in axes.texts]
	blue_colors = set(text_colors[:value_count])
	orange_colors = set(text_colors[value_count:])
	assert blue_colors == {WHITE}
	assert orange_colors == {BLACK}


def test_values_wider_than_their_bars_turn_upright() -> None:
	"""
	Check that values too wide for narrow bars are all turned upright, without warning about the values.

	.. versionadded:: 0.2.0
	"""
	counts = build_counts(WIDE_VALUE_COUNT)
	chart = ndp.BarChart(x="cluster", y=["count"], value_labels=TWO_DECIMALS)
	plot = ndp.Plot.bar(counts, chart, style=ndp.PlotStyle(size=NARROW_SIZE))

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		_, axes = draw(plot)

	rotations = {text.get_rotation() for text in axes.texts}
	warning_texts = [str(caught.message) for caught in caught_warnings]
	value_warnings = [warning_text for warning_text in warning_texts if warning_text.startswith(HIDDEN_VALUES_START)]
	assert rotations == {UPRIGHT}
	assert value_warnings == []


def test_values_without_room_are_left_out_with_a_warning() -> None:
	"""
	Check that values that do not fit even upright are not written, with a ReadabilityWarning.

	.. versionadded:: 0.2.0
	"""
	counts = build_counts(CROWDED_VALUE_COUNT)
	chart = ndp.BarChart(x="cluster", y=["count"], value_labels=TWO_DECIMALS)
	plot = ndp.Plot.bar(counts, chart, style=ndp.PlotStyle(size=TINY_SIZE))

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		_, axes = draw(plot)

	shown_texts = read_shown_texts(axes)
	warning_texts = [str(caught.message) for caught in caught_warnings]
	assert shown_texts == []
	assert EXPECTED_HIDDEN_MESSAGE in warning_texts
