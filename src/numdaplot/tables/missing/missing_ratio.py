"""
A ratio of missing values from which a row or a column is removed.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.measures.fraction import require_fraction
from numdaplot.tables.missing.ratio_comparison import RatioComparison


@dataclass(frozen=True)
class MissingRatio:
	"""
	A ratio of missing values from which a row or a column is removed, used by ``MissingDrop``.

	The ratio of a row is its missing values divided by its number of values, and the same for a column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	ratio
		The threshold, a fraction between 0 and 1: ``0.3`` for 30 %.
	comparison
		Whether a ratio equal to the threshold is enough, ``RatioComparison.AT_LEAST`` by default, or the ratio must be
		above it, ``RatioComparison.ABOVE``.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidFractionError
		When ``ratio`` is lower than 0, greater than 1 or NaN.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([120.0, None, 80.0, None])
	>>> stocks = ndp.Array.from_list([3.0, 5.0, None, 2.0])
	>>> table = ndp.Table.from_arrays({"price": prices, "stock": stocks})
	>>> table.drop_missing(ndp.MissingDrop(rule=ndp.MissingRatio(0.4)), axis=ndp.Axis.EACH_COLUMN)
	    stock
	  FLOAT64
	0     3.0
	1     5.0
	2     NaN
	3     2.0
	"""

	ratio: float
	comparison: RatioComparison = RatioComparison.AT_LEAST

	def __post_init__(self) -> None:
		"""
		Check that the ratio is a fraction.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidFractionError
			When ``ratio`` is lower than 0, greater than 1 or NaN.
		"""
		require_field_types(self)

		require_fraction(self.ratio)
