"""
Unit tests of the comparison of values with the values at the same positions of another Array.

.. versionadded:: 0.2.0
"""

from datetime import date, datetime

import numpy
import pytest

from numdaplot.arrays.array import Array
from numdaplot.arrays.array_data import read_stored_values
from numdaplot.arrays.selection.array_reference import compare_with_array, require_comparable_values
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.shape_mismatch_error import ShapeMismatchError

DEPARTURES = Array.from_list(["Pau", "Lyon", "Nice"])
ARRIVALS = Array.from_list(["Pau", None, "Dax"])
EXPECTED_SAME_CITIES = [True, False, False]
EXPECTED_OTHER_CITIES = [False, False, True]
SHORT_ARRIVALS = Array.from_list(["Pau"])
NUMBERS = Array.from_list([1.0, 2.0, 3.0])
EQUAL_NAME = "Equal"
DAYS = Array.from_list([date(2026, 1, 1)])
MIDNIGHTS = Array.from_list([datetime(2026, 1, 1)])


def test_compare_with_array_compares_each_position() -> None:
	"""
	Check that each value is compared with the value at its position, a missing reference matching nothing.

	.. versionadded:: 0.2.0
	"""
	departure_values = read_stored_values(DEPARTURES)

	matches = compare_with_array(departure_values, ARRIVALS, numpy.equal, EQUAL_NAME)

	match_list = matches.tolist()
	assert match_list == EXPECTED_SAME_CITIES


def test_compare_with_array_keeps_missing_references_out_of_not_equal() -> None:
	"""
	Check that a missing reference value does not satisfy a not equal comparison either.

	.. versionadded:: 0.2.0
	"""
	departure_values = read_stored_values(DEPARTURES)

	matches = compare_with_array(departure_values, ARRIVALS, numpy.not_equal, EQUAL_NAME)

	match_list = matches.tolist()
	assert match_list == EXPECTED_OTHER_CITIES


def test_compare_with_array_rejects_another_shape() -> None:
	"""
	Check that a reference Array of another shape raises ShapeMismatchError.

	.. versionadded:: 0.2.0
	"""
	departure_values = read_stored_values(DEPARTURES)

	with pytest.raises(ShapeMismatchError):
		compare_with_array(departure_values, SHORT_ARRIVALS, numpy.equal, EQUAL_NAME)


def test_require_comparable_values_rejects_texts_and_numbers() -> None:
	"""
	Check that texts compared with numbers raise IncompatibleTypesError.

	.. versionadded:: 0.2.0
	"""
	departure_values = read_stored_values(DEPARTURES)
	number_values = read_stored_values(NUMBERS)

	with pytest.raises(IncompatibleTypesError):
		require_comparable_values(departure_values, number_values, EQUAL_NAME)


def test_require_comparable_values_accepts_dates_and_datetimes() -> None:
	"""
	Check that dates and datetimes, of the same family, can be compared.

	.. versionadded:: 0.2.0
	"""
	day_values = read_stored_values(DAYS)
	midnight_values = read_stored_values(MIDNIGHTS)

	require_comparable_values(day_values, midnight_values, EQUAL_NAME)
