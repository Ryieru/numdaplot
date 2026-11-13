"""
Unit tests of TableRefusals.

.. versionadded:: 0.1.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

from collections.abc import Callable

import pandas
import pytest

from numdaplot.errors.settings.refused_operation_error import RefusedOperationError
from numdaplot.tables.table_refusals import TableRefusals

FRAME = pandas.DataFrame({"price": [1.5]})
OTHER = 1
EXPECTED_EQUAL_MESSAGE = "Comparing a Table with == is not available, use is_equal with ndp.Equality instead."
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
	table = TableRefusals._create(FRAME)

	with pytest.raises(RefusedOperationError):
		refused_operation(table)


def test_len_points_to_row_count() -> None:
	"""
	Check that the message of len names the row_count attribute.

	.. versionadded:: 0.1.0
	"""
	table = TableRefusals._create(FRAME)

	with pytest.raises(RefusedOperationError) as error_info:
		len(table)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_LENGTH_MESSAGE


def test_equality_names_the_table_and_is_equal() -> None:
	"""
	Check that ``table == value`` names the Table and points to ``is_equal``.

	.. versionadded:: 0.2.0
	"""
	table = TableRefusals._create(FRAME)

	with pytest.raises(RefusedOperationError) as error_information:
		table.__eq__(OTHER)

	error_text = str(error_information.value)
	assert error_text == EXPECTED_EQUAL_MESSAGE
