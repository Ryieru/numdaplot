"""
Name of the Table column in the errors about its values raised by a block.

.. versionadded:: 0.1.0
"""

from types import TracebackType

from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.out_of_domain_error import OutOfDomainError
from numdaplot.errors.time_overflow_error import TimeOverflowError
from numdaplot.errors.unmatched_value_error import UnmatchedValueError
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.frames.column import Column

NAMED_ERROR_TYPES = (
	IncompatibleTypesError,
	OutOfDomainError,
	TimeOverflowError,
	UnmatchedValueError,
	ValueConversionError,
)


class NamedColumnErrors:
	"""
	Context adding the name of a Table column to the errors about its values raised by a block.

	These errors are ``IncompatibleTypesError``, ``OutOfDomainError``, ``TimeOverflowError``,
	``UnmatchedValueError`` and ``ValueConversionError``.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Also names the column in ``OutOfDomainError`` and ``UnmatchedValueError``.

	Parameters
	----------
	column
		The column the block works on. A column without name leaves the errors as they are.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.frames.named_column_errors import NamedColumnErrors
	>>> try:
	... 	with NamedColumnErrors(pandas.Series([1.0], name="price")):
	... 		raise ndp.IncompatibleTypesError("Contains", ["FLOAT64"])
	... except ndp.IncompatibleTypesError as error:
	... 	print(error)
	Cannot apply Contains to the FLOAT64 column 'price'.
	"""

	def __init__(self, column: Column) -> None:
		"""
		Keep the column of the block.

		.. versionadded:: 0.1.0

		Parameters
		----------
		column
			The column the block works on.
		"""
		self.column = column

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
		Name the column in an error of the block about its values, which then goes on.

		.. versionadded:: 0.1.0
		.. versionchanged:: 0.2.0
			Also names the column in ``OutOfDomainError`` and ``UnmatchedValueError``.

		Parameters
		----------
		error_type
			The type of the error raised by the block, or None.
		error
			The error raised by the block, or None.
		traceback
			Its traceback, or None.
		"""
		column_name = self.column.name
		if column_name is None:
			return

		if isinstance(error, NAMED_ERROR_TYPES):
			column_text = str(column_name)
			error.name_column(column_text)
