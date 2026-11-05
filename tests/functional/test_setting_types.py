"""
Functional tests of settings given a value of the wrong kind, as a user without a type checker writes them.

.. versionadded:: 0.1.0
"""

# The tests write on purpose what the type checker refuses, as a user without a type checker would.
# pyright: reportArgumentType=false, reportCallIssue=false

from collections.abc import Callable

import pytest

import numdaplot as ndp

PRICES = ndp.Array.from_list([12.0, 15.5])
EXPECTED_REGION_MESSAGE = "Region rows expects an Index, a Range or None, got 0."
EXPECTED_PREVIEW_MESSAGE = "Preview side expects a Side such as Side.END, got 'end'."
EXPECTED_EQUAL_NONE_MESSAGE = "Equal(None) is not available, use IsMissing instead."
REFUSED_SHEET_NAME = "Sales/2026"
TEXT_FOR_LIST_CASES = [
	(lambda: ndp.BarChart(x="city", y="price"), "BarChart y expects a list such as ['price'], got 'price'."),
	(lambda: ndp.LineChart(y="price"), "LineChart y expects a list such as ['price'], got 'price'."),
	(lambda: ndp.BoxChart(columns="price"), "BoxChart columns expects a list such as ['price'], got 'price'."),
	(
		lambda: ndp.HistogramChart(columns="price"),
		"HistogramChart columns expects a list such as ['price'], got 'price'.",
	),
	(lambda: ndp.HeatmapChart(columns="price"), "HeatmapChart columns expects a list such as ['price'], got 'price'."),
	(
		lambda: ndp.Condition(rule=ndp.IsMissing(), columns="price"),
		"Condition columns expects a list such as ['price'], got 'price'.",
	),
	(lambda: ndp.ColumnChoice(columns="price"), "ColumnChoice columns expects a list such as ['price'], got 'price'."),
	(
		lambda: ndp.Deduplication(columns="price"),
		"Deduplication columns expects a list such as ['price'], got 'price'.",
	),
	(lambda: ndp.MissingDrop(columns="price"), "MissingDrop columns expects a list such as ['price'], got 'price'."),
	(lambda: ndp.Description(columns="price"), "Description columns expects a list such as ['price'], got 'price'."),
	(
		lambda: ndp.Aggregation(calculations=[ndp.Calculation(column="price", function=ndp.Sum())], group_by="city"),
		"Aggregation group_by expects a list such as ['city'], got 'city'.",
	),
	(lambda: ndp.IsIn[str]("FR"), "IsIn values expects a list such as ['FR'], got 'FR'."),
]
CLASS_CASES = [
	(lambda: PRICES.select(ndp.IsMissing), "ndp.IsMissing is a class, use ndp.IsMissing() instead."),
	(lambda: PRICES.compute(ndp.Sum), "ndp.Sum is a class, use ndp.Sum() instead."),
	(lambda: PRICES.apply(ndp.SquareRoot), "ndp.SquareRoot is a class, use ndp.SquareRoot() instead."),
	(
		lambda: ndp.Array.random(ndp.Uniform, shape=ndp.Shape((2,))),
		"ndp.Uniform is a class, use ndp.Uniform() instead.",
	),
	(lambda: ndp.plot_line(PRICES, ndp.LineChart), "ndp.LineChart is a class, use ndp.LineChart() instead."),
	(lambda: ndp.Calculation(column="price", function=ndp.Mean), "ndp.Mean is a class, use ndp.Mean() instead."),
	(lambda: ndp.Condition(rule=ndp.IsPresent), "ndp.IsPresent is a class, use ndp.IsPresent() instead."),
	(lambda: ndp.Description(functions=[ndp.Max]), "ndp.Max is a class, use ndp.Max() instead."),
]


@pytest.mark.parametrize(("create", "expected_message"), TEXT_FOR_LIST_CASES)
def test_a_text_in_place_of_a_list_shows_the_list_to_write(create: Callable[[], object], expected_message: str) -> None:
	"""
	Check that a single text given to a list setting names the list to write.

	.. versionadded:: 0.1.0

	Parameters
	----------
	create
		Creates the setting with a text.
	expected_message
		The message showing the text inside a list.
	"""
	with pytest.raises(ndp.InvalidSettingTypeError) as error_info:
		create()

	message = str(error_info.value)
	assert message == expected_message


@pytest.mark.parametrize(("use", "expected_message"), CLASS_CASES)
def test_a_class_in_place_of_an_object_shows_the_parentheses(use: Callable[[], object], expected_message: str) -> None:
	"""
	Check that a class given in place of an object names the object to write.

	.. versionadded:: 0.1.0

	Parameters
	----------
	use
		Gives a class in place of an object.
	expected_message
		The message adding the parentheses.
	"""
	with pytest.raises(ndp.InvalidSettingTypeError) as error_info:
		use()

	message = str(error_info.value)
	assert message == expected_message


def test_a_region_with_a_number_names_the_accepted_positions() -> None:
	"""
	Check that a number as the rows of a Region names Index and Range.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidSettingTypeError) as error_info:
		ndp.Region(rows=0)

	message = str(error_info.value)
	assert message == EXPECTED_REGION_MESSAGE


def test_a_preview_side_written_as_text_names_side() -> None:
	"""
	Check that a text in place of a Side names Side.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidSettingTypeError) as error_info:
		ndp.Preview(side="end")

	message = str(error_info.value)
	assert message == EXPECTED_PREVIEW_MESSAGE


def test_equal_none_points_to_is_missing() -> None:
	"""
	Check that Equal(None) names IsMissing.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.RefusedOperationError) as error_info:
		ndp.Equal(None)

	message = str(error_info.value)
	assert message == EXPECTED_EQUAL_NONE_MESSAGE


def test_a_rule_with_an_array_names_a_single_value() -> None:
	"""
	Check that an Array as the value of Greater names a single value.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidSettingTypeError):
		ndp.Greater(PRICES)


def test_an_excel_sheet_name_with_a_slash_is_refused() -> None:
	"""
	Check that a sheet name Excel refuses is refused when the settings are created.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidSheetNameError):
		ndp.ExcelOptions(sheet=REFUSED_SHEET_NAME)
