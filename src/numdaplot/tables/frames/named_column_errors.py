"""
Name of the Table column in the errors about its values raised by a block.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.column_value_error import ColumnValueError
from numdaplot.errors.error_translation import ErrorTranslation
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.tables.frames.column import Column

NAMED_ERROR_TYPES = (IncompatibleTypesError, ColumnValueError)


class NamedColumnErrors(ErrorTranslation):
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

	def translate_error(self, error: BaseException) -> None:
		"""
		Name the column in an error of the block about its values, which then goes on.

		.. versionadded:: 0.2.0

		Parameters
		----------
		error
			The error raised by the block.
		"""
		column_name = self.column.name
		if column_name is None:
			return

		if isinstance(error, NAMED_ERROR_TYPES):
			column_text = str(column_name)
			error.name_column(column_text)
