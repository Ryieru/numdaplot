"""
Functional tests of the settings checked when they are created: column names, positions, ranges and statistics.

.. versionadded:: 0.1.0
"""

from collections.abc import Callable

import pytest

import numdaplot as ndp

SUM = ndp.Sum()
EMPTY_NAME_CASES = [
	lambda: ndp.Calculation(column="", function=SUM),
	lambda: ndp.Conversion(column="", dtype=ndp.Type.TEXT),
	lambda: ndp.SortKey(column=""),
	lambda: ndp.NameChange(old_name="", new_name="city"),
	lambda: ndp.BarChart(x=""),
	lambda: ndp.BarChart(y=[""]),
	lambda: ndp.LineChart(x=""),
	lambda: ndp.ScatterChart(color_by=""),
	lambda: ndp.BoxChart(group_by=""),
	lambda: ndp.HeatmapChart(labels=""),
	lambda: ndp.PieChart(labels="", values="sales"),
	lambda: ndp.Condition(rule=ndp.IsMissing(), columns=[""]),
	lambda: ndp.ColumnChoice(columns=[""]),
	lambda: ndp.Deduplication(columns=[""]),
	lambda: ndp.MissingDrop(columns=[""]),
	lambda: ndp.Description(columns=[""]),
	lambda: ndp.Aggregation(calculations=[ndp.Calculation(column="price", function=SUM)], group_by=[""]),
	lambda: ndp.Region(columns=[""]),
]
EXPECTED_EMPTY_NAME_MESSAGE = "Expected a column name as a non-empty text, got ''."
EXPECTED_CELL_MESSAGE = "Expected a whole position of at least 0, got -1."
EXPECTED_INDEX_MESSAGE = "Index position expects an int, got 1.5."
EXPECTED_RANGE_MESSAGE = "Expected a step going from start to stop, got step 1 from 5 to 1."
EXPECTED_STATISTIC_MESSAGE = "The statistic Sum() appears more than once."
EXPECTED_SEED_MESSAGE = "Side.START does not accept seed."


@pytest.mark.parametrize("create", EMPTY_NAME_CASES)
def test_an_empty_column_name_is_refused_when_the_setting_is_created(create: Callable[[], object]) -> None:
	"""
	Check that every setting naming a column refuses an empty name at once.

	.. versionadded:: 0.1.0

	Parameters
	----------
	create
		Creates the setting with an empty name.
	"""
	with pytest.raises(ndp.InvalidColumnNameError) as error_info:
		create()

	message = str(error_info.value)
	assert message == EXPECTED_EMPTY_NAME_MESSAGE


def test_a_negative_cell_is_refused_before_it_is_placed() -> None:
	"""
	Check that Cell refuses a negative row when it is created.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidPositionError) as error_info:
		ndp.Cell(row=-1, column=0)

	message = str(error_info.value)
	assert message == EXPECTED_CELL_MESSAGE


def test_a_decimal_index_is_refused_before_it_is_used() -> None:
	"""
	Check that Index refuses a decimal position when it is created.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidTypeError) as error_info:
		# The type checker refuses this call too, as it does in the editor of a user.
		ndp.Index(1.5)  # pyright: ignore[reportArgumentType]

	message = str(error_info.value)
	assert message == EXPECTED_INDEX_MESSAGE


def test_a_range_going_away_from_its_stop_is_refused() -> None:
	"""
	Check that a positive step from 5 to 1 is refused instead of giving nothing.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidStepError) as error_info:
		ndp.Range(start=5, stop=1)

	message = str(error_info.value)
	assert message == EXPECTED_RANGE_MESSAGE


def test_a_statistic_given_twice_to_a_description_is_refused() -> None:
	"""
	Check that Description refuses the same statistic twice.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.DuplicateStatisticError) as error_info:
		ndp.Description(functions=[SUM, ndp.Mean(), SUM])

	message = str(error_info.value)
	assert message == EXPECTED_STATISTIC_MESSAGE


def test_an_empty_list_of_region_columns_is_refused() -> None:
	"""
	Check that Region refuses an empty list of columns, as every other list of columns does.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.EmptyListError):
		ndp.Region(columns=[])


def test_a_seed_without_random_draw_is_refused() -> None:
	"""
	Check that Preview refuses a seed with the first rows, where it would do nothing.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.RefusedSettingError) as error_info:
		ndp.Preview(seed=3)

	message = str(error_info.value)
	assert message == EXPECTED_SEED_MESSAGE
