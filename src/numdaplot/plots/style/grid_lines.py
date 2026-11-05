"""
Whether a Plot draws grid lines behind its values.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class GridLines(Enum):
	"""
	Whether a Plot draws light grid lines behind its values, used by ``Style``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> style = ndp.Style(grid_lines=ndp.GridLines.HIDDEN)
	>>> plot = ndp.plot_line(prices, style=style)
	>>> plot.show()
	"""

	SHOWN = auto()
	"""
	Light grid lines at each tick of the axes. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> style = ndp.Style(grid_lines=ndp.GridLines.SHOWN)
	>>> plot = ndp.plot_line(prices, style=style)
	>>> plot.show()
	"""

	HIDDEN = auto()
	"""
	No grid lines.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> style = ndp.Style(grid_lines=ndp.GridLines.HIDDEN)
	>>> plot = ndp.plot_line(prices, style=style)
	>>> plot.show()
	"""
