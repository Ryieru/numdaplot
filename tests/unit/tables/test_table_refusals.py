"""
Unit tests of TableRefusals.

.. versionadded:: 0.1.0
"""

from collections.abc import Callable

import pandas
import pytest

from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.tables.table_refusals import TableRefusals, refuse_table_comparison

FRAME = pandas.DataFrame({"price": [1.5]})
OTHER = 1
EQUAL_SYMBOL = "=="
ALTERNATIVE = "is_equal"
EXPECTED_COMPARISON_MESSAGE = "Comparing a Table with == is not available, use is_equal instead."
EXPECTED_LENGTH_MESSAGE = "len of a Table is not available, use the row_count attribute instead."
type RefusedOperation = Callable[[TableRefusals], object]
REFUSED_OPERATIONS = list[RefusedOperation](
	[
		lambda table: table == OTHER,
		lambda table: table != OTHER,
		lambda table: table < OTHER,
		lambda table: table <= OTHER,
		lambda table: table > OTHER,
		lambda table: table >= OTHER,
		lambda table: table["price"],
		lambda table: table.__setitem__("price", OTHER),
		lambda table: list(table),
		lambda table: OTHER in table,
		lambda table: len(table),
		lambda table: bool(table),
	]
)


@pytest.mark.parametrize("refused_operation", REFUSED_OPERATIONS)
def test_table_refusals_refuse_each_python_operation(refused_operation: RefusedOperation) -> None:
	"""
	Check that each refused Python operation raises RefusedOperationError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	refused_operation
		A function applying one refused operation to a Table.
	"""
	table = TableRefusals(FRAME)

	with pytest.raises(RefusedOperationError):
		refused_operation(table)


def test_len_points_to_row_count() -> None:
	"""
	Check that the message of len names the row_count attribute.

	.. versionadded:: 0.1.0
	"""
	table = TableRefusals(FRAME)

	with pytest.raises(RefusedOperationError) as error_info:
		len(table)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_LENGTH_MESSAGE


def test_refuse_table_comparison_names_the_operator_and_the_alternative() -> None:
	"""
	Check the message of a refused comparison.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedOperationError) as error_info:
		refuse_table_comparison(EQUAL_SYMBOL, ALTERNATIVE)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_COMPARISON_MESSAGE
