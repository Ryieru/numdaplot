"""
Unit tests of the colors of the series of a chart.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.invalid_color_count_error import InvalidColorCountError
from numdaplot.plots.drawing.series_colors import (
	COLOR_CODES,
	DEFAULT_CYCLE,
	choose_series_colors,
	find_color_code,
	require_color_count,
	take_cycle_colors,
)
from numdaplot.plots.style.color import Color
from numdaplot.plots.style.custom_color import CustomColor

ORANGE_CODE = "#ff8800"
CYCLE_LENGTH = len(DEFAULT_CYCLE)
FIRST_CYCLE_CODE = "#1f77b4"


@pytest.mark.parametrize("color", list(Color))
def test_find_color_code_knows_every_named_color(color: Color) -> None:
	"""
	Check that every Color has its code.

	.. versionadded:: 0.1.0

	Parameters
	----------
	color
		A named color.
	"""
	color_code = find_color_code(color)

	assert color_code == COLOR_CODES[color]


def test_find_color_code_keeps_the_code_of_a_custom_color() -> None:
	"""
	Check that a CustomColor gives its own code.

	.. versionadded:: 0.1.0
	"""
	color_code = find_color_code(CustomColor(ORANGE_CODE))

	assert color_code == ORANGE_CODE


def test_choose_series_colors_starts_the_cycle_again_after_ten_series() -> None:
	"""
	Check that the eleventh series takes the first color of the default cycle again.

	.. versionadded:: 0.1.0
	"""
	series_count = CYCLE_LENGTH + 1

	color_codes = choose_series_colors(None, series_count)

	assert len(color_codes) == series_count
	assert color_codes[-1] == FIRST_CYCLE_CODE


def test_choose_series_colors_follows_the_given_colors() -> None:
	"""
	Check that given colors are used in order.

	.. versionadded:: 0.1.0
	"""
	colors = list[Color | CustomColor]([Color.RED, CustomColor(ORANGE_CODE)])

	color_codes = choose_series_colors(colors, 2)

	assert color_codes == [COLOR_CODES[Color.RED], ORANGE_CODE]


def test_require_color_count_accepts_no_colors() -> None:
	"""
	Check that no colors are always accepted.

	.. versionadded:: 0.1.0
	"""
	require_color_count(None, 3)


def test_require_color_count_rejects_a_count_different_from_the_series() -> None:
	"""
	Check that one color for two series raises InvalidColorCountError.

	.. versionadded:: 0.1.0
	"""
	colors = list[Color | CustomColor]([Color.RED])

	with pytest.raises(InvalidColorCountError):
		require_color_count(colors, 2)


def test_take_cycle_colors_follows_the_colors_already_used() -> None:
	"""
	Check that the colors start after the ones used.

	.. versionadded:: 0.1.0
	"""
	colors = take_cycle_colors(1, 2)

	assert colors == [Color.ORANGE, Color.GREEN]


def test_take_cycle_colors_starts_again_after_ten_colors() -> None:
	"""
	Check that the cycle starts again with blue after cyan.

	.. versionadded:: 0.1.0
	"""
	colors = take_cycle_colors(9, 2)

	assert colors == [Color.CYAN, Color.BLUE]
