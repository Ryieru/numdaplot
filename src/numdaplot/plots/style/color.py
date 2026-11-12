"""
Named colors of the series of a chart.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Color(Enum):
	"""
	Named colors of the series of a chart: the ten colors of the default cycle, then black.

	Write any other color with ``CustomColor``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(colors=[ndp.Color.GREEN])
	>>> plot = ndp.Plot.line(prices, chart)
	>>> plot.show()
	"""

	BLUE = auto()
	"""
	Blue, ``#1f77b4``, the first color of the default cycle.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(colors=[ndp.Color.BLUE])
	>>> plot = ndp.Plot.line(prices, chart)
	>>> plot.show()
	"""

	ORANGE = auto()
	"""
	Orange, ``#ff7f0e``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(colors=[ndp.Color.ORANGE])
	>>> plot = ndp.Plot.line(prices, chart)
	>>> plot.show()
	"""

	GREEN = auto()
	"""
	Green, ``#2ca02c``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(colors=[ndp.Color.GREEN])
	>>> plot = ndp.Plot.line(prices, chart)
	>>> plot.show()
	"""

	RED = auto()
	"""
	Red, ``#d62728``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(colors=[ndp.Color.RED])
	>>> plot = ndp.Plot.line(prices, chart)
	>>> plot.show()
	"""

	PURPLE = auto()
	"""
	Purple, ``#9467bd``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(colors=[ndp.Color.PURPLE])
	>>> plot = ndp.Plot.line(prices, chart)
	>>> plot.show()
	"""

	BROWN = auto()
	"""
	Brown, ``#8c564b``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(colors=[ndp.Color.BROWN])
	>>> plot = ndp.Plot.line(prices, chart)
	>>> plot.show()
	"""

	PINK = auto()
	"""
	Pink, ``#e377c2``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(colors=[ndp.Color.PINK])
	>>> plot = ndp.Plot.line(prices, chart)
	>>> plot.show()
	"""

	GRAY = auto()
	"""
	Gray, ``#7f7f7f``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(colors=[ndp.Color.GRAY])
	>>> plot = ndp.Plot.line(prices, chart)
	>>> plot.show()
	"""

	OLIVE = auto()
	"""
	Olive, ``#bcbd22``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(colors=[ndp.Color.OLIVE])
	>>> plot = ndp.Plot.line(prices, chart)
	>>> plot.show()
	"""

	CYAN = auto()
	"""
	Cyan, ``#17becf``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(colors=[ndp.Color.CYAN])
	>>> plot = ndp.Plot.line(prices, chart)
	>>> plot.show()
	"""

	BLACK = auto()
	"""
	Black, ``#000000``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(colors=[ndp.Color.BLACK])
	>>> plot = ndp.Plot.line(prices, chart)
	>>> plot.show()
	"""
