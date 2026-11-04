"""
Colors of the series of a chart.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence
from itertools import cycle, islice

from numdaplot.errors.invalid_color_count_error import InvalidColorCountError
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
)


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


def choose_series_colors(colors: Sequence[Color | CustomColor] | None, series_count: int) -> list[str]:
	"""
	Return the color code of each series of a chart.

	.. versionadded:: 0.1.0

	Parameters
	----------
	colors
		One color per series, or None for the colors of the default cycle, which starts again after ten series.
	series_count
		The number of series drawn.

	Returns
	-------
	list[str]
		One ``#rrggbb`` code per series.

	Raises
	------
	InvalidColorCountError
		When the colors are not exactly one per series.

	Examples
	--------
	>>> from numdaplot.plots.drawing.series_colors import choose_series_colors
	>>> choose_series_colors(None, 2)
	['#1f77b4', '#ff7f0e']
	"""
	chosen_colors = colors
	if chosen_colors is None:
		default_colors = cycle(DEFAULT_CYCLE)
		cycled_colors = islice(default_colors, series_count)
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
