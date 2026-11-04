"""
Color scales of a HeatmapChart.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class ColorScale(Enum):
	"""
	Color scales of a ``HeatmapChart``, from the color of the smallest value to the color of the largest one.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> january = ndp.Array.from_list([5.5, 3.0, 8.0])
	>>> february = ndp.Array.from_list([6.0, 4.5, 9.0])
	>>> march = ndp.Array.from_list([9.5, 8.0, 11.5])
	>>> temperatures = ndp.Table.from_arrays({"city": cities, "jan": january, "feb": february, "mar": march})
	>>> chart = ndp.HeatmapChart(columns=["jan", "feb", "mar"], labels="city", scale=ndp.ColorScale.BLUES)
	>>> plot = ndp.plot_heatmap(temperatures, chart)
	>>> plot.show()
	"""

	VIRIDIS = auto()
	"""
	From dark purple for the smallest values to yellow for the largest. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> january = ndp.Array.from_list([5.5, 3.0, 8.0])
	>>> february = ndp.Array.from_list([6.0, 4.5, 9.0])
	>>> march = ndp.Array.from_list([9.5, 8.0, 11.5])
	>>> temperatures = ndp.Table.from_arrays({"city": cities, "jan": january, "feb": february, "mar": march})
	>>> chart = ndp.HeatmapChart(columns=["jan", "feb", "mar"], labels="city", scale=ndp.ColorScale.VIRIDIS)
	>>> plot = ndp.plot_heatmap(temperatures, chart)
	>>> plot.show()
	"""

	BLUES = auto()
	"""
	From white for the smallest values to dark blue for the largest.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> january = ndp.Array.from_list([5.5, 3.0, 8.0])
	>>> february = ndp.Array.from_list([6.0, 4.5, 9.0])
	>>> march = ndp.Array.from_list([9.5, 8.0, 11.5])
	>>> temperatures = ndp.Table.from_arrays({"city": cities, "jan": january, "feb": february, "mar": march})
	>>> chart = ndp.HeatmapChart(columns=["jan", "feb", "mar"], labels="city", scale=ndp.ColorScale.BLUES)
	>>> plot = ndp.plot_heatmap(temperatures, chart)
	>>> plot.show()
	"""

	REDS = auto()
	"""
	From white for the smallest values to dark red for the largest.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> january = ndp.Array.from_list([5.5, 3.0, 8.0])
	>>> february = ndp.Array.from_list([6.0, 4.5, 9.0])
	>>> march = ndp.Array.from_list([9.5, 8.0, 11.5])
	>>> temperatures = ndp.Table.from_arrays({"city": cities, "jan": january, "feb": february, "mar": march})
	>>> chart = ndp.HeatmapChart(columns=["jan", "feb", "mar"], labels="city", scale=ndp.ColorScale.REDS)
	>>> plot = ndp.plot_heatmap(temperatures, chart)
	>>> plot.show()
	"""

	RED_BLUE = auto()
	"""
	From blue for the smallest values to red for the largest, through white. When the values are on both
	sides of 0, the scale is centered on 0, so white means 0.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> january = ndp.Array.from_list([1.5, -2.0, 0.5])
	>>> february = ndp.Array.from_list([-0.5, 1.0, 2.5])
	>>> march = ndp.Array.from_list([-3.0, 0.5, 1.0])
	>>> temperatures = ndp.Table.from_arrays({"city": cities, "jan": january, "feb": february, "mar": march})
	>>> chart = ndp.HeatmapChart(columns=["jan", "feb", "mar"], labels="city", scale=ndp.ColorScale.RED_BLUE)
	>>> plot = ndp.plot_heatmap(temperatures, chart)
	>>> plot.show()
	"""
