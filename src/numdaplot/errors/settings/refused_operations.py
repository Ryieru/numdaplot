"""
The comparison operators that an Array and a Table refuse, and the error refusing them.

.. versionadded:: 0.2.0
"""

from typing import NoReturn

from numdaplot.errors.settings.refused_operation_error import RefusedOperationError

COMPARISON_OPERATION = "Comparing {owner} with {symbol}"
EQUAL_SYMBOL = "=="
NOT_EQUAL_SYMBOL = "!="
LESS_SYMBOL = "<"
LESS_OR_EQUAL_SYMBOL = "<="
GREATER_SYMBOL = ">"
GREATER_OR_EQUAL_SYMBOL = ">="


def refuse_comparison(owner: str, symbol: str, alternative: str) -> NoReturn:
	"""
	Raise the error refusing a comparison operator on an Array or a Table.

	.. versionadded:: 0.2.0

	Parameters
	----------
	owner
		The refused object with its article, such as ``"an Array"`` or ``"a Table"``.
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
	>>> from numdaplot.errors.settings.refused_operations import refuse_comparison
	>>> try:
	... 	refuse_comparison("an Array", "<", "select")
	... except ndp.RefusedOperationError as error:
	... 	print(error)
	Comparing an Array with < is not available, use select instead.
	"""
	operation = COMPARISON_OPERATION.format(owner=owner, symbol=symbol)
	raise RefusedOperationError(operation, alternative)
