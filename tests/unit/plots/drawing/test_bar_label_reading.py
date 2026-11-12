"""
Unit tests of the values written on bars, read back with their bars.

.. versionadded:: 0.2.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from numdaplot.plots.drawing.bar_label_reading import read_bar_labels
from numdaplot.plots.drawing.bar_value_labels import LabelPlace, write_value_labels

TWO_POSITIONS = [0.0, 1.0]
TWO_LENGTHS = [1.0, 2.0]
TWO_TEXTS = ["1.00", "2.00"]


def build_figure(figure_size: tuple[float, float] | None = None) -> tuple[Figure, Axes]:
	"""
	Return a figure and its axes, to draw bars on.

	.. versionadded:: 0.2.0

	Parameters
	----------
	figure_size
		The size of the figure in inches, the matplotlib default when omitted.

	Returns
	-------
	tuple[Figure, Axes]
		The figure and its single axes.
	"""
	figure = Figure(figsize=figure_size)
	axes = figure.add_subplot()

	return figure, axes


def test_read_bar_labels_pairs_each_bar_with_its_value() -> None:
	"""
	Check that each marked bar comes with its text and its place.

	.. versionadded:: 0.2.0
	"""
	_, axes = build_figure()
	bars = axes.bar(TWO_POSITIONS, TWO_LENGTHS)
	write_value_labels(axes, bars, TWO_TEXTS, LabelPlace.VERTICAL_END)

	bar_labels = read_bar_labels(axes)

	texts = [bar_label.text.get_text() for bar_label in bar_labels]
	labeled_bars = [bar_label.bar for bar_label in bar_labels]
	drawn_bars = list(bars.patches)
	places = {bar_label.place for bar_label in bar_labels}
	assert texts == TWO_TEXTS
	assert labeled_bars == drawn_bars
	assert places == {LabelPlace.VERTICAL_END}


def test_read_bar_labels_leaves_out_bars_without_value() -> None:
	"""
	Check that bars drawn without values give no label.

	.. versionadded:: 0.2.0
	"""
	_, axes = build_figure()
	axes.bar(TWO_POSITIONS, TWO_LENGTHS)

	bar_labels = read_bar_labels(axes)

	assert bar_labels == []
