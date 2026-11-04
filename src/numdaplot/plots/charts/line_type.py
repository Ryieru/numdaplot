"""
How the lines of a LineChart are drawn.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class LineType(Enum):
	"""
	How the lines of a ``LineChart`` are drawn.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(line=ndp.LineType.DASHED)
	>>> plot = ndp.plot_line(prices, chart)
	>>> plot.show()
	"""

	SOLID = auto()
	"""
	A continuous line. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(line=ndp.LineType.SOLID)
	>>> plot = ndp.plot_line(prices, chart)
	>>> plot.show()
	"""

	DASHED = auto()
	"""
	A line of dashes.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(line=ndp.LineType.DASHED)
	>>> plot = ndp.plot_line(prices, chart)
	>>> plot.show()
	"""

	DOTTED = auto()
	"""
	A line of dots.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(line=ndp.LineType.DOTTED)
	>>> plot = ndp.plot_line(prices, chart)
	>>> plot.show()
	"""

	DASH_DOT = auto()
	"""
	A line of dashes and dots in turn.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(line=ndp.LineType.DASH_DOT)
	>>> plot = ndp.plot_line(prices, chart)
	>>> plot.show()
	"""
