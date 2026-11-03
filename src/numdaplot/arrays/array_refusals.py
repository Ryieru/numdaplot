"""
Python operations refused by an Array, each pointing to the numdaplot way of doing it.

.. versionadded:: 0.1.0
"""

from collections.abc import Iterator
from typing import NoReturn

from numdaplot.arrays.array_data import ArrayData
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.rules.greater import Greater
from numdaplot.rules.greater_or_equal import GreaterOrEqual
from numdaplot.rules.less import Less
from numdaplot.rules.less_or_equal import LessOrEqual

COMPARISON_OPERATION = "Comparing an Array with {symbol}"
EQUALITY_ALTERNATIVE = "is_equal with ndp.Equality, or check with ndp.Equal for each value"
ORDER_ALTERNATIVE = "select or check with a rule such as ndp.{rule_name}"
BRACKETS_OPERATION = "Brackets on an Array"
BRACKETS_ALTERNATIVE = "take, replace, select or check"
ITERATION_OPERATION = "Iterating over an Array with for"
ITERATION_ALTERNATIVE = "for value in array.to_list()"
MEMBERSHIP_OPERATION = "Testing membership in an Array with in"
MEMBERSHIP_ALTERNATIVE = "check with ndp.Equal or ndp.IsIn"
LENGTH_OPERATION = "len of an Array"
LENGTH_ALTERNATIVE = "the shape attribute"
TRUTH_OPERATION = "Testing an Array as a boolean"
TRUTH_ALTERNATIVE = "compute with ndp.Count, or is_equal"
MATRIX_PRODUCT_OPERATION = "The matrix product @ of an Array"
MATRIX_PRODUCT_ALTERNATIVE = "to_numpy and numpy"
EQUAL_SYMBOL = "=="
NOT_EQUAL_SYMBOL = "!="
LESS_SYMBOL = "<"
LESS_OR_EQUAL_SYMBOL = "<="
GREATER_SYMBOL = ">"
GREATER_OR_EQUAL_SYMBOL = ">="


class ArrayRefusals(ArrayData):
	"""
	Python operations refused by an Array, each raising ``RefusedOperationError`` with the numdaplot way of doing it.

	``==``, ``!=``, ``<``, ``<=``, ``>``, ``>=``, brackets, ``for``, ``in``, ``len``, ``bool`` and ``@`` are refused.

	.. versionadded:: 0.1.0
	"""

	def __eq__(self, other: object) -> NoReturn:
		"""
		Refuse ``array == other``; use ``is_equal`` or ``check(ndp.Equal(...))``.

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
		refuse_comparison(EQUAL_SYMBOL, EQUALITY_ALTERNATIVE)

	def __ne__(self, other: object) -> NoReturn:
		"""
		Refuse ``array != other``; use ``is_equal`` or ``check(ndp.NotEqual(...))``.

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
		refuse_comparison(NOT_EQUAL_SYMBOL, EQUALITY_ALTERNATIVE)

	def __lt__(self, other: object) -> NoReturn:
		"""
		Refuse ``array < other``; use ``select`` or ``check`` with ``ndp.Less``.

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
		>>> try:
		... 	ndp.Array.from_list([1, 2]) < 2
		... except ndp.RefusedOperationError as error:
		... 	print(error)
		Comparing an Array with < is not available, use select or check with a rule such as ndp.Less instead.
		"""
		alternative = ORDER_ALTERNATIVE.format(rule_name=Less.__name__)
		refuse_comparison(LESS_SYMBOL, alternative)

	def __le__(self, other: object) -> NoReturn:
		"""
		Refuse ``array <= other``; use ``select`` or ``check`` with ``ndp.LessOrEqual``.

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
		alternative = ORDER_ALTERNATIVE.format(rule_name=LessOrEqual.__name__)
		refuse_comparison(LESS_OR_EQUAL_SYMBOL, alternative)

	def __gt__(self, other: object) -> NoReturn:
		"""
		Refuse ``array > other``; use ``select`` or ``check`` with ``ndp.Greater``.

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
		alternative = ORDER_ALTERNATIVE.format(rule_name=Greater.__name__)
		refuse_comparison(GREATER_SYMBOL, alternative)

	def __ge__(self, other: object) -> NoReturn:
		"""
		Refuse ``array >= other``; use ``select`` or ``check`` with ``ndp.GreaterOrEqual``.

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
		alternative = ORDER_ALTERNATIVE.format(rule_name=GreaterOrEqual.__name__)
		refuse_comparison(GREATER_OR_EQUAL_SYMBOL, alternative)

	def __getitem__(self, key: object) -> NoReturn:
		"""
		Refuse ``array[...]``; use ``take``, ``select`` or ``check``.

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
		Refuse ``array[...] = value``; use ``replace``, which returns a new Array.

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
		Refuse ``for value in array``; iterate over ``array.to_list()`` instead.

		.. versionadded:: 0.1.0

		Raises
		------
		RefusedOperationError
			Always.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> for price in ndp.Array.from_list([10, 20]).to_list():
		... 	print(price)
		10
		20
		"""
		raise RefusedOperationError(ITERATION_OPERATION, ITERATION_ALTERNATIVE)

	def __contains__(self, value: object) -> NoReturn:
		"""
		Refuse ``value in array``; use ``check`` with ``ndp.Equal`` or ``ndp.IsIn``.

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
		Refuse ``len(array)``; read the ``shape`` attribute instead.

		.. versionadded:: 0.1.0

		Raises
		------
		RefusedOperationError
			Always.
		"""
		raise RefusedOperationError(LENGTH_OPERATION, LENGTH_ALTERNATIVE)

	def __bool__(self) -> NoReturn:
		"""
		Refuse ``if array:`` and ``bool(array)``, whose meaning would be unclear.

		.. versionadded:: 0.1.0

		Raises
		------
		RefusedOperationError
			Always.
		"""
		raise RefusedOperationError(TRUTH_OPERATION, TRUTH_ALTERNATIVE)

	def __matmul__(self, other: object) -> NoReturn:
		"""
		Refuse ``array @ other``; numdaplot has no linear algebra.

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
		raise RefusedOperationError(MATRIX_PRODUCT_OPERATION, MATRIX_PRODUCT_ALTERNATIVE)

	def __rmatmul__(self, other: object) -> NoReturn:
		"""
		Refuse ``other @ array``; numdaplot has no linear algebra.

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
		raise RefusedOperationError(MATRIX_PRODUCT_OPERATION, MATRIX_PRODUCT_ALTERNATIVE)


def refuse_comparison(symbol: str, alternative: str) -> NoReturn:
	"""
	Raise the error refusing a comparison operator.

	.. versionadded:: 0.1.0

	Parameters
	----------
	symbol
		The comparison operator, such as ``<``.
	alternative
		What to use instead.

	Raises
	------
	RefusedOperationError
		Always.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.array_refusals import refuse_comparison
	>>> try:
	... 	refuse_comparison("<", "select")
	... except ndp.RefusedOperationError as error:
	... 	print(error)
	Comparing an Array with < is not available, use select instead.
	"""
	operation = COMPARISON_OPERATION.format(symbol=symbol)
	raise RefusedOperationError(operation, alternative)
