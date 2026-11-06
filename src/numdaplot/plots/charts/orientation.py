"""
Direction of the bars of a BarChart.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Orientation(Enum):
	"""
	Direction of the bars of a ``BarChart``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.BarChart(x="day", y=["price", "cost"], orientation=ndp.Orientation.HORIZONTAL)
	>>> plot = ndp.Plot.bar(sales, chart)
	>>> plot.show()
	"""

	VERTICAL = auto()
	"""
	Bars rising from the horizontal axis. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.BarChart(x="day", y=["price", "cost"], orientation=ndp.Orientation.VERTICAL)
	>>> plot = ndp.Plot.bar(sales, chart)
	>>> plot.show()
	"""

	HORIZONTAL = auto()
	"""
	Bars extending from the vertical axis, which then holds the ``x`` values.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.BarChart(x="day", y=["price", "cost"], orientation=ndp.Orientation.HORIZONTAL)
	>>> plot = ndp.Plot.bar(sales, chart)
	>>> plot.show()
	"""
