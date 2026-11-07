"""
Unit tests of the application of a ValueMapping to the values of an Array.

.. versionadded:: 0.1.0
"""

from datetime import date, datetime

import numpy
import pytest

from numdaplot.arrays.creation.list_conversion import convert_list
from numdaplot.arrays.mapping.mapped_values import (
	find_flat_new_values,
	find_lookup_value,
	map_values,
	require_missing_supported,
	write_date_as_datetime,
	write_midnight_as_date,
)
from numdaplot.arrays.mapping.unmatched import Unmatched
from numdaplot.arrays.mapping.value_change import ValueChange
from numdaplot.arrays.mapping.value_mapping import ValueMapping
from numdaplot.data_types.type import Type
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.unmatched_value_error import UnmatchedValueError
from numdaplot.errors.unsupported_missing_error import UnsupportedMissingError

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
TEXTS_WITH_MISSING = ["a", None]


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

	Parameters
	----------
	new_values
		New values with a missing one.
	new_type
		Their type.
	"""
	with pytest.raises(UnsupportedMissingError):
		require_missing_supported(new_values, new_type)


def test_require_missing_supported_accepts_texts() -> None:
	"""
	Check that texts may hold a missing value.

	.. versionadded:: 0.1.0
	"""
	require_missing_supported(TEXTS_WITH_MISSING, Type.TEXT)


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
