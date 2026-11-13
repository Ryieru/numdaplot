"""
Values of the color scales of a chart: their matplotlib names and their limits.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import matplotlib
import numpy
from matplotlib.colors import Colormap, ListedColormap
from numpy.typing import NDArray

from numdaplot.plots.charts.color_scale import ColorScale

SCALE_NAMES = {
	ColorScale.VIRIDIS: "viridis",
	ColorScale.BLUES: "Blues",
	ColorScale.REDS: "Reds",
	ColorScale.RED_BLUE: "RdBu_r",
	ColorScale.GREENS: "Greens",
	ColorScale.GRAYS: "Greys",
	ColorScale.CIVIDIS: "cividis",
}
NO_LIMITS = (None, None)
SCALES_STARTING_WHITE = frozenset({ColorScale.BLUES, ColorScale.REDS, ColorScale.GREENS, ColorScale.GRAYS})
# The start of the scale keeps a point of the smallest values visible on a white background.
VISIBLE_SCALE_START = 0.25
SCALE_END = 1.0
SCALE_COLOR_COUNT = 256


def find_scale_limits(grid: NDArray[numpy.float64], color_scale: ColorScale) -> tuple[float | None, float | None]:
	"""
	Return the values of the two ends of a color scale, centered on 0 for ``RED_BLUE`` around 0.

	.. versionadded:: 0.1.0

	Parameters
	----------
	grid
		The numbers colored, NaN where a value is missing.
	color_scale
		The color scale.

	Returns
	-------
	tuple[float | None, float | None]
		Opposite limits for ``RED_BLUE`` when the numbers are on both sides of 0, so white means 0, and None
		otherwise, for limits on the smallest and the largest number.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> import numpy
	>>> from numdaplot.plots.drawing.colors.color_scale_values import find_scale_limits
	>>> find_scale_limits(numpy.array([[-1.0, 4.0]]), ndp.ColorScale.RED_BLUE)
	(-4.0, 4.0)
	"""
	if color_scale != ColorScale.RED_BLUE:
		return NO_LIMITS

	present = ~numpy.isnan(grid)
	present_numbers = grid[present]
	present_count = len(present_numbers)
	if present_count == 0:
		return NO_LIMITS

	smallest_number = float(present_numbers.min())
	largest_number = float(present_numbers.max())
	is_below_zero = smallest_number < 0
	is_above_zero = largest_number > 0
	spans_zero = is_below_zero and is_above_zero
	if not spans_zero:
		return NO_LIMITS

	smallest_distance = abs(smallest_number)
	limit = max(smallest_distance, largest_number)

	return -limit, limit


def find_point_colors(color_scale: ColorScale) -> Colormap:
	"""
	Return the matplotlib colors of points colored along a color scale.

	A scale starting from white loses its lightest colors, so that no point disappears on a white background.

	.. versionadded:: 0.1.0

	Parameters
	----------
	color_scale
		The color scale.

	Returns
	-------
	matplotlib.colors.Colormap
		The colors, under the matplotlib name of the scale.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.drawing.colors.color_scale_values import find_point_colors
	>>> find_point_colors(ndp.ColorScale.VIRIDIS).name
	'viridis'
	>>> [float(color) < 0.9 for color in find_point_colors(ndp.ColorScale.BLUES)(0.0)[:3]]
	[True, True, False]
	"""
	scale_name = SCALE_NAMES[color_scale]
	full_colors = matplotlib.colormaps[scale_name]
	if color_scale not in SCALES_STARTING_WHITE:
		return full_colors

	kept_positions = numpy.linspace(VISIBLE_SCALE_START, SCALE_END, SCALE_COLOR_COUNT)
	# Some versions of the matplotlib stubs leave the result of a Colormap unknown.
	kept_colors = cast(Any, full_colors(kept_positions))
	visible_colors = ListedColormap(kept_colors, name=scale_name)

	return visible_colors
