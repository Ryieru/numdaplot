"""
Number of values statistic.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.settings.field_types import require_field_types
from numdaplot.statistics.counted_missing import CountedMissing
from numdaplot.statistics.statistic import Statistic


@dataclass(frozen=True)
class Count(Statistic):
	"""
	Number of values, without the missing ones by default.

	Use ``count_missing`` to count only the missing values, and the ``row_count`` of an ``Aggregation`` to count the
	rows of each group.

	.. versionadded:: 0.1.0

	Parameters
	----------
	missing
		``CountedMissing.EXCLUDED`` by default to count only the present values, ``CountedMissing.INCLUDED`` to count
		every value.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> answers = ndp.Array.from_list([4.0, None, 2.0])
	>>> answers.compute(ndp.Count()).to_value()
	2
	>>> answers.compute(ndp.Count(missing=ndp.CountedMissing.INCLUDED)).to_value()
	3
	"""

	missing: CountedMissing = CountedMissing.EXCLUDED

	def __post_init__(self) -> None:
		"""
		Check the type of the setting.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		"""
		require_field_types(self)
