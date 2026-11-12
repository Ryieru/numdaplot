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
	>>> plot = ndp.Plot.line(sales, chart, style)
	>>> plot.show()
	"""

	BEST = auto()
	"""
	Inside the axes where it hides no value, otherwise past the axes on the right, as with ``OUTSIDE_RIGHT``. With an
	axis on the right, the values of both axes leave little room inside: the legend is placed as with
	``OUTSIDE_RIGHT``. Default value.

	.. versionadded:: 0.1.0

	.. versionchanged:: 0.2.0
		Goes past the axes when every place inside hides a value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"])
	>>> style = ndp.PlotStyle(legend=ndp.LegendPosition.BEST)
	>>> plot = ndp.Plot.line(sales, chart, style)
	>>> plot.show()
	"""

	UPPER_LEFT = auto()
	"""
	Inside the axes, in the upper left corner.

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
	>>> plot = ndp.Plot.line(sales, chart, style)
	>>> plot.show()
	"""

	UPPER_RIGHT = auto()
	"""
	Inside the axes, in the upper right corner.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"])
	>>> style = ndp.PlotStyle(legend=ndp.LegendPosition.UPPER_RIGHT)
	>>> plot = ndp.Plot.line(sales, chart, style)
	>>> plot.show()
	"""

	LOWER_LEFT = auto()
	"""
	Inside the axes, in the lower left corner.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"])
	>>> style = ndp.PlotStyle(legend=ndp.LegendPosition.LOWER_LEFT)
	>>> plot = ndp.Plot.line(sales, chart, style)
	>>> plot.show()
	"""

	LOWER_RIGHT = auto()
	"""
	Inside the axes, in the lower right corner.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"])
	>>> style = ndp.PlotStyle(legend=ndp.LegendPosition.LOWER_RIGHT)
	>>> plot = ndp.Plot.line(sales, chart, style)
	>>> plot.show()
	"""

	OUTSIDE_RIGHT = auto()
	"""
	Outside the axes, on their right and past an axis on the right if any, so it never hides a value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"])
	>>> style = ndp.PlotStyle(legend=ndp.LegendPosition.OUTSIDE_RIGHT)
	>>> plot = ndp.Plot.line(sales, chart, style)
	>>> plot.show()
	"""

	HIDDEN = auto()
	"""
	No legend.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"])
	>>> style = ndp.PlotStyle(legend=ndp.LegendPosition.HIDDEN)
	>>> plot = ndp.Plot.line(sales, chart, style)
	>>> plot.show()
	"""
