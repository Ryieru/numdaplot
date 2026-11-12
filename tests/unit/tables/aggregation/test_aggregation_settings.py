"""
Unit tests of Calculation and Aggregation.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.duplicate_column_error import RESULT_NAME_ADVICE, DuplicateColumnError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.errors.invalid_column_name_error import InvalidColumnNameError
from numdaplot.statistics.maximum import Max
from numdaplot.statistics.mean import Mean
from numdaplot.tables.aggregation.aggregation import Aggregation, require_unique_result_names
from numdaplot.tables.aggregation.calculation import Calculation, find_result_name

COLUMN_NAME = "price"
RESULT_NAME = "average_price"
AUTOMATIC_NAME = "price_mean"
EMPTY_NAME = ""
AVERAGE_PRICE = Calculation(column=COLUMN_NAME, function=Mean())
HIGHEST_PRICE = Calculation(column=COLUMN_NAME, function=Max())
GROUP_COLUMNS = ["city"]
EMPTY_GROUP_COLUMNS = list[str]()


def test_find_result_name_joins_the_column_and_the_statistic() -> None:
	"""
	Check the automatic name.

	.. versionadded:: 0.1.0
	"""
	result_name = find_result_name(AVERAGE_PRICE)

	assert result_name == AUTOMATIC_NAME


def test_find_result_name_keeps_a_given_name() -> None:
	"""
	Check that a given result name wins.

	.. versionadded:: 0.1.0
	"""
	calculation = Calculation(column=COLUMN_NAME, function=Mean(), result_name=RESULT_NAME)

	result_name = find_result_name(calculation)

	assert result_name == RESULT_NAME


def test_calculation_rejects_an_empty_result_name() -> None:
	"""
	Check that an empty result name raises InvalidColumnNameError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidColumnNameError):
		Calculation(column=COLUMN_NAME, function=Mean(), result_name=EMPTY_NAME)


def test_aggregation_gives_a_single_row_by_default() -> None:
	"""
	Check that no group is set by default.

	.. versionadded:: 0.1.0
	"""
	aggregation = Aggregation(calculations=[AVERAGE_PRICE])

	assert aggregation.group_by is None


def test_aggregation_keeps_its_own_copy_of_the_lists() -> None:
	"""
	Check that changing the given lists does not change the aggregation.

	.. versionadded:: 0.1.0
	"""
	calculations = [AVERAGE_PRICE]
	group_columns = list(GROUP_COLUMNS)
	aggregation = Aggregation(calculations=calculations, group_by=group_columns)

	calculations.clear()
	group_columns.clear()

	assert aggregation.calculations == [AVERAGE_PRICE]
	assert aggregation.group_by == GROUP_COLUMNS


def test_aggregation_rejects_no_calculation() -> None:
	"""
	Check that an empty list of calculations raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		Aggregation(calculations=[])


def test_aggregation_rejects_an_empty_list_of_groups() -> None:
	"""
	Check that an empty list of group columns raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		Aggregation(calculations=[AVERAGE_PRICE], group_by=EMPTY_GROUP_COLUMNS)


def test_aggregation_rejects_two_results_of_the_same_name() -> None:
	"""
	Check that two calculations giving price_mean raise DuplicateColumnError, advising a result name.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError) as error_info:
		Aggregation(calculations=[AVERAGE_PRICE, AVERAGE_PRICE])

	assert error_info.value.advice == RESULT_NAME_ADVICE


def test_aggregation_rejects_a_result_named_like_a_group() -> None:
	"""
	Check that a result named like a group column raises DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	city_result = Calculation(column=COLUMN_NAME, function=Max(), result_name=GROUP_COLUMNS[0])

	with pytest.raises(DuplicateColumnError):
		Aggregation(calculations=[city_result, HIGHEST_PRICE], group_by=GROUP_COLUMNS)


def test_require_unique_result_names_accepts_distinct_names() -> None:
	"""
	Check that two results of different names, apart from the group column, pass.

	.. versionadded:: 0.2.0
	"""
	require_unique_result_names([AVERAGE_PRICE, HIGHEST_PRICE], GROUP_COLUMNS)
