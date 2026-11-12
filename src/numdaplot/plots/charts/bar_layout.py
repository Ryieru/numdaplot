"""
How the bars of several series share a position of a BarChart.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class BarLayout(Enum):
	"""
	How the bars of several series share a position of a ``BarChart``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.BarChart(x="day", y=["price", "cost"], layout=ndp.BarLayout.STACKED)
	>>> plot = ndp.Plot.bar(sales, chart)
	>>> plot.show()
	"""

	GROUPED = auto()
	"""
	Side by side. Default value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.BarChart(x="day", y=["price", "cost"], layout=ndp.BarLayout.GROUPED)
	>>> plot = ndp.Plot.bar(sales, chart)
	>>> plot.show()
	"""

	STACKED = auto()
	"""
	On top of each other, positive values above zero and negative values below it.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.BarChart(x="day", y=["price", "cost"], layout=ndp.BarLayout.STACKED)
	>>> plot = ndp.Plot.bar(sales, chart)
	>>> plot.show()
	"""
