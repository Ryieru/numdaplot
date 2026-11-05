"""
Chart drawing the missing values of each column of a Table as bars.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.plots.charts.chart import Chart
from numdaplot.ratios.measure import Measure


@dataclass(frozen=True)
class MissingChart(Chart):
	"""
	Chart drawing one bar per column of a Table, as high as its missing values, used by ``plot_missing_by_column``.

	Every column has its bar, even without missing value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	measure
		``Measure.COUNT`` by default for the number of missing values of each column, ``Measure.RATIO`` for their
		share, on an axis from 0 to 1.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Nice", "Pau"])
	>>> prices = ndp.Array.from_list([12.0, None, None, 15.5])
	>>> rooms = ndp.Array.from_list([2, 3, 1, 4])
	>>> flats = ndp.Table.from_arrays({"city": cities, "price": prices, "rooms": rooms})
	>>> chart = ndp.MissingChart(measure=ndp.Measure.RATIO)
	>>> plot = ndp.plot_missing_by_column(flats, chart)
	>>> plot.show()
	"""

	measure: Measure = Measure.COUNT
