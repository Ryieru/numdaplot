"""
Quantile statistic.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.ratios.fraction import require_fraction
from numdaplot.settings.field_types import require_field_types
from numdaplot.statistics.statistic import Statistic


@dataclass(frozen=True)
class Quantile(Statistic):
	"""
	Value below which a given fraction of the values lies.

	``Quantile(0.9)`` on salaries gives the salary below which 90 % of people are,
	and ``Quantile(0.5)`` is the median. Missing values are ignored.

	.. versionadded:: 0.1.0

	Parameters
	----------
	fraction
		Fraction of the values that lie below the result, between 0 and 1 included.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidFractionError
		When ``fraction`` is lower than 0, greater than 1 or NaN.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> salaries = ndp.Array.from_list([1000, 2000, 3000, 4000, 5000])
	>>> salaries.compute(ndp.Quantile(0.9)).to_value()
	4600.0
	"""

	fraction: float

	def __post_init__(self) -> None:
		"""
		Check that the fraction is between 0 and 1.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidFractionError
			When ``fraction`` is lower than 0, greater than 1 or NaN.
		"""
		require_field_types(self)

		require_fraction(self.fraction)
