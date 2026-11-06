"""
Functional tests of Tables created with a datetime or a duration out of range.

.. versionadded:: 0.1.0
"""

from pathlib import Path
from typing import Any, cast

import numpy
import pandas
import pytest
from numpy.typing import NDArray

import numdaplot as ndp

FAR_TEXT = "3000-01-01T10"
SECOND_DTYPE = "datetime64[s]"
MICROSECOND_DTYPE = "datetime64[us]"
DURATION_DTYPE = "timedelta64[s]"
FAR_SECONDS = 200000 * 86400
COLUMN_NAME = "when"
FILE_NAME = "sales.parquet"
FROM_ARRAYS_MESSAGE = (
	"The operation from_arrays gives values of the column 'when' outside the range of DATETIME, from 1677 to 2262."
)
FROM_PANDAS_MESSAGE = (
	"The operation Table creation gives values of the column 'when' outside the range of DATETIME, from 1677 to 2262."
)
ADD_COLUMN_MESSAGE = (
	"The operation add_column gives values of the column 'when' outside the range of DURATION, "
	"about 292 years before or after zero."
)
UTC_ZONE = "UTC"


def build_far_moments() -> NDArray[numpy.datetime64]:
	"""
	Return a datetime numpy holds in seconds, out of the range of nanoseconds.

	.. versionadded:: 0.1.0

	Returns
	-------
	NDArray[numpy.datetime64]
		The values.
	"""
	far_moments = numpy.array([FAR_TEXT], dtype=SECOND_DTYPE)

	return far_moments


def build_far_durations() -> NDArray[numpy.timedelta64]:
	"""
	Return a duration numpy holds in seconds, out of the range of nanoseconds.

	.. versionadded:: 0.1.0

	Returns
	-------
	NDArray[numpy.timedelta64]
		The values.
	"""
	far_durations = numpy.array([FAR_SECONDS], dtype=DURATION_DTYPE)

	return far_durations


def test_from_arrays_refuses_a_far_datetime_and_names_the_column() -> None:
	"""
	Check an Array that holds what a Table cannot.

	.. versionadded:: 0.1.0
	"""
	far_moments = build_far_moments()
	moments = ndp.Array.from_numpy(far_moments)

	with pytest.raises(ndp.TimeOverflowError) as error_info:
		ndp.Table.from_arrays({COLUMN_NAME: moments})

	error_text = str(error_info.value)
	assert error_text == FROM_ARRAYS_MESSAGE


def test_from_arrays_refuses_a_far_duration() -> None:
	"""
	Check a duration.

	.. versionadded:: 0.1.0
	"""
	far_durations = build_far_durations()
	durations = ndp.Array.from_numpy(far_durations)

	with pytest.raises(ndp.TimeOverflowError):
		ndp.Table.from_arrays({COLUMN_NAME: durations})


def test_add_column_refuses_a_far_duration_and_names_the_column() -> None:
	"""
	Check ``Table.add_column``.

	.. versionadded:: 0.1.0
	"""
	table = ndp.Table.from_arrays({"count": ndp.Array.from_list([1])})
	far_durations = build_far_durations()
	durations = ndp.Array.from_numpy(far_durations)
	new_column = ndp.NewColumn(name=COLUMN_NAME, values=durations)

	with pytest.raises(ndp.TimeOverflowError) as error_info:
		table.add_column(new_column)

	error_text = str(error_info.value)
	assert error_text == ADD_COLUMN_MESSAGE


def test_from_pandas_refuses_a_far_datetime_and_names_the_column() -> None:
	"""
	Check a pandas column in microseconds.

	.. versionadded:: 0.1.0
	"""
	far_moments = numpy.array([FAR_TEXT], dtype=MICROSECOND_DTYPE)
	frame = pandas.DataFrame({COLUMN_NAME: far_moments})

	with pytest.raises(ndp.TimeOverflowError) as error_info:
		ndp.Table.from_pandas(frame)

	error_text = str(error_info.value)
	assert error_text == FROM_PANDAS_MESSAGE


def test_from_pandas_refuses_a_far_datetime_with_a_time_zone() -> None:
	"""
	Check the other conversion of datetimes.

	.. versionadded:: 0.1.0
	"""
	far_moments = numpy.array([FAR_TEXT], dtype=MICROSECOND_DTYPE)
	# Some versions of the pandas stubs leave the date methods of a Series built from numpy unknown.
	far_series = cast(Any, pandas.Series(far_moments))
	moments = far_series.dt.tz_localize(UTC_ZONE)
	frame = pandas.DataFrame({COLUMN_NAME: moments})

	with pytest.raises(ndp.TimeOverflowError):
		ndp.Table.from_pandas(frame)


def test_from_pandas_refuses_a_far_duration() -> None:
	"""
	Check a pandas column of durations in seconds.

	.. versionadded:: 0.1.0
	"""
	far_durations = build_far_durations()
	frame = pandas.DataFrame({COLUMN_NAME: far_durations})

	with pytest.raises(ndp.TimeOverflowError):
		ndp.Table.from_pandas(frame)


def test_from_parquet_refuses_a_far_datetime(tmp_path: Path) -> None:
	"""
	Check a file holding a datetime out of range.

	.. versionadded:: 0.1.0
	"""
	far_moments = numpy.array([FAR_TEXT], dtype=MICROSECOND_DTYPE)
	frame = pandas.DataFrame({COLUMN_NAME: far_moments})
	path = tmp_path / FILE_NAME
	frame.to_parquet(path)

	with pytest.raises(ndp.TimeOverflowError):
		ndp.Table.from_parquet(path)


def test_an_array_keeps_a_far_datetime_of_numpy() -> None:
	"""
	Check that ``Array.from_numpy`` still holds the exact value.

	.. versionadded:: 0.1.0
	"""
	far_moments = build_far_moments()
	moments = ndp.Array.from_numpy(far_moments)

	numpy_moments = moments.to_numpy()

	assert numpy_moments.dtype == far_moments.dtype
	assert numpy_moments[0] == far_moments[0]
