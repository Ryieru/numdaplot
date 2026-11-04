"""
Unit tests of the color bar of a chart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import numpy
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

from numdaplot.plots.drawing.color_bar import add_color_bar

WHOLE_NUMBERS = numpy.array([1.0, 2.0, numpy.nan, 5.0])
DECIMALS = numpy.array([0.5, 1.25])


def test_add_color_bar_draws_a_labeled_scale_next_to_the_axes() -> None:
	"""
	Check that the color bar is new axes with the label.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()
	scaled_points = axes.scatter([0.0, 1.0, 2.0, 3.0], [0.0, 1.0, 2.0, 3.0], c=WHOLE_NUMBERS)

	add_color_bar(axes, scaled_points, "rooms", WHOLE_NUMBERS)

	color_bar_label = figure.axes[1].get_ylabel()
	assert color_bar_label == "rooms"


def test_add_color_bar_places_whole_ticks_for_whole_numbers() -> None:
	"""
	Check that whole numbers, missing ones aside, give ticks on whole numbers only.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()
	scaled_points = axes.scatter([0.0, 1.0, 2.0, 3.0], [0.0, 1.0, 2.0, 3.0], c=WHOLE_NUMBERS)

	add_color_bar(axes, scaled_points, "", WHOLE_NUMBERS)

	locator = figure.axes[1].yaxis.get_major_locator()
	# AutoLocator, the default one, also inherits MaxNLocator.
	is_whole_locator = type(locator) is MaxNLocator
	assert is_whole_locator


def test_add_color_bar_keeps_the_default_ticks_for_decimals() -> None:
	"""
	Check that decimals keep the ticks matplotlib chooses.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()
	scaled_points = axes.scatter([0.0, 1.0], [0.0, 1.0], c=DECIMALS)

	add_color_bar(axes, scaled_points, "", DECIMALS)

	locator = figure.axes[1].yaxis.get_major_locator()
	is_whole_locator = type(locator) is MaxNLocator
	assert not is_whole_locator
