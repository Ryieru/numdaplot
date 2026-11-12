"""
Parts of a chart taking one color each.

.. versionadded:: 0.2.0
"""

from enum import Enum


class ColoredParts(Enum):
	"""
	The parts of a chart taking one color each, named in the warning given when colors are shared.

	.. versionadded:: 0.2.0

	Examples
	--------
	>>> import warnings
	>>> from numdaplot.plots.drawing.colored_parts import ColoredParts
	>>> from numdaplot.plots.drawing.series_colors import warn_shared_colors
	>>> with warnings.catch_warnings(record=True) as caught_warnings:
	... 	warnings.simplefilter("always")
	... 	warn_shared_colors("LineChart", ColoredParts.SERIES, 21)
	>>> print(caught_warnings[0].message)
	A LineChart with 21 series is hard to read: 20 colors are available, so some series share a color.
	"""

	SERIES = "series"
	"""
	The series of a chart, one per column drawn.

	.. versionadded:: 0.2.0

	Examples
	--------
	>>> from numdaplot.plots.drawing.colored_parts import ColoredParts
	>>> ColoredParts.SERIES.value
	'series'
	"""

	COLOR_GROUPS = "color groups"
	"""
	The groups of points of a ``ScatterChart``, one per text of its ``color_by`` column.

	.. versionadded:: 0.2.0

	Examples
	--------
	>>> from numdaplot.plots.drawing.colored_parts import ColoredParts
	>>> ColoredParts.COLOR_GROUPS.value
	'color groups'
	"""

	SLICES = "slices"
	"""
	The slices of a ``PieChart``.

	.. versionadded:: 0.2.0

	Examples
	--------
	>>> from numdaplot.plots.drawing.colored_parts import ColoredParts
	>>> ColoredParts.SLICES.value
	'slices'
	"""
