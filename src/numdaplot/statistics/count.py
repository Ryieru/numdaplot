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

	With ``CountedMissing.INCLUDED``, it gives the number of rows of each group of an aggregation, whatever the
	column it is computed on. Use ``count_missing`` to count only the missing values.

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

	The number of rows of each group does not depend on the missing values of the column.

	>>> colors = ndp.Array.from_list(["green", "green", "yellow"])
	>>> fares = ndp.Array.from_list([7.0, None, 9.0])
	>>> trips = ndp.Table.from_arrays({"color": colors, "fare": fares})
	>>> every_row = ndp.Count(missing=ndp.CountedMissing.INCLUDED)
	>>> trip_count = ndp.Calculation(column="fare", function=every_row, result_name="trip_count")
	>>> trips.aggregate(ndp.Aggregation(calculations=[trip_count], group_by=["color"]))
	    color trip_count
	     TEXT      INT64
	0   green          2
	1  yellow          1
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
