"""
Functional tests of the conversion of the values of an Array to another type.

.. versionadded:: 0.2.0
"""

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Any

import pytest

import numdaplot as ndp

DAY = date(2026, 12, 31)
MOMENT = datetime(2026, 12, 31, 15, 35)
MIDNIGHT_MOMENT = datetime(2026, 12, 31)
AFTERNOON = time(15, 35)
ONE_HOUR = timedelta(hours=1)
INTEGER_TYPES = [
	ndp.Type.INT8,
	ndp.Type.INT16,
	ndp.Type.INT32,
	ndp.Type.INT64,
	ndp.Type.UINT8,
	ndp.Type.UINT16,
	ndp.Type.UINT32,
	ndp.Type.UINT64,
]
SMALL_COUNTS = [1, 0]
EXPECTED_DECIMAL_COUNTS = [1.0, 0.0]
EXPECTED_BOOLEAN_COUNTS = [True, False]
GRID = [[1, 2], [3, 4]]
EXPECTED_DECIMAL_GRID = [[1.0, 2.0], [3.0, 4.0]]
EXPECTED_GRID_SHAPE = ndp.Shape([2, 2])
INTEGER_MISSING_MESSAGE = (
	"INT64 values cannot be missing in an Array. Convert to FLOAT64 instead, which can be missing."
)
BOOLEAN_MISSING_MESSAGE = (
	"BOOL values cannot be missing in an Array. Keep the present values first with select(ndp.IsPresent()), which "
	"gives one dimension, or convert the column of the Table, which can hold missing booleans."
)
CATEGORY_REFUSAL = "ArrayConversion does not accept Type.CATEGORY."
DAY_FIRST_TEXTS = ["31/12/2026", None]
EXPECTED_DAY_FIRST_TEXTS = ["31/12/2026", None]
COMPACT_TIME = ndp.CustomDateFormat("%H%M")
COMPACT_TIMES = ["1535", None]
NONZERO_COUNTS = [2, 0]
EXPECTED_NONZERO_BOOLEANS = [True, False]
NOTEBOOK_TARGETS = [1.0, 0.0, 1.0]
EXPECTED_NOTEBOOK_TARGETS = [1, 0, 1]


@dataclass(frozen=True)
class ConversionCase:
	"""
	Values of an Array, the type they are converted to, and the expected values.

	.. versionadded:: 0.2.0

	Parameters
	----------
	values
		The values, as given to ``Array.from_list``.
	source_type
		The type of the values.
	target_type
		The type they are converted to.
	expected_values
		The values after the conversion, as given by ``to_list``.
	"""

	values: list[Any]
	source_type: ndp.Type
	target_type: ndp.Type
	expected_values: list[Any]


ACCEPTED_CASES = [
	*[ConversionCase(SMALL_COUNTS, ndp.Type.INT64, integer_type, SMALL_COUNTS) for integer_type in INTEGER_TYPES],
	ConversionCase(SMALL_COUNTS, ndp.Type.INT64, ndp.Type.FLOAT32, EXPECTED_DECIMAL_COUNTS),
	ConversionCase(SMALL_COUNTS, ndp.Type.INT8, ndp.Type.FLOAT64, EXPECTED_DECIMAL_COUNTS),
	ConversionCase([1.0, None], ndp.Type.FLOAT64, ndp.Type.FLOAT32, [1.0, None]),
	ConversionCase([2.0, 3.0], ndp.Type.FLOAT64, ndp.Type.UINT8, [2, 3]),
	ConversionCase(SMALL_COUNTS, ndp.Type.INT64, ndp.Type.BOOL, EXPECTED_BOOLEAN_COUNTS),
	ConversionCase(EXPECTED_DECIMAL_COUNTS, ndp.Type.FLOAT64, ndp.Type.BOOL, EXPECTED_BOOLEAN_COUNTS),
	ConversionCase(EXPECTED_BOOLEAN_COUNTS, ndp.Type.BOOL, ndp.Type.INT8, SMALL_COUNTS),
	ConversionCase(EXPECTED_BOOLEAN_COUNTS, ndp.Type.BOOL, ndp.Type.FLOAT64, EXPECTED_DECIMAL_COUNTS),
	ConversionCase([12, -3], ndp.Type.INT64, ndp.Type.TEXT, ["12", "-3"]),
	ConversionCase([2.5, None], ndp.Type.FLOAT64, ndp.Type.TEXT, ["2.5", None]),
	ConversionCase(EXPECTED_BOOLEAN_COUNTS, ndp.Type.BOOL, ndp.Type.TEXT, ["True", "False"]),
	ConversionCase([DAY, None], ndp.Type.DATE, ndp.Type.TEXT, ["2026-12-31", None]),
	ConversionCase([MOMENT, None], ndp.Type.DATETIME, ndp.Type.TEXT, ["2026-12-31 15:35:00", None]),
	ConversionCase([ONE_HOUR, None], ndp.Type.DURATION, ndp.Type.TEXT, ["0 days 01:00:00", None]),
	ConversionCase([AFTERNOON, None], ndp.Type.TIME, ndp.Type.TEXT, ["15:35:00", None]),
	ConversionCase(["06000", "75001"], ndp.Type.TEXT, ndp.Type.INT32, [6000, 75001]),
	ConversionCase(["2.5", None], ndp.Type.TEXT, ndp.Type.FLOAT64, [2.5, None]),
	ConversionCase(["TRUE", " false "], ndp.Type.TEXT, ndp.Type.BOOL, EXPECTED_BOOLEAN_COUNTS),
	ConversionCase(["2026-12-31", None], ndp.Type.TEXT, ndp.Type.DATE, [DAY, None]),
	ConversionCase(["2026-12-31 15:35", "2026-12-31"], ndp.Type.TEXT, ndp.Type.DATETIME, [MOMENT, MIDNIGHT_MOMENT]),
	ConversionCase(["15:35", None], ndp.Type.TEXT, ndp.Type.TIME, [AFTERNOON, None]),
	ConversionCase([DAY, None], ndp.Type.DATE, ndp.Type.DATETIME, [MIDNIGHT_MOMENT, None]),
	ConversionCase([MOMENT, None], ndp.Type.DATETIME, ndp.Type.DATE, [DAY, None]),
	ConversionCase([MOMENT, None], ndp.Type.DATETIME, ndp.Type.TIME, [AFTERNOON, None]),
	ConversionCase(["a", None], ndp.Type.TEXT, ndp.Type.TEXT, ["a", None]),
]
REFUSED_PAIRS = [
	([1, 2], ndp.Type.INT64, ndp.Type.DATE),
	([1.5], ndp.Type.FLOAT64, ndp.Type.DATETIME),
	([1], ndp.Type.INT64, ndp.Type.DURATION),
	([1], ndp.Type.INT64, ndp.Type.TIME),
	([True], ndp.Type.BOOL, ndp.Type.DATE),
	([DAY], ndp.Type.DATE, ndp.Type.INT64),
	([DAY], ndp.Type.DATE, ndp.Type.BOOL),
	([DAY], ndp.Type.DATE, ndp.Type.TIME),
	([MOMENT], ndp.Type.DATETIME, ndp.Type.FLOAT64),
	([MOMENT], ndp.Type.DATETIME, ndp.Type.DURATION),
	([ONE_HOUR], ndp.Type.DURATION, ndp.Type.INT64),
	([ONE_HOUR], ndp.Type.DURATION, ndp.Type.DATETIME),
	([AFTERNOON], ndp.Type.TIME, ndp.Type.DATETIME),
	([AFTERNOON], ndp.Type.TIME, ndp.Type.INT64),
	(["1:00:00"], ndp.Type.TEXT, ndp.Type.DURATION),
]
LOST_VALUES = [
	([300], ndp.Type.INT64, ndp.Type.INT8),
	([-1], ndp.Type.INT64, ndp.Type.UINT8),
	([2.5], ndp.Type.FLOAT64, ndp.Type.INT64),
	(["abc"], ndp.Type.TEXT, ndp.Type.INT64),
	(["1.5"], ndp.Type.TEXT, ndp.Type.INT64),
	(["yes"], ndp.Type.TEXT, ndp.Type.BOOL),
	([3], ndp.Type.INT64, ndp.Type.BOOL),
	(["31/02/2026"], ndp.Type.TEXT, ndp.Type.DATE),
	(["25:00"], ndp.Type.TEXT, ndp.Type.TIME),
]
MISSING_CASES = [
	([1.0, None], ndp.Type.FLOAT64, ndp.Type.INT64, INTEGER_MISSING_MESSAGE),
	(["1", None], ndp.Type.TEXT, ndp.Type.INT64, INTEGER_MISSING_MESSAGE),
	([1.0, None], ndp.Type.FLOAT64, ndp.Type.BOOL, BOOLEAN_MISSING_MESSAGE),
	(["true", None], ndp.Type.TEXT, ndp.Type.BOOL, BOOLEAN_MISSING_MESSAGE),
]
MISPLACED_SETTINGS = [
	([1], ndp.Type.INT64, ndp.ArrayConversion(dtype=ndp.Type.TEXT, format=ndp.DateFormat.DAY_MONTH_YEAR)),
	(["1"], ndp.Type.TEXT, ndp.ArrayConversion(dtype=ndp.Type.BOOL, booleans=ndp.BooleanRule.NONZERO_TRUE)),
	([DAY], ndp.Type.DATE, ndp.ArrayConversion(dtype=ndp.Type.DATE, format=ndp.DateFormat.YEAR_MONTH_DAY_TIME)),
]


@pytest.mark.parametrize("case", ACCEPTED_CASES)
def test_an_accepted_conversion_gives_the_new_type_and_keeps_missing_values(case: ConversionCase) -> None:
	"""
	Check each accepted conversion: the type of the result, and its values, missing values staying missing.

	.. versionadded:: 0.2.0

	Parameters
	----------
	case
		The values, their type, the new type and the expected values.
	"""
	values = ndp.Array.from_list(case.values, dtype=case.source_type)
	expected = ndp.Array.from_list(case.expected_values, dtype=case.target_type)

	converted = values.convert(ndp.ArrayConversion(dtype=case.target_type))

	is_expected = converted.is_equal(ndp.Equality(other=expected, types=ndp.TypeMatch.STRICT))
	assert is_expected


@pytest.mark.parametrize(("values", "source_type", "target_type"), REFUSED_PAIRS)
def test_a_conversion_between_unrelated_types_is_refused(
	values: list[Any], source_type: ndp.Type, target_type: ndp.Type
) -> None:
	"""
	Check that a conversion that is not accepted raises IncompatibleTypesError.

	.. versionadded:: 0.2.0

	Parameters
	----------
	values
		The values.
	source_type
		Their type.
	target_type
		A type they cannot be converted to.
	"""
	array = ndp.Array.from_list(values, dtype=source_type)

	with pytest.raises(ndp.IncompatibleTypesError):
		array.convert(ndp.ArrayConversion(dtype=target_type))


@pytest.mark.parametrize(("values", "source_type", "target_type"), LOST_VALUES)
def test_a_value_that_does_not_fit_the_new_type_is_refused(
	values: list[Any], source_type: ndp.Type, target_type: ndp.Type
) -> None:
	"""
	Check that a value the new type cannot hold without losing information raises ValueConversionError.

	.. versionadded:: 0.2.0

	Parameters
	----------
	values
		Values holding one that does not fit.
	source_type
		Their type.
	target_type
		The new type.
	"""
	array = ndp.Array.from_list(values, dtype=source_type)

	with pytest.raises(ndp.ValueConversionError):
		array.convert(ndp.ArrayConversion(dtype=target_type))


@pytest.mark.parametrize(("values", "source_type", "target_type", "expected_message"), MISSING_CASES)
def test_missing_values_converted_to_integers_or_booleans_are_refused(
	values: list[Any], source_type: ndp.Type, target_type: ndp.Type, expected_message: str
) -> None:
	"""
	Check that integers and booleans that would hold a missing value raise UnsupportedMissingError with advice.

	.. versionadded:: 0.2.0

	Parameters
	----------
	values
		Values with a missing one.
	source_type
		Their type.
	target_type
		An integer type or ``BOOL``.
	expected_message
		The message of the error.
	"""
	array = ndp.Array.from_list(values, dtype=source_type)

	with pytest.raises(ndp.UnsupportedMissingError) as error_info:
		array.convert(ndp.ArrayConversion(dtype=target_type))

	error_text = str(error_info.value)
	assert error_text == expected_message


@pytest.mark.parametrize(("values", "source_type", "conversion"), MISPLACED_SETTINGS)
def test_a_setting_that_does_not_apply_is_refused(
	values: list[Any], source_type: ndp.Type, conversion: ndp.ArrayConversion
) -> None:
	"""
	Check that a format or a boolean rule given to another conversion raises InvalidConversionError.

	.. versionadded:: 0.2.0

	Parameters
	----------
	values
		The values.
	source_type
		Their type.
	conversion
		A conversion with a setting that does not apply to it.
	"""
	array = ndp.Array.from_list(values, dtype=source_type)

	with pytest.raises(ndp.InvalidConversionError):
		array.convert(conversion)


def test_texts_are_read_and_written_as_dates_with_a_format() -> None:
	"""
	Check that a day-first format reads texts as dates, and writes the dates back the same way.

	.. versionadded:: 0.2.0
	"""
	texts = ndp.Array.from_list(DAY_FIRST_TEXTS)
	day_first = ndp.DateFormat.DAY_MONTH_YEAR

	days = texts.convert(ndp.ArrayConversion(dtype=ndp.Type.DATE, format=day_first))
	written_days = days.convert(ndp.ArrayConversion(dtype=ndp.Type.TEXT, format=day_first))

	day_values = days.to_list()
	written_values = written_days.to_list()
	assert day_values == [DAY, None]
	assert written_values == EXPECTED_DAY_FIRST_TEXTS


def test_texts_are_read_and_written_as_times_with_a_custom_format() -> None:
	"""
	Check that a custom format of a time only reads texts as times of day, and writes them back.

	.. versionadded:: 0.2.0
	"""
	texts = ndp.Array.from_list(COMPACT_TIMES)

	times = texts.convert(ndp.ArrayConversion(dtype=ndp.Type.TIME, format=COMPACT_TIME))
	written_times = times.convert(ndp.ArrayConversion(dtype=ndp.Type.TEXT, format=COMPACT_TIME))

	time_values = times.to_list()
	written_values = written_times.to_list()
	assert time_values == [AFTERNOON, None]
	assert written_values == COMPACT_TIMES


def test_numbers_are_read_as_booleans_with_the_given_rule() -> None:
	"""
	Check that NONZERO_TRUE reads every number other than 0 as True.

	.. versionadded:: 0.2.0
	"""
	counts = ndp.Array.from_list(NONZERO_COUNTS)
	nonzero_rule = ndp.BooleanRule.NONZERO_TRUE

	flags = counts.convert(ndp.ArrayConversion(dtype=ndp.Type.BOOL, booleans=nonzero_rule))

	flag_values = flags.to_list()
	assert flag_values == EXPECTED_NONZERO_BOOLEANS


def test_a_grid_keeps_its_shape() -> None:
	"""
	Check that the values of a two-dimensional Array keep their places.

	.. versionadded:: 0.2.0
	"""
	grid = ndp.Array.from_list(GRID)

	decimal_grid = grid.convert(ndp.ArrayConversion(dtype=ndp.Type.FLOAT64))

	grid_values = decimal_grid.to_list()
	assert decimal_grid.shape == EXPECTED_GRID_SHAPE
	assert grid_values == EXPECTED_DECIMAL_GRID


def test_a_conversion_to_the_same_type_gives_an_equal_new_array() -> None:
	"""
	Check that converting to the type of the values gives another Array with the same values.

	.. versionadded:: 0.2.0
	"""
	counts = ndp.Array.from_list(SMALL_COUNTS)

	same_counts = counts.convert(ndp.ArrayConversion(dtype=ndp.Type.INT64))

	is_equal = same_counts.is_equal(ndp.Equality(other=counts))
	assert is_equal
	assert same_counts is not counts


def test_categories_are_refused() -> None:
	"""
	Check that a conversion to CATEGORY is refused when it is created.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(ndp.RefusedSettingError) as error_info:
		ndp.ArrayConversion(dtype=ndp.Type.CATEGORY)

	error_text = str(error_info.value)
	assert error_text == CATEGORY_REFUSAL


def test_decimal_targets_become_integers_once_the_missing_values_are_removed() -> None:
	"""
	Check the case of a target column read as decimals: once complete, its values are converted to integers.

	.. versionadded:: 0.2.0
	"""
	targets = ndp.Array.from_list(NOTEBOOK_TARGETS)

	integer_targets = targets.convert(ndp.ArrayConversion(dtype=ndp.Type.INT8))

	target_values = integer_targets.to_list()
	assert integer_targets.dtype == ndp.Type.INT8
	assert target_values == EXPECTED_NOTEBOOK_TARGETS
