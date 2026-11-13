"""
Unit tests of the application of a ValueMapping to the values of an Array.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass
from datetime import date, datetime

import numpy
import pytest

from numdaplot.arrays.creation.list_conversion import convert_list
from numdaplot.arrays.mapping.mapped_values import (
	find_flat_new_values,
	find_lookup_value,
	find_mapping_result,
	find_number_type,
	find_result_type,
	map_values,
	require_missing_supported,
	write_date_as_datetime,
	write_midnight_as_date,
)
from numdaplot.arrays.mapping.value_change import ValueChange
from numdaplot.arrays.mapping.value_mapping import ValueMapping
from numdaplot.brackets.unmatched import Unmatched
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.unmatched_value_error import UnmatchedValueError
from numdaplot.errors.unsupported_missing_error import UnsupportedMissingError
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.types.type import Type

LABELS = ValueMapping(changes=[ValueChange(1, "Homme"), ValueChange(2, "Femme")])
GRID = numpy.array([[1, 2], [2, 1]])
EXPECTED_GRID_LABELS = [["Homme", "Femme"], ["Femme", "Homme"]]
CODES_WITH_OTHER = numpy.array([1, 9])
LABELS_OR_MISSING = ValueMapping(changes=[ValueChange(1, "Homme")], others=Unmatched.MISSING)
EXPECTED_LABELS_OR_MISSING = ["Homme", None]
DECIMAL_CODES = numpy.array([1.0, numpy.nan])
DECIMAL_LABELS = ValueMapping(changes=[ValueChange(1, "one")])
EXPECTED_DECIMAL_LABELS = ["one", None]
TEXT_CODES = numpy.array(["a"])
INTEGER_RESULTS = ValueMapping(changes=[ValueChange(1, 10)], others=Unmatched.MISSING)
CHRISTMAS = date(2026, 12, 25)
DAYS = convert_list([date(2026, 1, 1), CHRISTMAS], None)
MOMENTS = convert_list([datetime(2026, 12, 25, 0, 0), datetime(2026, 12, 25, 10, 0)], None)
HOLIDAYS = ValueMapping(changes=[ValueChange(CHRISTMAS, "Noel")], others=Unmatched.MISSING)
EXPECTED_HOLIDAYS = [None, "Noel"]
EXPECTED_MIDNIGHT_HOLIDAYS = ["Noel", None]
MIDNIGHT_CHRISTMAS = datetime(2026, 12, 25, 0, 0)
MORNING_CHRISTMAS = datetime(2026, 12, 25, 10, 0)
INTEGERS_WITH_MISSING = [10, None]
BOOLEANS_WITH_MISSING = [True, None]
ONLY_MISSING_VALUES = [None, None]
EXPECTED_FLAT_GRID_LABELS = ["Homme", "Femme", "Femme", "Homme"]
TEXTS_WITH_MISSING = ["a", None]
KEPT_CODES = ValueMapping(changes=[ValueChange(1, 10)], others=Unmatched.KEEP)
EXPECTED_KEPT_CODES = [10, 9]
DECIMAL_CHANGE_AMONG_KEPT = ValueMapping(changes=[ValueChange(1, 1.5)], others=Unmatched.KEEP)
EXPECTED_WIDENED_CODES = [1.5, 9.0]
TEXT_CHANGE_AMONG_KEPT = ValueMapping(changes=[ValueChange(1, "Homme")], others=Unmatched.KEEP)
DECIMAL_ANSWERS = numpy.array([1.0, 7.0])
UNKNOWN_ANSWER_REMOVAL = ValueMapping(changes=[ValueChange(7, None)], others=Unmatched.KEEP)
EXPECTED_KEPT_ANSWER = 1.0
UNKNOWN_ANSWER_POSITION = 1
INTEGER_CHANGE = ValueMapping(changes=[ValueChange(1, 10)], others=Unmatched.MISSING)
KEPT_INTEGER_MESSAGE = (
	"INT64 values cannot be missing in an Array. Give decimal new values, such as 10.0, or convert the Array to "
	"FLOAT64 first."
)
KEPT_BOOLEAN_MESSAGE = "BOOL values cannot be missing in an Array. Convert the Array to TEXT first."
ONLY_MISSING_CHANGE = ValueMapping(changes=[ValueChange(7, None)], others=Unmatched.MISSING)
DATETIME_CHANGE_AMONG_KEPT = ValueMapping(changes=[ValueChange(CHRISTMAS, MORNING_CHRISTMAS)], others=Unmatched.KEEP)
SMALL_INTEGER_DTYPE = numpy.dtype(numpy.int8)
SMALL_CODES = numpy.array([1, 2], dtype=SMALL_INTEGER_DTYPE)
SMALL_CODE_CHANGES = ValueMapping(changes=[ValueChange(1, 100), ValueChange(2, 2)])
LARGE_CODE_CHANGES = ValueMapping(changes=[ValueChange(1, 1000), ValueChange(2, 2)])


@dataclass(frozen=True)
class NumberCase:
	"""
	The type of an Array, the type of Python numbers given to it, and the type of the result.

	.. versionadded:: 0.2.0

	Parameters
	----------
	array_type
		The number type of the Array.
	new_type
		The type of the Python numbers.
	expected_type
		The expected type of the result.
	"""

	array_type: Type
	new_type: Type
	expected_type: Type


NUMBER_CASES = [
	NumberCase(Type.INT8, Type.INT64, Type.INT8),
	NumberCase(Type.UINT16, Type.INT64, Type.UINT16),
	NumberCase(Type.FLOAT32, Type.INT64, Type.FLOAT32),
	NumberCase(Type.FLOAT32, Type.FLOAT64, Type.FLOAT32),
	NumberCase(Type.INT8, Type.FLOAT64, Type.FLOAT64),
	NumberCase(Type.INT64, Type.FLOAT64, Type.FLOAT64),
]


def test_map_values_keeps_the_shape() -> None:
	"""
	Check that a two-dimensional Array keeps its shape.

	.. versionadded:: 0.1.0
	"""
	mapped_values = map_values(GRID, LABELS)

	labels = mapped_values.tolist()
	assert labels == EXPECTED_GRID_LABELS


def test_map_values_rejects_old_values_of_another_family() -> None:
	"""
	Check that numbers as old values of a text Array raise IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError):
		map_values(TEXT_CODES, LABELS)


def test_map_values_rejects_integers_with_missing_values() -> None:
	"""
	Check that an integer result with a missing value raises UnsupportedMissingError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(UnsupportedMissingError):
		map_values(CODES_WITH_OTHER, INTEGER_RESULTS)


def test_find_flat_new_values_names_the_first_unmatched_value() -> None:
	"""
	Check that a value without change raises UnmatchedValueError by default.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(UnmatchedValueError) as error_info:
		find_flat_new_values(CODES_WITH_OTHER, LABELS)

	assert error_info.value.value == CODES_WITH_OTHER[-1]


def test_find_flat_new_values_makes_unmatched_values_missing_when_asked() -> None:
	"""
	Check Unmatched.MISSING.

	.. versionadded:: 0.1.0
	"""
	new_values = find_flat_new_values(CODES_WITH_OTHER, LABELS_OR_MISSING)

	assert new_values == EXPECTED_LABELS_OR_MISSING


def test_find_flat_new_values_keeps_missing_values_missing() -> None:
	"""
	Check that a missing decimal stays missing even with Unmatched.ERROR.

	.. versionadded:: 0.1.0
	"""
	new_values = find_flat_new_values(DECIMAL_CODES, DECIMAL_LABELS)

	assert new_values == EXPECTED_DECIMAL_LABELS


def test_find_flat_new_values_finds_dates() -> None:
	"""
	Check that a date old value finds the same date of the Array.

	.. versionadded:: 0.1.0
	"""
	new_values = find_flat_new_values(DAYS, HOLIDAYS)

	assert new_values == EXPECTED_HOLIDAYS


@pytest.mark.parametrize(
	("new_values", "new_type"), [(INTEGERS_WITH_MISSING, Type.INT64), (BOOLEANS_WITH_MISSING, Type.BOOL)]
)
def test_require_missing_supported_rejects_integers_and_booleans(new_values: list[object], new_type: Type) -> None:
	"""
	Check that integers and booleans cannot hold a missing value.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Gives ``others`` to ``require_missing_supported``.

	Parameters
	----------
	new_values
		New values with a missing one.
	new_type
		Their type.
	"""
	with pytest.raises(UnsupportedMissingError):
		require_missing_supported(new_values, new_type, Unmatched.MISSING)


def test_require_missing_supported_accepts_texts() -> None:
	"""
	Check that texts may hold a missing value.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Gives ``others`` to ``require_missing_supported``.
	"""
	require_missing_supported(TEXTS_WITH_MISSING, Type.TEXT, Unmatched.KEEP)


def test_require_missing_supported_advises_to_convert_kept_integers() -> None:
	"""
	Check that with Unmatched.KEEP, the advice for integers names the conversion to FLOAT64.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(UnsupportedMissingError) as error_info:
		require_missing_supported(INTEGERS_WITH_MISSING, Type.INT64, Unmatched.KEEP)

	error_text = str(error_info.value)
	assert error_text == KEPT_INTEGER_MESSAGE


def test_require_missing_supported_advises_to_convert_integers_given_only_missing_values() -> None:
	"""
	Check that integers whose new values are all missing get the advice to convert the Array to FLOAT64.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(UnsupportedMissingError) as error_info:
		require_missing_supported(ONLY_MISSING_VALUES, Type.INT64, Unmatched.MISSING)

	error_text = str(error_info.value)
	assert error_text == KEPT_INTEGER_MESSAGE


def test_require_missing_supported_advises_to_convert_kept_booleans() -> None:
	"""
	Check that with Unmatched.KEEP, the advice for booleans names the conversion to TEXT.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(UnsupportedMissingError) as error_info:
		require_missing_supported(BOOLEANS_WITH_MISSING, Type.BOOL, Unmatched.KEEP)

	error_text = str(error_info.value)
	assert error_text == KEPT_BOOLEAN_MESSAGE


def test_find_flat_new_values_keeps_unmatched_values_with_keep() -> None:
	"""
	Check that Unmatched.KEEP keeps a value without change as it is.

	.. versionadded:: 0.2.0
	"""
	new_values = find_flat_new_values(CODES_WITH_OTHER, KEPT_CODES)

	assert new_values == EXPECTED_KEPT_CODES


def test_map_values_widens_kept_integers_to_decimal_new_values() -> None:
	"""
	Check that kept integers become decimals when a new value is a decimal.

	.. versionadded:: 0.2.0
	"""
	mapped_values = map_values(CODES_WITH_OTHER, DECIMAL_CHANGE_AMONG_KEPT)

	widened_codes = mapped_values.tolist()
	assert widened_codes == EXPECTED_WIDENED_CODES


def test_map_values_rejects_texts_among_kept_numbers() -> None:
	"""
	Check that a text new value among kept numbers raises IncompatibleTypesError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(IncompatibleTypesError):
		map_values(CODES_WITH_OTHER, TEXT_CHANGE_AMONG_KEPT)


def test_map_values_makes_only_listed_decimals_missing_with_keep() -> None:
	"""
	Check that a decimal Array keeps its type when the only new value is missing.

	.. versionadded:: 0.2.0
	"""
	mapped_values = map_values(DECIMAL_ANSWERS, UNKNOWN_ANSWER_REMOVAL)

	kept_answer = mapped_values[0]
	unknown_answer = mapped_values[UNKNOWN_ANSWER_POSITION]
	is_unknown_missing = numpy.isnan(unknown_answer)
	assert kept_answer == EXPECTED_KEPT_ANSWER
	assert is_unknown_missing


def test_find_result_type_gives_the_array_type_to_integers_given_to_decimals() -> None:
	"""
	Check that Python integers given to a decimal Array take its type, as with the operators.

	.. versionadded:: 0.2.0
	"""
	result_type = find_result_type(Type.FLOAT64, INTEGER_CHANGE)

	assert result_type == Type.FLOAT64


def test_find_result_type_gives_the_new_type_to_another_family_without_keep() -> None:
	"""
	Check that numbers given to a text Array give their own type.

	.. versionadded:: 0.2.0
	"""
	result_type = find_result_type(Type.TEXT, INTEGER_CHANGE)

	assert result_type == Type.INT64


def test_find_result_type_gives_the_array_type_to_only_missing_new_values() -> None:
	"""
	Check that only missing new values keep the type of the Array when the other values are not kept.

	.. versionadded:: 0.2.0
	"""
	result_type = find_result_type(Type.FLOAT32, ONLY_MISSING_CHANGE)

	assert result_type == Type.FLOAT32


def test_find_result_type_widens_dates_to_datetimes_with_keep() -> None:
	"""
	Check that with Unmatched.KEEP, a datetime new value among kept dates gives datetimes.

	.. versionadded:: 0.2.0
	"""
	result_type = find_result_type(Type.DATE, DATETIME_CHANGE_AMONG_KEPT)

	assert result_type == Type.DATETIME


@pytest.mark.parametrize("number_case", NUMBER_CASES)
def test_find_number_type_follows_the_type_of_the_array(number_case: NumberCase) -> None:
	"""
	Check that numbers take the type of the Array, except decimals given to integers.

	.. versionadded:: 0.2.0

	Parameters
	----------
	number_case
		The type of the Array, the type of the new values and the expected type.
	"""
	number_type = find_number_type(number_case.array_type, number_case.new_type)

	assert number_type == number_case.expected_type


def test_find_mapping_result_gives_flat_new_values_and_their_type() -> None:
	"""
	Check that the new values of a grid come in one dimension, with the type of the result.

	.. versionadded:: 0.2.0
	"""
	mapping_result = find_mapping_result(GRID, LABELS)

	assert mapping_result.new_values == EXPECTED_FLAT_GRID_LABELS
	assert mapping_result.result_type == Type.TEXT


def test_find_mapping_result_keeps_missing_integers() -> None:
	"""
	Check that integers given None keep their type, without the check of map_values.

	.. versionadded:: 0.2.0
	"""
	mapping_result = find_mapping_result(CODES_WITH_OTHER, INTEGER_CHANGE)

	assert mapping_result.new_values == INTEGERS_WITH_MISSING
	assert mapping_result.result_type == Type.INT64


def test_map_values_keeps_small_integers_small() -> None:
	"""
	Check that integer new values given to INT8 values stay INT8.

	.. versionadded:: 0.2.0
	"""
	mapped_values = map_values(SMALL_CODES, SMALL_CODE_CHANGES)

	assert mapped_values.dtype == SMALL_INTEGER_DTYPE


def test_map_values_rejects_a_number_too_large_for_the_array_type() -> None:
	"""
	Check that a new integer out of the range of INT8 values raises ValueConversionError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(ValueConversionError):
		map_values(SMALL_CODES, LARGE_CODE_CHANGES)


def test_find_result_type_gives_the_array_type_when_every_new_value_is_missing() -> None:
	"""
	Check that with Unmatched.KEEP and only missing new values, the type of the Array is the result type.

	.. versionadded:: 0.2.0
	"""
	result_type = find_result_type(Type.FLOAT64, UNKNOWN_ANSWER_REMOVAL)

	assert result_type == Type.FLOAT64


def test_find_result_type_widens_the_array_type_with_keep() -> None:
	"""
	Check that with Unmatched.KEEP, integers of the Array and decimal new values give decimals.

	.. versionadded:: 0.2.0
	"""
	result_type = find_result_type(Type.INT64, DECIMAL_CHANGE_AMONG_KEPT)

	assert result_type == Type.FLOAT64


def test_find_flat_new_values_finds_a_date_among_datetimes_at_midnight() -> None:
	"""
	Check that a date old value finds the datetime at midnight of that day only, as Equal does.

	.. versionadded:: 0.1.0
	"""
	new_values = find_flat_new_values(MOMENTS, HOLIDAYS)

	assert new_values == EXPECTED_MIDNIGHT_HOLIDAYS


def test_find_lookup_value_writes_a_midnight_datetime_as_a_date_for_dates() -> None:
	"""
	Check that a datetime at midnight finds a date.

	.. versionadded:: 0.1.0
	"""
	lookup_value = find_lookup_value(MIDNIGHT_CHRISTMAS, Type.DATE)

	assert lookup_value == CHRISTMAS


def test_find_lookup_value_keeps_a_datetime_with_a_time_for_dates() -> None:
	"""
	Check that a datetime with a time is kept, so that it finds no date.

	.. versionadded:: 0.1.0
	"""
	lookup_value = find_lookup_value(MORNING_CHRISTMAS, Type.DATE)

	assert lookup_value == MORNING_CHRISTMAS


def test_write_date_as_datetime_keeps_a_datetime() -> None:
	"""
	Check that a datetime is not changed.

	.. versionadded:: 0.1.0
	"""
	datetime_value = write_date_as_datetime(MORNING_CHRISTMAS)

	assert datetime_value == MORNING_CHRISTMAS


def test_write_midnight_as_date_keeps_a_date() -> None:
	"""
	Check that a date is not changed.

	.. versionadded:: 0.1.0
	"""
	date_value = write_midnight_as_date(CHRISTMAS)

	assert date_value == CHRISTMAS
