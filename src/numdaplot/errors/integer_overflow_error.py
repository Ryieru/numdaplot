"""
Error raised when the result of a calculation does not fit an integer type.

.. versionadded:: 0.1.0
"""

import numpy

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.types.numpy_mapping import to_numpy_dtype
from numdaplot.types.type import Type

INTEGER_OVERFLOW_MESSAGE = (
	"The operation {operation_name} gives values outside the range of {type_name}, from {lowest} to {highest}. {advice}"
)
WIDER_INTEGER_ADVICE = "Convert the values to INT64 first."
DECIMAL_ADVICE = "Convert the values to FLOAT64 first, which keeps about 16 digits."
WIDEST_INTEGER_TYPES = frozenset({Type.INT64, Type.UINT64})


class IntegerOverflowError(NumdaplotError):
	"""
	Raised when an integer result does not fit its type, which would otherwise wrap around to a wrong number.

	The message gives the range of the type and advises ``INT64`` for smaller integers, ``FLOAT64`` for ``INT64`` and
	``UINT64``, which have no wider integer type.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		The message gives the range of the type and advises ``INT64`` for smaller integers. It names the type of the
		Array when a number written before an operator does not fit it.

	Parameters
	----------
	operation_name
		The operator or the statistic, such as ``*`` or ``Sum``.
	type_name
		Name of the integer ``ndp.Type`` member that cannot hold the result.

	Attributes
	----------
	operation_name
		The operator or the statistic, such as ``*`` or ``Sum``.
	type_name
		Name of the integer ``ndp.Type`` member that cannot hold the result.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Array.from_list([2**62]) * 4
	... except ndp.IntegerOverflowError as error:
	... 	print(error)
	The operation * gives values outside the range of INT64, from -9223372036854775808 to 9223372036854775807.
	Convert the values to FLOAT64 first, which keeps about 16 digits.
	>>> small_counts = ndp.Table.from_arrays({"count": ndp.Array.from_list([1, 2])})
	>>> small_counts = small_counts.convert(ndp.TableConversion(columns=["count"], dtype=ndp.Type.UINT8))
	>>> try:
	... 	small_counts.column("count") - 5
	... except ndp.IntegerOverflowError as error:
	... 	print(error)
	The operation - gives values outside the range of UINT8, from 0 to 255. Convert the values to INT64 first.
	"""

	def __init__(self, operation_name: str, type_name: str) -> None:
		"""
		Build the error message from the operation, the type and its range, with the advice fitting the type.

		.. versionadded:: 0.1.0
		.. versionchanged:: 0.2.0
			Gives the range of the type and the advice fitting it.

		Parameters
		----------
		operation_name
			The operator or the statistic, such as ``*`` or ``Sum``.
		type_name
			Name of the integer ``ndp.Type`` member that cannot hold the result.
		"""
		integer_type = Type[type_name]
		integer_dtype = to_numpy_dtype(integer_type)
		limits = numpy.iinfo(integer_dtype)
		advice = WIDER_INTEGER_ADVICE
		if integer_type in WIDEST_INTEGER_TYPES:
			advice = DECIMAL_ADVICE

		message = INTEGER_OVERFLOW_MESSAGE.format(
			operation_name=operation_name,
			type_name=type_name,
			lowest=limits.min,
			highest=limits.max,
			advice=advice,
		)
		super().__init__(message)

		self.operation_name = operation_name
		self.type_name = type_name
