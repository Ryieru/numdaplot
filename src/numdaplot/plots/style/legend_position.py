"""
Where the legend of a Plot is placed.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class LegendPosition(Enum):
	"""
	Where the legend of a Plot is placed, used by ``PlotStyle``.

	The legend names the series, and is only drawn when a chart has several of them.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"])
	>>> style = ndp.PlotStyle(legend=ndp.LegendPosition.UPPER_LEFT)
	>>> plot = ndp.plot_line(sales, chart, style)
	>>> plot.show()
	"""

	BEST = auto()
	"""
	Inside the axes, where it hides the fewest values. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"])
	>>> style = ndp.PlotStyle(legend=ndp.LegendPosition.BEST)
	>>> plot = ndp.plot_line(sales, chart, style)
	>>> plot.show()
	"""

	UPPER_LEFT = auto()
	"""
	Inside the axes, in the upper left corner.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"])
	>>> style = ndp.PlotStyle(legend=ndp.LegendPosition.UPPER_LEFT)
	>>> plot = ndp.plot_line(sales, chart, style)
	>>> plot.show()
	"""

	UPPER_RIGHT = auto()
	"""
	Inside the axes, in the upper right corner.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"])
	>>> style = ndp.PlotStyle(legend=ndp.LegendPosition.UPPER_RIGHT)
	>>> plot = ndp.plot_line(sales, chart, style)
	>>> plot.show()
	"""

	LOWER_LEFT = auto()
	"""
	Inside the axes, in the lower left corner.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"])
	>>> style = ndp.PlotStyle(legend=ndp.LegendPosition.LOWER_LEFT)
	>>> plot = ndp.plot_line(sales, chart, style)
	>>> plot.show()
	"""

	LOWER_RIGHT = auto()
	"""
	Inside the axes, in the lower right corner.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"])
	>>> style = ndp.PlotStyle(legend=ndp.LegendPosition.LOWER_RIGHT)
	>>> plot = ndp.plot_line(sales, chart, style)
	>>> plot.show()
	"""

	OUTSIDE_RIGHT = auto()
	"""
	Outside the axes, on their right, so it never hides a value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"])
	>>> style = ndp.PlotStyle(legend=ndp.LegendPosition.OUTSIDE_RIGHT)
	>>> plot = ndp.plot_line(sales, chart, style)
	>>> plot.show()
	"""

	HIDDEN = auto()
	"""
	No legend.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"])
	>>> style = ndp.PlotStyle(legend=ndp.LegendPosition.HIDDEN)
	>>> plot = ndp.plot_line(sales, chart, style)
	>>> plot.show()
	"""
