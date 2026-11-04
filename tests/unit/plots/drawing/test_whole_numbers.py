"""
Unit tests of the ticks of an axis holding whole numbers only.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import numpy
from matplotlib.figure import Figure
from matplotlib.ticker import AutoLocator

from numdaplot.plots.drawing.whole_numbers import has_only_whole_numbers, place_whole_ticks

WHOLE_NUMBERS = numpy.array([1.0, numpy.nan, 3.0])
DECIMALS = numpy.array([1.0, 2.5])


def test_has_only_whole_numbers_ignores_missing_values() -> None:
	"""
	Check that NaN does not prevent numbers from being whole.

	.. versionadded:: 0.1.0
	"""
	all_whole = has_only_whole_numbers(WHOLE_NUMBERS)

	assert all_whole


def test_has_only_whole_numbers_is_false_with_a_fraction() -> None:
	"""
	Check that 2.5 is not whole.

	.. versionadded:: 0.1.0
	"""
	all_whole = has_only_whole_numbers(DECIMALS)

	assert not all_whole


def test_place_whole_ticks_keeps_the_default_ticks_for_decimals() -> None:
	"""
	Check that decimals keep the default locator of matplotlib.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	place_whole_ticks(axes.xaxis, DECIMALS)

	locator = axes.xaxis.get_major_locator()
	assert isinstance(locator, AutoLocator)


def test_place_whole_ticks_replaces_the_default_ticks_for_whole_numbers() -> None:
	"""
	Check that whole numbers get a locator other than the default one.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	place_whole_ticks(axes.xaxis, WHOLE_NUMBERS)

	locator = axes.xaxis.get_major_locator()
	assert not isinstance(locator, AutoLocator)
