"""
Whether a BoxChart draws its outliers.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Outliers(Enum):
	"""
	Whether a ``BoxChart`` draws its outliers, the values beyond its whiskers.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0, 13.5, 16.0, 14.5, 29.0])
	>>> chart = ndp.BoxChart(outliers=ndp.Outliers.HIDDEN)
	>>> plot = ndp.Plot.box(prices, chart)
	>>> plot.show()
	"""

	SHOWN = auto()
	"""
	Each outlier is drawn as a point. Default value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0, 13.5, 16.0, 14.5, 29.0])
	>>> chart = ndp.BoxChart(outliers=ndp.Outliers.SHOWN)
	>>> plot = ndp.Plot.box(prices, chart)
	>>> plot.show()
	"""

	HIDDEN = auto()
	"""
	The outliers are not drawn. They still count in the box and the whiskers.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0, 13.5, 16.0, 14.5, 29.0])
	>>> chart = ndp.BoxChart(outliers=ndp.Outliers.HIDDEN)
	>>> plot = ndp.Plot.box(prices, chart)
	>>> plot.show()
	"""
