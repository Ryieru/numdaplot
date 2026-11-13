"""
Change of the type of the values of an Array.

.. versionadded:: 0.2.0
"""

from typing import Self

from numdaplot.argument_checks.argument_types import checked_arguments
from numdaplot.arrays.array_data import ArrayData
from numdaplot.conversions.array_conversion import ArrayConversion
from numdaplot.conversions.converted_array import convert_array_values


class ArrayTypeChange(ArrayData):
	"""
	Change of the type of the values of an Array with ``convert``.

	.. versionadded:: 0.2.0
	"""

	@checked_arguments
	def convert(self, conversion: ArrayConversion) -> Self:
		"""
		Return the values converted to another type, in the same shape, missing values staying missing.

		.. versionadded:: 0.2.0

		Parameters
		----------
		conversion
			The new type, and the date format or the rule reading numbers as booleans. Accepted: between number
			types, between numbers and booleans, from numbers, booleans, dates, datetimes, durations and times of day
			to texts, from texts to numbers, booleans (``"true"`` or ``"false"`` in any case), dates, datetimes or
			times of day, between dates and datetimes, and from datetimes to times of day.

		Returns
		-------
		Self
			A new Array, a copy when the values already have the type.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		IncompatibleTypesError
			When the conversion is not accepted, such as a boolean to a date.
		InvalidConversionError
			When the format or the boolean rule does not apply to the conversion.
		ValueConversionError
			At the first value that cannot be stored in the new type, such as ``"abc"`` read as a number, 2.5 stored
			as an integer, 3 read as a boolean with ``ZERO_ONE``, or ``"31/02/2026"`` read as a date.
		TimeOverflowError
			When a value converted to ``DATETIME`` is outside 1677 to 2262.
		UnsupportedMissingError
			When integers or booleans would hold a missing value, which an Array cannot hold: convert integers to
			``FLOAT64`` instead.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> counts = ndp.Array.from_list([[1, 2], [3, 4]], dtype=ndp.Type.INT8)
		>>> counts.convert(ndp.ArrayConversion(dtype=ndp.Type.INT64))
		Array([[1, 2],
		       [3, 4]], dtype=INT64)
		"""
		converted_values = convert_array_values(self._values, conversion)
		converted_array = self._create(converted_values)

		return converted_array
