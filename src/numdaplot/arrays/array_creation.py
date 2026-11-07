"""
Ways to create an Array.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence
from typing import Any, Self

import numpy.typing

from numdaplot.arrays.array_data import ArrayData
from numdaplot.arrays.creation.date_parts import DateParts
from numdaplot.arrays.creation.date_parts_values import build_dates
from numdaplot.arrays.creation.filled_values import build_filled_values
from numdaplot.arrays.creation.list_conversion import convert_list
from numdaplot.arrays.creation.normal import Normal
from numdaplot.arrays.creation.numpy_conversion import copy_numpy_values
from numdaplot.arrays.creation.random_integers import RandomIntegers
from numdaplot.arrays.creation.random_values import draw_random_values
from numdaplot.arrays.creation.range_values import compute_range_values
from numdaplot.arrays.creation.spacing import Spacing
from numdaplot.arrays.creation.spacing_values import compute_spacing_values
from numdaplot.arrays.creation.uniform import Uniform
from numdaplot.arrays.shape import Shape
from numdaplot.data_types.type import Type
from numdaplot.positions.range import Range
from numdaplot.rules.rule_values import ScalarValue
from numdaplot.settings.argument_types import checked_arguments

type ListValue = ScalarValue | None
"""
A single value of a list given to ``Array.from_list``: a ``ScalarValue``, or ``None`` for a missing value.

It is a name used by the documentation and the annotations, not an object to create: pass the value itself,
such as ``10``, ``"Paris"`` or ``None``.

.. versionadded:: 0.1.0

Examples
--------
>>> import numdaplot as ndp
>>> ndp.Array.from_list([1.5, None])
Array([1.5, nan], dtype=FLOAT64)
"""

type NestedValues = Sequence[ListValue] | Sequence[NestedValues]
"""
A list of ``ListValue``, or a list of lists nested to any depth, as ``Array.from_list`` reads it.

It is a name used by the documentation and the annotations, not an object to create: pass the value itself,
such as ``[1, 2, 3]``, ``["Paris", "Lyon"]`` or ``[[1, 2], [3, 4]]``.

.. versionadded:: 0.1.0

Examples
--------
>>> import numdaplot as ndp
>>> ndp.Array.from_list([[1, 2], [3, 4]]).shape
Shape(dimensions=[2, 2])
"""


class ArrayCreation(ArrayData):
	"""
	Ways to create an Array.

	From a list, from numpy, filled with one value, from a range, from a spacing, or drawn at random.

	.. versionadded:: 0.1.0
	"""

	@classmethod
	@checked_arguments
	def from_list(cls, values: NestedValues, dtype: Type | None = None) -> Self:
		"""
		Create an Array from a Python list, or from nested lists for several dimensions.

		The type is guessed when omitted: integers give ``INT64``, decimals or a mix of integers and
		decimals give ``FLOAT64``, then ``BOOL``, ``TEXT``, ``DATE``, ``DATETIME`` and ``DURATION``.
		``None`` is a missing value, only accepted for decimals, texts, dates, datetimes and durations.

		.. versionadded:: 0.1.0

		Parameters
		----------
		values
			The values, a ``NestedValues`` such as ``[1, 2, 3]``, ``["Paris", None]`` or ``[[1, 2], [3, 4]]``.
			Nested lists must form a regular block.
		dtype
			The type to store the values as, guessed from the values when omitted. Required when no value is present.

		Returns
		-------
		Self
			A new Array.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		IrregularListError
			When nested lists do not form a regular block.
		IncompatibleTypesError
			When the values mix several kinds of types, such as numbers and texts.
		MissingTypeError
			When ``dtype`` is omitted and no value is present.
		UnsupportedMissingError
			When a value is missing and the type cannot hold missing values.
		ValueConversionError
			When the values cannot be stored as ``dtype`` without losing information.
		TimeOverflowError
			When a datetime is outside 1677 to 2262, or a duration beyond about 292 years.
		UnsupportedTypeError
			When a value has no numdaplot type, or ``dtype`` is ``CATEGORY``.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Array.from_list([[1, 2], [3, None]], dtype=ndp.Type.FLOAT64)
		Array([[ 1.,  2.],
		       [ 3., nan]], dtype=FLOAT64)
		"""
		value_list = list[object](values)
		converted_values = convert_list(value_list, dtype)
		created_array = cls._create(converted_values)

		return created_array

	@classmethod
	@checked_arguments
	def from_numpy(cls, values: numpy.typing.NDArray[Any]) -> Self:
		"""
		Create an Array from a copy of a numpy array; changing the numpy array never changes the Array.

		.. versionadded:: 0.1.0

		Parameters
		----------
		values
			The numpy array. Texts may mark their missing values with any marker of ``StringDType``.

		Returns
		-------
		Self
			A new Array.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		UnsupportedTypeError
			When numdaplot has no equivalent type, for example complex numbers or Python objects.

		Examples
		--------
		>>> import numpy
		>>> import numdaplot as ndp
		>>> ndp.Array.from_numpy(numpy.array([1.5, 2.5]))
		Array([1.5, 2.5], dtype=FLOAT64)
		"""
		copied_values = copy_numpy_values(values)
		created_array = cls._create(copied_values)

		return created_array

	@classmethod
	@checked_arguments
	def filled(cls, shape: Shape, value: ScalarValue, dtype: Type | None = None) -> Self:
		"""
		Create an Array of a shape, with the same value everywhere.

		.. versionadded:: 0.1.0

		Parameters
		----------
		shape
			The shape of the Array.
		value
			The repeated value, a ``ScalarValue`` such as ``0``, ``"Paris"`` or ``True``.
		dtype
			The type to store the value as, guessed from the value when omitted.

		Returns
		-------
		Self
			A new Array.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		ValueConversionError
			When the value cannot be stored as ``dtype`` without losing information.
		TimeOverflowError
			When a datetime is outside 1677 to 2262, or a duration beyond about 292 years.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Array.filled(shape=ndp.Shape([2, 3]), value=0)
		Array([[0, 0, 0],
		       [0, 0, 0]], dtype=INT64)
		"""
		filled_values = build_filled_values(shape, value, dtype)
		created_array = cls._create(filled_values)

		return created_array

	@classmethod
	@checked_arguments
	def from_range(cls, sequence: Range) -> Self:
		"""
		Create a one-dimensional Array of the numbers of a regular sequence.

		Unlike the Python ``range``, the stop is included by default.

		.. versionadded:: 0.1.0

		Parameters
		----------
		sequence
			The start, the stop, the step and the bounds kept. ``LOW_ONLY`` keeps the start and drops
			the stop, ``HIGH_ONLY`` the opposite.

		Returns
		-------
		Self
			A new Array of integers when the start and the step are integers, of decimals otherwise.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Array.from_range(ndp.Range(start=0, stop=1, step=0.25))
		Array([0.  , 0.25, 0.5 , 0.75, 1.  ], dtype=FLOAT64)
		"""
		range_values = compute_range_values(sequence)
		created_array = cls._create(range_values)

		return created_array

	@classmethod
	@checked_arguments
	def from_date_parts(cls, parts: DateParts) -> Self:
		"""
		Create an Array of dates from their year, their month and their day, such as three columns of a file.

		.. versionadded:: 0.1.0

		Parameters
		----------
		parts
			The year, the month and the day of each date, Arrays of whole numbers of the same shape.

		Returns
		-------
		Self
			A new ``DATE`` Array of the shape of the parts. A date is missing where one of its parts is missing.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		ValueConversionError
			At the first part that is not a whole number, such as the day 3.5, then at the first year, month and day
			that form no date, such as the 31st of February, a month 13 or a year outside 1 to 9999.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> accidents = ndp.Table.from_arrays(
		... 	{
		... 		"jour": ndp.Array.from_list([14, 25]),
		... 		"mois": ndp.Array.from_list([7, 12]),
		... 		"an": ndp.Array.from_list([2025, 2025]),
		... 	}
		... )
		>>> years = accidents.column("an")
		>>> parts = ndp.DateParts(year=years, month=accidents.column("mois"), day=accidents.column("jour"))
		>>> ndp.Array.from_date_parts(parts)
		Array(['2025-07-14', '2025-12-25'], dtype=DATE)
		"""
		dates = build_dates(parts)
		created_array = cls._create(dates)

		return created_array

	@classmethod
	@checked_arguments
	def from_spacing(cls, spacing: Spacing) -> Self:
		"""
		Create a one-dimensional Array of evenly spaced decimals.

		.. versionadded:: 0.1.0

		Parameters
		----------
		spacing
			The bounds, the count of values and whether each bound is among them.

		Returns
		-------
		Self
			A new ``FLOAT64`` Array of ``count`` values.


		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Array.from_spacing(ndp.Spacing(start=0, stop=1, count=5))
		Array([0.  , 0.25, 0.5 , 0.75, 1.  ], dtype=FLOAT64)
		"""
		spacing_values = compute_spacing_values(spacing)
		created_array = cls._create(spacing_values)

		return created_array

	@classmethod
	@checked_arguments
	def random(cls, distribution: Uniform | Normal | RandomIntegers, shape: Shape, seed: int | None = None) -> Self:
		"""
		Create an Array of values drawn at random from a distribution.

		.. versionadded:: 0.1.0

		Parameters
		----------
		distribution
			The ``Distribution`` followed by the values, such as ``ndp.Uniform(low=0, high=10)``:
			see ``Distribution`` for every distribution.
		shape
			The shape of the Array.
		seed
			A number, at least 0, giving the same values at each call. Different values at each call when omitted.

		Returns
		-------
		Self
			A new ``FLOAT64`` Array for ``Uniform`` and ``Normal``, ``INT64`` for ``RandomIntegers``.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		InvalidSeedError
			When ``seed`` is lower than 0.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> dice = ndp.RandomIntegers(low=1, high=6)
		>>> ndp.Array.random(dice, shape=ndp.Shape([5]), seed=0)
		Array([6, 4, 4, 2, 2], dtype=INT64)
		"""
		random_values = draw_random_values(distribution, shape, seed)
		created_array = cls._create(random_values)

		return created_array
