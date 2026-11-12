"""
Share of the values satisfying a rule statistic.

.. versionadded:: 0.2.0
"""

from dataclasses import dataclass

from numdaplot.rules.rule import Rule
from numdaplot.settings.field_types import require_field_types
from numdaplot.statistics.counted_missing import CountedMissing
from numdaplot.statistics.statistic import Statistic


@dataclass(frozen=True)
class Share(Statistic):
	"""
	Fraction of the values satisfying a rule, between 0 and 1, without the missing values by default.

	It gives the share of each group in ``aggregate`` and ``pivot_table`` without adding a column first.

	.. versionadded:: 0.2.0

	Parameters
	----------
	rule
		The ``Rule`` the counted values satisfy, such as ``ndp.Between(65, 99)``: see ``Rule`` for every rule.
	missing
		``CountedMissing.EXCLUDED`` by default to divide by the present values only, ``CountedMissing.INCLUDED`` to
		divide by every value, a missing value then counting as not satisfying the rule.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ages = ndp.Array.from_list([30.0, 70.0, None, 80.0])
	>>> ages.compute(ndp.Share(rule=ndp.Between(65, 99))).to_value()
	0.6666666666666666
	>>> ages.compute(ndp.Share(rule=ndp.Between(65, 99), missing=ndp.CountedMissing.INCLUDED)).to_value()
	0.5

	The share of each group of rows.

	>>> sexes = ndp.Array.from_list([1, 2, 2, 1])
	>>> people = ndp.Table.from_arrays({"sex": sexes, "age": ages})
	>>> senior_share = ndp.Calculation(column="age", function=ndp.Share(rule=ndp.Between(65, 99)))
	>>> people.aggregate(ndp.Aggregation(calculations=[senior_share], group_by=["sex"]))
	    sex age_share
	  INT64   FLOAT64
	0     1       0.5
	1     2       1.0
	"""

	rule: Rule
	missing: CountedMissing = CountedMissing.EXCLUDED

	def __post_init__(self) -> None:
		"""
		Check the type of every setting.

		.. versionadded:: 0.2.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		"""
		require_field_types(self)
