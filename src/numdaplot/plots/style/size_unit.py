"""
Units of the width and the height of a Plot.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class SizeUnit(Enum):
	"""
	Units of the width and the height of a Plot, used by ``Size``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> style = ndp.PlotStyle(size=ndp.Size(width=16, height=8, unit=ndp.SizeUnit.CENTIMETER))
	>>> plot = ndp.Plot.line(prices, style=style)
	>>> plot.show()
	"""

	INCH = auto()
	"""
	Inches, as matplotlib counts sizes. Default value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> style = ndp.PlotStyle(size=ndp.Size(width=6, height=3, unit=ndp.SizeUnit.INCH))
	>>> plot = ndp.Plot.line(prices, style=style)
	>>> plot.show()
	"""

	CENTIMETER = auto()
	"""
	Centimeters, 2.54 per inch.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> style = ndp.PlotStyle(size=ndp.Size(width=16, height=8, unit=ndp.SizeUnit.CENTIMETER))
	>>> plot = ndp.Plot.line(prices, style=style)
	>>> plot.show()
	"""

	PIXEL = auto()
	"""
	Pixels, 100 per inch, the resolution of a PNG image saved without ``ImageOptions``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> style = ndp.PlotStyle(size=ndp.Size(width=600, height=300, unit=ndp.SizeUnit.PIXEL))
	>>> plot = ndp.Plot.line(prices, style=style)
	>>> plot.show()
	"""
