"""
Unit tests of PivotTable.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.settings.empty_list_error import EmptyListError
from numdaplot.errors.settings.refused_setting_error import RefusedSettingError
from numdaplot.errors.tables.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.tables.invalid_column_name_error import InvalidColumnNameError
from numdaplot.errors.types.invalid_type_error import InvalidTypeError
from numdaplot.statistics.sum import Sum
from numdaplot.tables.aggregation.calculation import Calculation
from numdaplot.tables.pivot.pivot_table import PivotTable

HOUR = "hour"
WEEKDAY = "weekday"
FARE = "fare"
TOTAL_FARE = Calculation(column=FARE, function=Sum())
NAMED_TOTAL = Calculation(column=FARE, function=Sum(), result_name="total")


def test_pivot_table_keeps_its_settings() -> None:
	"""
	Check that the settings are available as attributes.

	.. versionadded:: 0.1.0
	"""
	pivot = PivotTable(rows=[HOUR], columns=WEEKDAY, calculation=TOTAL_FARE)

	assert pivot.rows == [HOUR]
	assert pivot.columns == WEEKDAY
	assert pivot.calculation == TOTAL_FARE


def test_pivot_table_keeps_its_own_copy_of_the_rows() -> None:
	"""
	Check that changing the given list never changes the settings.

	.. versionadded:: 0.1.0
	"""
	rows = [HOUR]
	pivot = PivotTable(rows=rows, columns=WEEKDAY, calculation=TOTAL_FARE)

	rows.append(FARE)

	assert pivot.rows == [HOUR]


def test_pivot_table_refuses_empty_rows() -> None:
	"""
	Check that a result needs at least one row column.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		PivotTable(rows=[], columns=WEEKDAY, calculation=TOTAL_FARE)


def test_pivot_table_refuses_an_empty_column_name() -> None:
	"""
	Check the name of the column giving its values to the result columns.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidColumnNameError):
		PivotTable(rows=[HOUR], columns="", calculation=TOTAL_FARE)


def test_pivot_table_refuses_an_empty_row_name() -> None:
	"""
	Check the names of the row columns.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidColumnNameError):
		PivotTable(rows=[""], columns=WEEKDAY, calculation=TOTAL_FARE)


@pytest.mark.parametrize("rows", [[HOUR, HOUR], [WEEKDAY]])
def test_pivot_table_refuses_a_name_used_twice(rows: list[str]) -> None:
	"""
	Check that a name appears only once among the rows and the columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rows
		Row columns repeating a name.
	"""
	with pytest.raises(DuplicateColumnError):
		PivotTable(rows=rows, columns=WEEKDAY, calculation=TOTAL_FARE)


def test_pivot_table_refuses_a_result_name() -> None:
	"""
	Check that a calculation cannot name the result, each column being named after a value.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedSettingError):
		PivotTable(rows=[HOUR], columns=WEEKDAY, calculation=NAMED_TOTAL)


def test_pivot_table_refuses_rows_of_another_type() -> None:
	"""
	Check that the types of the settings are checked at creation.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidTypeError):
		PivotTable(rows=HOUR, columns=WEEKDAY, calculation=TOTAL_FARE)  # pyright: ignore[reportArgumentType]
