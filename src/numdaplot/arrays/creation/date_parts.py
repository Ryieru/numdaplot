"""
The year, the month and the day of the dates of an Array.

.. versionadded:: 0.1.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.arrays.operations.type_requirements import require_family
from numdaplot.errors.positions.shape_mismatch_error import ShapeMismatchError
from numdaplot.types.value_family import ValueFamily

if TYPE_CHECKING:
	from numdaplot.arrays.array import Array

DATE_PARTS_OPERATION = "from_date_parts"
NUMBER_FAMILIES = frozenset({ValueFamily.NUMBER})


@dataclass(frozen=True, eq=False)
class DateParts:
	"""
	The year, the month and the day of each date, used by ``Array.from_date_parts``.

	Each part is an Array of whole numbers, as integers or as decimals such as ``3.0``, all of the same shape. The
	year is taken as written: ``25`` is the year 25.

	.. versionadded:: 0.1.0

	Parameters
	----------
	year
		The year of each date, from 1 to 9999.
	month
		The month of each date, from 1 to 12.
	day
		The day of each date, from 1 to the last day of its month.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	IncompatibleTypesError
		When a part does not hold numbers.
	ShapeMismatchError
		When the parts do not have the same shape.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> years = ndp.Array.from_list([2025, 2025])
	>>> months = ndp.Array.from_list([3, 12])
	>>> days = ndp.Array.from_list([15, 31])
	>>> ndp.Array.from_date_parts(ndp.DateParts(year=years, month=months, day=days))
	Array(['2025-03-15', '2025-12-31'], dtype=DATE)
	"""

	year: Array
	month: Array
	day: Array

	def __post_init__(self) -> None:
		"""
		Check that each part holds numbers, and that the parts have the same shape.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		IncompatibleTypesError
			When a part does not hold numbers.
		ShapeMismatchError
			When the parts do not have the same shape.
		"""
		require_field_types(self)

		year_dimensions = self.year.shape.dimensions
		for part in (self.year, self.month, self.day):
			part_values = part.to_numpy()
			require_family(part_values, NUMBER_FAMILIES, DATE_PARTS_OPERATION)
			part_dimensions = part.shape.dimensions
			if part_dimensions != year_dimensions:
				raise ShapeMismatchError(year_dimensions, part_dimensions)
