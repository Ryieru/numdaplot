"""
Colors of the series of a chart.

.. versionadded:: 0.1.0
"""

import warnings
from collections.abc import Sequence
from itertools import cycle, islice

from numdaplot.arrays.operations.float_errors import INTERNAL_FILES
from numdaplot.errors.invalid_color_count_error import InvalidColorCountError
from numdaplot.errors.readability_warning import ReadabilityWarning
from numdaplot.plots.drawing.colored_parts import ColoredParts
from numdaplot.plots.style.color import Color
from numdaplot.plots.style.custom_color import CustomColor

COLOR_CODES = {
	Color.BLUE: "#1f77b4",
	Color.ORANGE: "#ff7f0e",
	Color.GREEN: "#2ca02c",
	Color.RED: "#d62728",
	Color.PURPLE: "#9467bd",
	Color.BROWN: "#8c564b",
	Color.PINK: "#e377c2",
	Color.GRAY: "#7f7f7f",
	Color.OLIVE: "#bcbd22",
	Color.CYAN: "#17becf",
	Color.BLACK: "#000000",
}
# The light colors of the tab20 colors of matplotlib, in the order of the named colors they lighten.
LIGHT_COLORS = (
	CustomColor("#aec7e8"),
	CustomColor("#ffbb78"),
	CustomColor("#98df8a"),
	CustomColor("#ff9896"),
	CustomColor("#c5b0d5"),
	CustomColor("#c49c94"),
	CustomColor("#f7b6d2"),
	CustomColor("#c7c7c7"),
	CustomColor("#dbdb8d"),
	CustomColor("#9edae5"),
)
DEFAULT_CYCLE = (
	Color.BLUE,
	Color.ORANGE,
	Color.GREEN,
	Color.RED,
	Color.PURPLE,
	Color.BROWN,
	Color.PINK,
	Color.GRAY,
	Color.OLIVE,
	Color.CYAN,
	*LIGHT_COLORS,
)
CYCLE_LENGTH = len(DEFAULT_CYCLE)
SHARED_COLORS_MESSAGE = (
	"A {owner_name} with {part_count} {parts} is hard to read: {color_count} colors are available, "
	"so some {short_parts} share a color."
)
SHORT_PART_NAMES = {
	ColoredParts.SERIES: "series",
	ColoredParts.COLOR_GROUPS: "groups",
	ColoredParts.SLICES: "slices",
}


def find_color_code(color: Color | CustomColor) -> str:
	"""
	Return the ``#rrggbb`` code of a color.

	.. versionadded:: 0.1.0

	Parameters
	----------
	color
		A named or a custom color.

	Returns
	-------
	str
		The code matplotlib draws.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.drawing.series_colors import find_color_code
	>>> find_color_code(ndp.Color.RED)
	'#d62728'
	"""
	if isinstance(color, CustomColor):
		return color.code

	color_code = COLOR_CODES[color]

	return color_code


def choose_series_colors(
	colors: Sequence[Color | CustomColor] | None,
	series_count: int,
	chart_name: str,
	parts: ColoredParts,
) -> list[str]:
	"""
	Return the color code of each series of a chart.

	.. versionadded:: 0.1.0

	.. versionchanged:: 0.2.0
		The default cycle has 20 colors, and a warning tells when series share a color.

	Parameters
	----------
	colors
		One color per series, or None for the colors of the default cycle, which starts again after 20 series.
	series_count
		The number of series drawn.
	chart_name
		The name of the chart, such as ``LineChart``, shown in the warning.
	parts
		What the series of the chart are, such as slices, shown in the warning.

	Returns
	-------
	list[str]
		One ``#rrggbb`` code per series.

	Raises
	------
	InvalidColorCountError
		When the colors are not exactly one per series.

	Warns
	-----
	ReadabilityWarning
		When the default cycle gives the same color to several series.

	Examples
	--------
	>>> from numdaplot.plots.drawing.colored_parts import ColoredParts
	>>> from numdaplot.plots.drawing.series_colors import choose_series_colors
	>>> choose_series_colors(None, 2, "LineChart", ColoredParts.SERIES)
	['#1f77b4', '#ff7f0e']
	"""
	chosen_colors = colors
	if chosen_colors is None:
		warn_shared_colors(chart_name, parts, series_count)
		cycled_colors = take_cycle_colors(0, series_count)
		chosen_colors = list[Color | CustomColor](cycled_colors)

	require_color_count(chosen_colors, series_count)
	color_codes = [find_color_code(color) for color in chosen_colors]

	return color_codes


def require_color_count(colors: Sequence[Color | CustomColor] | None, series_count: int) -> None:
	"""
	Check that a chart has one color per series, or no colors at all.

	.. versionadded:: 0.1.0

	Parameters
	----------
	colors
		The colors of the chart, or None for the colors of the default cycle.
	series_count
		The number of series drawn.

	Raises
	------
	InvalidColorCountError
		When the colors are not exactly one per series.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.drawing.series_colors import require_color_count
	>>> try:
	... 	require_color_count([ndp.Color.RED], 2)
	... except ndp.InvalidColorCountError as error:
	... 	print(error)
	Expected one color per series, 2 series and 1 color(s) given.
	"""
	if colors is None:
		return

	color_count = len(colors)
	if color_count != series_count:
		raise InvalidColorCountError(color_count, series_count)


def take_cycle_colors(start: int, color_count: int) -> list[Color | CustomColor]:
	"""
	Return colors of the default cycle: the ten named colors, then their light colors, then the same again.

	.. versionadded:: 0.1.0

	.. versionchanged:: 0.2.0
		The cycle has 20 colors.

	Parameters
	----------
	start
		The number of colors of the cycle already used, from 0.
	color_count
		The number of colors taken.

	Returns
	-------
	list[Color | CustomColor]
		The colors following the ones already used.

	Examples
	--------
	>>> from numdaplot.plots.drawing.series_colors import take_cycle_colors
	>>> take_cycle_colors(9, 2)
	[<Color.CYAN: 10>, CustomColor(code='#aec7e8')]
	>>> take_cycle_colors(19, 2)
	[CustomColor(code='#9edae5'), <Color.BLUE: 1>]
	"""
	end = start + color_count
	default_colors = cycle(DEFAULT_CYCLE)
	taken_colors = islice(default_colors, start, end)
	color_list = list(taken_colors)

	return color_list


def warn_shared_colors(owner_name: str, parts: ColoredParts, part_count: int) -> None:
	"""
	Warn that the default cycle gives the same color to several parts of a chart or of a Plot.

	.. versionadded:: 0.2.0

	Parameters
	----------
	owner_name
		The name of the chart, such as ``ScatterChart``, or ``Plot`` for the charts drawn over each other.
	parts
		What takes one color each, such as the color groups of a ``ScatterChart``.
	part_count
		The number of parts taking a color of the cycle.

	Warns
	-----
	ReadabilityWarning
		When there are more parts than colors in the cycle.

	Examples
	--------
	>>> import warnings
	>>> from numdaplot.plots.drawing.colored_parts import ColoredParts
	>>> from numdaplot.plots.drawing.series_colors import warn_shared_colors
	>>> with warnings.catch_warnings(record=True) as caught_warnings:
	... 	warnings.simplefilter("always")
	... 	warn_shared_colors("ScatterChart", ColoredParts.COLOR_GROUPS, 25)
	>>> print(caught_warnings[0].message)
	A ScatterChart with 25 color groups is hard to read: 20 colors are available, so some groups share a color.
	"""
	if part_count <= CYCLE_LENGTH:
		return

	short_parts = SHORT_PART_NAMES[parts]
	message = SHARED_COLORS_MESSAGE.format(
		owner_name=owner_name,
		part_count=part_count,
		parts=parts.value,
		color_count=CYCLE_LENGTH,
		short_parts=short_parts,
	)
	warnings.warn(message, ReadabilityWarning, skip_file_prefixes=INTERNAL_FILES)
