"""
Unit tests of the context refusing dates and durations out of range.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

from numdaplot.column_storage.time_range_errors import TimeRangeErrors
from numdaplot.errors.dates.time_overflow_error import TimeOverflowError

OPERATION_NAME = "from_arrays"
COLUMN_NAME = "when"
PANDAS_MESSAGE = "out of bounds"
DATETIME_NAME = "DATETIME"
DURATION_NAME = "DURATION"


def test_time_range_errors_replaces_a_datetime_error() -> None:
	"""
	Check the type and the column of the error.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(TimeOverflowError) as error_info:
		with TimeRangeErrors(OPERATION_NAME, COLUMN_NAME):
			raise pandas.errors.OutOfBoundsDatetime(PANDAS_MESSAGE)

	assert error_info.value.type_name == DATETIME_NAME
	assert error_info.value.column_name == COLUMN_NAME


def test_time_range_errors_replaces_a_duration_error() -> None:
	"""
	Check the type of the error.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(TimeOverflowError) as error_info:
		with TimeRangeErrors(OPERATION_NAME, COLUMN_NAME):
			raise pandas.errors.OutOfBoundsTimedelta(PANDAS_MESSAGE)

	assert error_info.value.type_name == DURATION_NAME


def test_time_range_errors_keeps_the_cause() -> None:
	"""
	Check that the error of pandas stays available.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(TimeOverflowError) as error_info:
		with TimeRangeErrors(OPERATION_NAME, COLUMN_NAME):
			raise pandas.errors.OutOfBoundsDatetime(PANDAS_MESSAGE)

	cause = error_info.value.__cause__
	assert isinstance(cause, pandas.errors.OutOfBoundsDatetime)


def test_time_range_errors_leaves_other_errors() -> None:
	"""
	Check an error it does not replace.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(KeyError):
		with TimeRangeErrors(OPERATION_NAME, COLUMN_NAME):
			raise KeyError(COLUMN_NAME)


def test_time_range_errors_leaves_a_block_without_error() -> None:
	"""
	Check that a block without error goes on.

	.. versionadded:: 0.1.0
	"""
	with TimeRangeErrors(OPERATION_NAME, COLUMN_NAME):
		value = 1

	assert value == 1
