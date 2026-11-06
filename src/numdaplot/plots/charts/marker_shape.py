"""
Shapes drawn at the values of a chart.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class MarkerShape(Enum):
	"""
	Shapes drawn at the values of a ``LineChart`` or a ``ScatterChart``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> surfaces = ndp.Array.from_list([30.0, 45.0, 60.0, 80.0])
	>>> prices = ndp.Array.from_list([150.0, 210.0, 260.0, 330.0])
	>>> flats = ndp.Table.from_arrays({"surface": surfaces, "price": prices})
	>>> chart = ndp.ScatterChart(x="surface", y="price", marker=ndp.MarkerShape.SQUARE)
	>>> plot = ndp.Plot.scatter(flats, chart)
	>>> plot.show()
	"""

	NONE = auto()
	"""
	No marker, only the line. Default value of ``LineChart``, refused by ``ScatterChart``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> chart = ndp.LineChart(marker=ndp.MarkerShape.NONE)
	>>> plot = ndp.Plot.line(prices, chart)
	>>> plot.show()
	"""

	CIRCLE = auto()
	"""
	A disc. Default value of ``ScatterChart``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> surfaces = ndp.Array.from_list([30.0, 45.0, 60.0, 80.0])
	>>> prices = ndp.Array.from_list([150.0, 210.0, 260.0, 330.0])
	>>> flats = ndp.Table.from_arrays({"surface": surfaces, "price": prices})
	>>> chart = ndp.ScatterChart(x="surface", y="price", marker=ndp.MarkerShape.CIRCLE)
	>>> plot = ndp.Plot.scatter(flats, chart)
	>>> plot.show()
	"""

	SQUARE = auto()
	"""
	A square.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> surfaces = ndp.Array.from_list([30.0, 45.0, 60.0, 80.0])
	>>> prices = ndp.Array.from_list([150.0, 210.0, 260.0, 330.0])
	>>> flats = ndp.Table.from_arrays({"surface": surfaces, "price": prices})
	>>> chart = ndp.ScatterChart(x="surface", y="price", marker=ndp.MarkerShape.SQUARE)
	>>> plot = ndp.Plot.scatter(flats, chart)
	>>> plot.show()
	"""

	TRIANGLE = auto()
	"""
	A triangle pointing up.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> surfaces = ndp.Array.from_list([30.0, 45.0, 60.0, 80.0])
	>>> prices = ndp.Array.from_list([150.0, 210.0, 260.0, 330.0])
	>>> flats = ndp.Table.from_arrays({"surface": surfaces, "price": prices})
	>>> chart = ndp.ScatterChart(x="surface", y="price", marker=ndp.MarkerShape.TRIANGLE)
	>>> plot = ndp.Plot.scatter(flats, chart)
	>>> plot.show()
	"""

	CROSS = auto()
	"""
	A cross made of two diagonal strokes.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> surfaces = ndp.Array.from_list([30.0, 45.0, 60.0, 80.0])
	>>> prices = ndp.Array.from_list([150.0, 210.0, 260.0, 330.0])
	>>> flats = ndp.Table.from_arrays({"surface": surfaces, "price": prices})
	>>> chart = ndp.ScatterChart(x="surface", y="price", marker=ndp.MarkerShape.CROSS)
	>>> plot = ndp.Plot.scatter(flats, chart)
	>>> plot.show()
	"""

	DIAMOND = auto()
	"""
	A diamond.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> surfaces = ndp.Array.from_list([30.0, 45.0, 60.0, 80.0])
	>>> prices = ndp.Array.from_list([150.0, 210.0, 260.0, 330.0])
	>>> flats = ndp.Table.from_arrays({"surface": surfaces, "price": prices})
	>>> chart = ndp.ScatterChart(x="surface", y="price", marker=ndp.MarkerShape.DIAMOND)
	>>> plot = ndp.Plot.scatter(flats, chart)
	>>> plot.show()
	"""
