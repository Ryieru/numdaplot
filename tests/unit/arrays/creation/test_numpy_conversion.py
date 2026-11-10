"""
Unit tests of copy_numpy_values and normalize_text.

.. versionadded:: 0.1.0
"""

from datetime import time
from typing import Any, cast

import numpy
import pytest

from numdaplot.arrays.creation.numpy_conversion import copy_numpy_values, normalize_durations, normalize_text
from numdaplot.errors.time_overflow_error import TimeOverflowError
from numdaplot.errors.unsupported_type_error import UnsupportedTypeError

# Some versions of the numpy stubs leave out the missing value marker of StringDType.
STRING_DTYPE_CLASS = cast(Any, numpy.dtypes.StringDType)
TEXT_DTYPE = STRING_DTYPE_CLASS(na_object=numpy.nan)
TEXT_DTYPE_MARKED_WITH_NONE = STRING_DTYPE_CLASS(na_object=None)
CHANGED_VALUE = 99
FIRST_POSITION = 0
ORIGINAL_VALUES = [1, 2]
TEXT_VALUES = ["a", "b"]
MICROSECOND_DURATIONS = numpy.array([5, "NaT"], dtype="timedelta64[us]")
NANOSECOND_DTYPE = numpy.dtype("timedelta64[ns]")
SECOND_DURATIONS = numpy.array([5], dtype="timedelta64[s]")
FAR_DURATIONS = numpy.array([2**62], dtype="timedelta64[us]")
OBJECT_TIMES = numpy.array([time(8), None], dtype=object)
TIME_DTYPE = numpy.dtype("timedelta64[us]")


def test_copy_numpy_values_is_independent_from_the_original() -> None:
	"""
	Check that changing the original array does not change the copy.

	.. versionadded:: 0.1.0
	"""
	original_values = numpy.array(ORIGINAL_VALUES)
	copied_values = copy_numpy_values(original_values)

	original_values[FIRST_POSITION] = CHANGED_VALUE

	copied_list = copied_values.tolist()
	assert copied_list == ORIGINAL_VALUES


def test_copy_numpy_values_rejects_python_objects() -> None:
	"""
	Check that an object array raises UnsupportedTypeError.

	.. versionadded:: 0.1.0
	"""
	object_values = numpy.array([None], dtype=object)

	with pytest.raises(UnsupportedTypeError):
		copy_numpy_values(object_values)


def test_normalize_text_stores_fixed_length_texts_as_variable_length_texts() -> None:
	"""
	Check that a fixed-length text array becomes a StringDType array.

	.. versionadded:: 0.1.0
	"""
	fixed_length_texts = numpy.array(["a", "bc"])

	normalized_values = normalize_text(fixed_length_texts)

	assert normalized_values.dtype == TEXT_DTYPE


def test_normalize_text_turns_another_missing_marker_into_nan() -> None:
	"""
	Check that a text array marking missing values with None gets the marker of a TEXT Array.

	.. versionadded:: 0.1.0
	"""
	marked_texts = numpy.array(["a", None], dtype=TEXT_DTYPE_MARKED_WITH_NONE)

	normalized_values = normalize_text(marked_texts)

	assert normalized_values.dtype == TEXT_DTYPE
	missing = numpy.isnan(normalized_values)
	assert missing.tolist() == [False, True]


def test_normalize_text_keeps_other_values_as_they_are() -> None:
	"""
	Check that numbers are returned without copy.

	.. versionadded:: 0.1.0
	"""
	numbers = numpy.array(ORIGINAL_VALUES)

	normalized_values = normalize_text(numbers)

	assert normalized_values is numbers


def test_normalize_text_keeps_texts_already_stored_as_they_are() -> None:
	"""
	Check that texts already of the TEXT dtype are returned without copy.

	.. versionadded:: 0.1.0
	"""
	texts = numpy.array(TEXT_VALUES, dtype=TEXT_DTYPE)

	normalized_values = normalize_text(texts)

	assert normalized_values is texts


def test_normalize_durations_turns_microseconds_into_nanoseconds() -> None:
	"""
	Check that durations in microseconds become nanoseconds, NaT kept.

	.. versionadded:: 0.1.0
	"""
	durations = normalize_durations(MICROSECOND_DURATIONS)

	assert durations.dtype == NANOSECOND_DTYPE


def test_normalize_durations_keeps_other_units() -> None:
	"""
	Check that seconds are kept as they are.

	.. versionadded:: 0.1.0
	"""
	durations = normalize_durations(SECOND_DURATIONS)

	assert durations is SECOND_DURATIONS


def test_normalize_durations_rejects_a_duration_beyond_nanoseconds() -> None:
	"""
	Check that a duration too long for nanoseconds raises TimeOverflowError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(TimeOverflowError):
		normalize_durations(FAR_DURATIONS)


def test_normalize_durations_rejects_a_duration_numpy_cannot_convert(overflowing_durations: Any) -> None:
	"""
	Check that a numpy raising OverflowError for nanoseconds gives TimeOverflowError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	overflowing_durations
		Durations whose conversion raises.
	"""
	with pytest.raises(TimeOverflowError):
		normalize_durations(overflowing_durations)


def test_normalize_durations_rejects_a_duration_numpy_wraps_around(wrapping_durations: Any) -> None:
	"""
	Check that a numpy wrapping the value around for nanoseconds gives TimeOverflowError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	wrapping_durations
		Durations whose conversion wraps around.
	"""
	with pytest.raises(TimeOverflowError):
		normalize_durations(wrapping_durations)


def test_copy_numpy_values_reads_an_object_array_of_times() -> None:
	"""
	Check that Python times of day give times stored in microseconds.

	.. versionadded:: 0.1.0
	"""
	copied_values = copy_numpy_values(OBJECT_TIMES)

	assert copied_values.dtype == TIME_DTYPE
