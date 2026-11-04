"""
Whether the slices of a PieChart show their share.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Percentages(Enum):
	"""
	Whether the slices of a ``PieChart`` show their share of the total.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> sales = ndp.Array.from_list([120.0, 80.0, 45.0])
	>>> shares = ndp.Table.from_arrays({"city": cities, "sales": sales})
	>>> chart = ndp.PieChart(labels="city", values="sales", percentages=ndp.Percentages.HIDDEN)
	>>> plot = ndp.plot_pie(shares, chart)
	>>> plot.show()
	"""

	SHOWN = auto()
	"""
	Each slice shows its share with one decimal, such as ``42.5%``. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> sales = ndp.Array.from_list([120.0, 80.0, 45.0])
	>>> shares = ndp.Table.from_arrays({"city": cities, "sales": sales})
	>>> chart = ndp.PieChart(labels="city", values="sales", percentages=ndp.Percentages.SHOWN)
	>>> plot = ndp.plot_pie(shares, chart)
	>>> plot.show()
	"""

	HIDDEN = auto()
	"""
	The slices only show their label.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> sales = ndp.Array.from_list([120.0, 80.0, 45.0])
	>>> shares = ndp.Table.from_arrays({"city": cities, "sales": sales})
	>>> chart = ndp.PieChart(labels="city", values="sales", percentages=ndp.Percentages.HIDDEN)
	>>> plot = ndp.plot_pie(shares, chart)
	>>> plot.show()
	"""
