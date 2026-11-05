"""
Settings of the count of the missing values of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.ratios.measure import Measure


@dataclass(frozen=True)
class MissingCount:
	"""
	How the missing values of a Table are counted, used by ``Table.count_missing``.

	The axis, for each row or each column, is given to ``Table.count_missing`` itself.

	.. versionadded:: 0.1.0

	Parameters
	----------
	measure
		A number of missing values by default, or with ``Measure.RATIO`` their fraction of the values counted.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> prices = ndp.Array.from_list([120.0, None, None])
	>>> table = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> table.count_missing(ndp.MissingCount(measure=ndp.Measure.RATIO), axis=ndp.Axis.EACH_COLUMN)
	  column missing_ratio
	    TEXT       FLOAT64
	0   city      0.000000
	1  price      0.666667
	"""

	measure: Measure = Measure.COUNT
