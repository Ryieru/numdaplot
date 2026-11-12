"""
Unit tests of the colors of the series of a chart.

.. versionadded:: 0.1.0
"""

import warnings

import pytest

from numdaplot.errors.invalid_color_count_error import InvalidColorCountError
from numdaplot.errors.readability_warning import ReadabilityWarning
from numdaplot.plots.drawing.colored_parts import ColoredParts
from numdaplot.plots.drawing.series_colors import (
	COLOR_CODES,
	CYCLE_LENGTH,
	choose_series_colors,
	find_color_code,
	require_color_count,
	take_cycle_colors,
	warn_shared_colors,
)
from numdaplot.plots.style.color import Color
from numdaplot.plots.style.custom_color import CustomColor

ORANGE_CODE = "#ff8800"
FIRST_CYCLE_CODE = "#1f77b4"
LIGHT_BLUE_CODE = "#aec7e8"
NAMED_COLOR_COUNT = 10
CHART_NAME = "LineChart"
EXPECTED_GIVEN_CODES = [COLOR_CODES[Color.RED], ORANGE_CODE]
EXPECTED_SHARED_MESSAGE = (
	"A ScatterChart with 21 color groups is hard to read: 20 colors are available, so some groups share a color."
)
SCATTER_NAME = "ScatterChart"


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


def test_choose_series_colors_gives_a_light_color_to_the_eleventh_series() -> None:
	"""
	Check that the eleventh series takes the light color of the first one.

	.. versionadded:: 0.2.0
	"""
	series_count = NAMED_COLOR_COUNT + 1

	color_codes = choose_series_colors(None, series_count, CHART_NAME, ColoredParts.SERIES)

	assert color_codes[-1] == LIGHT_BLUE_CODE


def test_choose_series_colors_starts_the_cycle_again_with_a_warning() -> None:
	"""
	Check that the series after the cycle take its first color again, with a ReadabilityWarning.

	.. versionadded:: 0.1.0
	"""
	series_count = CYCLE_LENGTH + 1

	with pytest.warns(ReadabilityWarning):
		color_codes = choose_series_colors(None, series_count, CHART_NAME, ColoredParts.SERIES)

	code_count = len(color_codes)
	assert code_count == series_count
	assert color_codes[-1] == FIRST_CYCLE_CODE


def test_choose_series_colors_does_not_warn_for_given_colors() -> None:
	"""
	Check that colors chosen for each series never warn, however many there are.

	.. versionadded:: 0.2.0
	"""
	series_count = CYCLE_LENGTH + 1
	colors = list[Color | CustomColor]([Color.RED] * series_count)

	with warnings.catch_warnings():
		warnings.simplefilter("error")
		color_codes = choose_series_colors(colors, series_count, CHART_NAME, ColoredParts.SERIES)

	code_count = len(color_codes)
	assert code_count == series_count


def test_choose_series_colors_follows_the_given_colors() -> None:
	"""
	Check that given colors are used in order.

	.. versionadded:: 0.1.0
	"""
	colors = list[Color | CustomColor]([Color.RED, CustomColor(ORANGE_CODE)])

	color_codes = choose_series_colors(colors, 2, CHART_NAME, ColoredParts.SERIES)

	assert color_codes == EXPECTED_GIVEN_CODES


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


def test_take_cycle_colors_follows_cyan_with_light_blue() -> None:
	"""
	Check that the light colors follow the ten named colors.

	.. versionadded:: 0.2.0
	"""
	colors = take_cycle_colors(NAMED_COLOR_COUNT - 1, 2)

	assert colors == [Color.CYAN, CustomColor(LIGHT_BLUE_CODE)]


def test_take_cycle_colors_starts_again_after_the_whole_cycle() -> None:
	"""
	Check that the cycle starts again with blue after its last color.

	.. versionadded:: 0.1.0
	"""
	colors = take_cycle_colors(CYCLE_LENGTH, 1)

	assert colors == [Color.BLUE]


def test_warn_shared_colors_names_the_chart_and_its_parts() -> None:
	"""
	Check the warning of a ScatterChart with one color group more than the cycle.

	.. versionadded:: 0.2.0
	"""
	group_count = CYCLE_LENGTH + 1

	with pytest.warns(ReadabilityWarning) as caught_warnings:
		warn_shared_colors(SCATTER_NAME, ColoredParts.COLOR_GROUPS, group_count)

	warning_message = caught_warnings[0].message
	warning_text = str(warning_message)
	assert warning_text == EXPECTED_SHARED_MESSAGE


def test_warn_shared_colors_stays_silent_for_a_full_cycle() -> None:
	"""
	Check that as many parts as colors give no warning.

	.. versionadded:: 0.2.0
	"""
	with warnings.catch_warnings():
		warnings.simplefilter("error")
		warn_shared_colors(SCATTER_NAME, ColoredParts.COLOR_GROUPS, CYCLE_LENGTH)
