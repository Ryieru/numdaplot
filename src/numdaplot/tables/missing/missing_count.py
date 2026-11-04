"""
Settings of the count of the missing values of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.positions.axis import Axis
from numdaplot.ratios.measure import Measure


@dataclass(frozen=True)
class MissingCount:
	"""
	How the missing values of a Table are counted, used by ``Table.count_missing``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		One count per row with ``Axis.EACH_ROW``, one per column with ``Axis.EACH_COLUMN``,
		a single count for the whole Table when omitted.
	measure
		A number of missing values by default, or with ``Measure.RATIO`` their fraction of the values counted.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> prices = ndp.Array.from_list([120.0, None, None])
	>>> table = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> table.count_missing(ndp.MissingCount(axis=ndp.Axis.EACH_COLUMN))
	column missing_count
	TEXT         INT64
	0   city             0
	1  price             2
	"""

	axis: Axis | None = None
	measure: Measure = Measure.COUNT
