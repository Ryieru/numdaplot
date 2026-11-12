"""
Whether the cells of a HeatmapChart show their value.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class CellValues(Enum):
	"""
	Whether the cells of a ``HeatmapChart`` show their value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> january = ndp.Array.from_list([5.5, 3.0, 8.0])
	>>> february = ndp.Array.from_list([6.0, 4.5, 9.0])
	>>> march = ndp.Array.from_list([9.5, 8.0, 11.5])
	>>> temperatures = ndp.Table.from_arrays({"city": cities, "jan": january, "feb": february, "mar": march})
	>>> chart = ndp.HeatmapChart(columns=["jan", "feb", "mar"], labels="city", values=ndp.CellValues.SHOWN)
	>>> plot = ndp.Plot.heatmap(temperatures, chart)
	>>> plot.show()
	"""

	SHOWN = auto()
	"""
	Each cell shows its value with at most two decimals, in black or white to stay readable.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> january = ndp.Array.from_list([5.5, 3.0, 8.0])
	>>> february = ndp.Array.from_list([6.0, 4.5, 9.0])
	>>> march = ndp.Array.from_list([9.5, 8.0, 11.5])
	>>> temperatures = ndp.Table.from_arrays({"city": cities, "jan": january, "feb": february, "mar": march})
	>>> chart = ndp.HeatmapChart(columns=["jan", "feb", "mar"], labels="city", values=ndp.CellValues.SHOWN)
	>>> plot = ndp.Plot.heatmap(temperatures, chart)
	>>> plot.show()
	"""

	HIDDEN = auto()
	"""
	The cells only show their color. Default value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> january = ndp.Array.from_list([5.5, 3.0, 8.0])
	>>> february = ndp.Array.from_list([6.0, 4.5, 9.0])
	>>> march = ndp.Array.from_list([9.5, 8.0, 11.5])
	>>> temperatures = ndp.Table.from_arrays({"city": cities, "jan": january, "feb": february, "mar": march})
	>>> chart = ndp.HeatmapChart(columns=["jan", "feb", "mar"], labels="city", values=ndp.CellValues.HIDDEN)
	>>> plot = ndp.Plot.heatmap(temperatures, chart)
	>>> plot.show()
	"""
