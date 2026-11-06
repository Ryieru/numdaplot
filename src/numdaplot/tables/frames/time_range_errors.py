"""
Refusal of the dates and durations pandas cannot store in a Table column.

.. versionadded:: 0.1.0
"""

from types import TracebackType

import pandas

from numdaplot.data_types.type import Type
from numdaplot.errors.time_overflow_error import TimeOverflowError


class TimeRangeErrors:
	"""
	Context giving the out of range errors of pandas in a block as ``TimeOverflowError``, naming the column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operation_name
		The operation shown in the message.
	column_name
		The name of the column the block works on.

	Examples
	--------
	>>> import numpy
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.frames.time_range_errors import TimeRangeErrors
	>>> far_moments = pandas.Series(numpy.array(["3000-01-01"], dtype="datetime64[s]"))
	>>> try:
	... 	with TimeRangeErrors("from_arrays", "day"):
	... 		far_moments.astype("datetime64[ns]")
	... except ndp.TimeOverflowError as error:
	... 	print(error)
	The operation from_arrays gives values of the column 'day' outside the range of DATETIME, from 1677 to 2262.
	"""

	def __init__(self, operation_name: str, column_name: str) -> None:
		"""
		Keep the operation and the column of the block.

		.. versionadded:: 0.1.0

		Parameters
		----------
		operation_name
			The operation shown in the message.
		column_name
			The name of the column the block works on.
		"""
		self.operation_name = operation_name
		self.column_name = column_name

	def __enter__(self) -> None:
		"""
		Start the block.

		.. versionadded:: 0.1.0
		"""

	def __exit__(
		self,
		error_type: type[BaseException] | None,
		error: BaseException | None,
		traceback: TracebackType | None,
	) -> None:
		"""
		Replace an out of range error of pandas raised by the block.

		.. versionadded:: 0.1.0

		Parameters
		----------
		error_type
			The type of the error raised by the block, or None.
		error
			The error raised by the block, or None.
		traceback
			Its traceback, or None.

		Raises
		------
		TimeOverflowError
			When the block raised ``OutOfBoundsDatetime`` or ``OutOfBoundsTimedelta``.
		"""
		if isinstance(error, pandas.errors.OutOfBoundsDatetime):
			self.raise_overflow(Type.DATETIME, error)

		if isinstance(error, pandas.errors.OutOfBoundsTimedelta):
			self.raise_overflow(Type.DURATION, error)

	def raise_overflow(self, data_type: Type, error: BaseException) -> None:
		"""
		Raise the error of a value out of the range of a type.

		.. versionadded:: 0.1.0

		Parameters
		----------
		data_type
			The type that cannot hold the value.
		error
			The error of pandas.

		Raises
		------
		TimeOverflowError
			Always.
		"""
		overflow_error = TimeOverflowError(self.operation_name, data_type.name)
		overflow_error.name_column(self.column_name)
		raise overflow_error from error
