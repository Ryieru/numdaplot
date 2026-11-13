"""
Python operations refused by a Table, each pointing to the numdaplot way of doing it.

.. versionadded:: 0.1.0
"""

from collections.abc import Iterator
from typing import NoReturn

from numdaplot.errors.settings.refused_operation_error import RefusedOperationError
from numdaplot.tables.table_data import TableData

COMPARISON_OPERATION = "Comparing a Table with {symbol}"
EQUALITY_ALTERNATIVE = "is_equal with ndp.Equality"
ORDER_ALTERNATIVE = "filter with a rule such as ndp.Greater"
BRACKETS_OPERATION = "Brackets on a Table"
BRACKETS_ALTERNATIVE = "column, take or filter"
ITERATION_OPERATION = "Iterating over a Table with for"
ITERATION_ALTERNATIVE = "for value in table.column(name).to_list()"
MEMBERSHIP_OPERATION = "Testing membership in a Table with in"
MEMBERSHIP_ALTERNATIVE = "filter with ndp.Equal or ndp.IsIn, or column_names"
LENGTH_OPERATION = "len of a Table"
LENGTH_ALTERNATIVE = "the row_count attribute"
TRUTH_OPERATION = "Testing a Table as a boolean"
TRUTH_ALTERNATIVE = "the row_count attribute, or is_equal"
EQUAL_SYMBOL = "=="
NOT_EQUAL_SYMBOL = "!="
LESS_SYMBOL = "<"
LESS_OR_EQUAL_SYMBOL = "<="
GREATER_SYMBOL = ">"
GREATER_OR_EQUAL_SYMBOL = ">="


class TableRefusals(TableData):
	"""
	Python operations refused by a Table, each raising ``RefusedOperationError`` with the numdaplot way of doing it.

	``==``, ``!=``, ``<``, ``<=``, ``>``, ``>=``, brackets, ``for``, ``in``, ``len`` and ``bool`` are refused.

	.. versionadded:: 0.1.0
	"""

	def __eq__(self, other: object) -> NoReturn:
		"""
		Refuse ``table == other``; use ``is_equal``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			Any value.

		Raises
		------
		RefusedOperationError
			Always.
		"""
		refuse_table_comparison(EQUAL_SYMBOL, EQUALITY_ALTERNATIVE)

	def __ne__(self, other: object) -> NoReturn:
		"""
		Refuse ``table != other``; use ``is_equal``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			Any value.

		Raises
		------
		RefusedOperationError
			Always.
		"""
		refuse_table_comparison(NOT_EQUAL_SYMBOL, EQUALITY_ALTERNATIVE)

	def __lt__(self, other: object) -> NoReturn:
		"""
		Refuse ``table < other``; use ``filter``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			Any value.

		Raises
		------
		RefusedOperationError
			Always.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> table = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5])})
		>>> try:
		... 	table < 2
		... except ndp.RefusedOperationError as error:
		... 	print(error)
		Comparing a Table with < is not available, use filter with a rule such as ndp.Greater instead.
		"""
		refuse_table_comparison(LESS_SYMBOL, ORDER_ALTERNATIVE)

	def __le__(self, other: object) -> NoReturn:
		"""
		Refuse ``table <= other``; use ``filter``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			Any value.

		Raises
		------
		RefusedOperationError
			Always.
		"""
		refuse_table_comparison(LESS_OR_EQUAL_SYMBOL, ORDER_ALTERNATIVE)

	def __gt__(self, other: object) -> NoReturn:
		"""
		Refuse ``table > other``; use ``filter``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			Any value.

		Raises
		------
		RefusedOperationError
			Always.
		"""
		refuse_table_comparison(GREATER_SYMBOL, ORDER_ALTERNATIVE)

	def __ge__(self, other: object) -> NoReturn:
		"""
		Refuse ``table >= other``; use ``filter``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			Any value.

		Raises
		------
		RefusedOperationError
			Always.
		"""
		refuse_table_comparison(GREATER_OR_EQUAL_SYMBOL, ORDER_ALTERNATIVE)

	def __getitem__(self, key: object) -> NoReturn:
		"""
		Refuse ``table[...]``; use ``column``, ``take`` or ``filter``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		key
			Any value.

		Raises
		------
		RefusedOperationError
			Always.
		"""
		raise RefusedOperationError(BRACKETS_OPERATION, BRACKETS_ALTERNATIVE)

	def __setitem__(self, key: object, value: object) -> NoReturn:
		"""
		Refuse ``table[...] = value``; use ``add_column``, which returns a new Table.

		.. versionadded:: 0.1.0

		Parameters
		----------
		key
			Any value.
		value
			Any value.

		Raises
		------
		RefusedOperationError
			Always.
		"""
		raise RefusedOperationError(BRACKETS_OPERATION, BRACKETS_ALTERNATIVE)

	def __iter__(self) -> Iterator[object]:
		"""
		Refuse ``for row in table``; iterate over the values of a column instead.

		.. versionadded:: 0.1.0

		Raises
		------
		RefusedOperationError
			Always.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> table = ndp.Table.from_arrays({"city": ndp.Array.from_list(["Paris", "Lyon"])})
		>>> for city in table.column("city").to_list():
		... 	print(city)
		Paris
		Lyon
		"""
		raise RefusedOperationError(ITERATION_OPERATION, ITERATION_ALTERNATIVE)

	def __contains__(self, value: object) -> NoReturn:
		"""
		Refuse ``value in table``; use ``filter`` with ``ndp.Equal`` or ``ndp.IsIn``, or ``column_names``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		value
			Any value.

		Raises
		------
		RefusedOperationError
			Always.
		"""
		raise RefusedOperationError(MEMBERSHIP_OPERATION, MEMBERSHIP_ALTERNATIVE)

	def __len__(self) -> NoReturn:
		"""
		Refuse ``len(table)``; read the ``row_count`` attribute instead.

		.. versionadded:: 0.1.0

		Raises
		------
		RefusedOperationError
			Always.
		"""
		raise RefusedOperationError(LENGTH_OPERATION, LENGTH_ALTERNATIVE)

	def __bool__(self) -> NoReturn:
		"""
		Refuse ``if table:`` and ``bool(table)``, whose meaning would be unclear.

		.. versionadded:: 0.1.0

		Raises
		------
		RefusedOperationError
			Always.
		"""
		raise RefusedOperationError(TRUTH_OPERATION, TRUTH_ALTERNATIVE)


def refuse_table_comparison(symbol: str, alternative: str) -> NoReturn:
	"""
	Raise the error refusing a comparison operator on a Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	symbol
		The comparison operator, such as ``"<"``.
	alternative
		What to use instead.

	Raises
	------
	RefusedOperationError
		Always.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.table_refusals import refuse_table_comparison
	>>> try:
	... 	refuse_table_comparison("==", "is_equal")
	... except ndp.RefusedOperationError as error:
	... 	print(error)
	Comparing a Table with == is not available, use is_equal instead.
	"""
	operation = COMPARISON_OPERATION.format(symbol=symbol)
	raise RefusedOperationError(operation, alternative)
