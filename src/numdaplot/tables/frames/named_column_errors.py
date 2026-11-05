"""
Name of the Table column in the type errors of a block.

.. versionadded:: 0.1.0
"""

from types import TracebackType

from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.frames.column import Column


class NamedColumnErrors:
	"""
	Context adding the name of a Table column to the type errors raised by a block.

	.. versionadded:: 0.1.0

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
		Name the column in a type error of the block, which then goes on.

		.. versionadded:: 0.1.0

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

		if isinstance(error, IncompatibleTypesError | ValueConversionError):
			column_text = str(column_name)
			error.name_column(column_text)
