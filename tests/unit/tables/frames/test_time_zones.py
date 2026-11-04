"""
Unit tests of the time zones of the datetime columns of a Table.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

from numdaplot.data_types.type import Type
from numdaplot.dates.time_zone import TimeZone
from numdaplot.errors.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.errors.unsupported_type_error import UnsupportedTypeError
from numdaplot.tables.frames.time_zones import (
	attribute_source_time_zone,
	attribute_utc_results,
	find_column_time_zone,
	name_column_type,
	normalize_time_zone_column,
	remove_utc_zone,
	require_no_time_zone,
)

PARIS_NAME = "Europe/Paris"
PARIS = TimeZone(PARIS_NAME)
NAIVE_TIMES = pandas.Series(pandas.to_datetime(["2026-07-01 08:30"]))
PARIS_TIMES = NAIVE_TIMES.dt.tz_localize(PARIS_NAME)
SECOND_UTC_TIMES = NAIVE_TIMES.dt.tz_localize("UTC").dt.as_unit("s")
FIXED_OFFSET_TIMES = pandas.Series(pandas.to_datetime(["2026-07-01 10:30+02:00"]))
PRICES = pandas.Series([1.5])
EXPECTED_PARIS_TYPE = "DATETIME Europe/Paris"
EXPECTED_PRICE_TYPE = "FLOAT64"
EXPECTED_NANOSECOND_UTC = "datetime64[ns, UTC]"
EXPECTED_UTC_CLOCK = [pandas.Timestamp("2026-07-01 06:30")]
EXPECTED_PARIS_CLOCK = [pandas.Timestamp("2026-07-01 10:30", tz=PARIS_NAME)]
EXCEL_OPERATION = "An Excel file"


def test_find_column_time_zone_reads_the_zone_of_a_datetime_column() -> None:
	"""
	Check the zone of a column with one, and None for a column without.

	.. versionadded:: 0.1.0
	"""
	paris_zone = find_column_time_zone(PARIS_TIMES)
	no_zone = find_column_time_zone(NAIVE_TIMES)

	assert paris_zone == PARIS
	assert no_zone is None


def test_name_column_type_adds_the_zone_after_the_type() -> None:
	"""
	Check the type names of a column with a zone and of a number column.

	.. versionadded:: 0.1.0
	"""
	paris_type = name_column_type(PARIS_TIMES, Type.DATETIME)
	price_type = name_column_type(PRICES, Type.FLOAT64)

	assert paris_type == EXPECTED_PARIS_TYPE
	assert price_type == EXPECTED_PRICE_TYPE


def test_normalize_time_zone_column_counts_in_nanoseconds() -> None:
	"""
	Check that a zone column in seconds is stored in nanoseconds.

	.. versionadded:: 0.1.0
	"""
	normalized_column = normalize_time_zone_column(SECOND_UTC_TIMES)

	dtype_name = str(normalized_column.dtype)
	assert dtype_name == EXPECTED_NANOSECOND_UTC


def test_normalize_time_zone_column_rejects_a_fixed_offset() -> None:
	"""
	Check that a fixed offset raises UnsupportedTypeError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(UnsupportedTypeError):
		normalize_time_zone_column(FIXED_OFFSET_TIMES)


def test_remove_utc_zone_gives_the_utc_clock_time() -> None:
	"""
	Check that 08:30 in Paris in summer is 06:30 UTC.

	.. versionadded:: 0.1.0
	"""
	utc_column = remove_utc_zone(PARIS_TIMES)

	utc_times = utc_column.tolist()
	assert utc_times == EXPECTED_UTC_CLOCK


def test_attribute_utc_results_shows_utc_clock_times_in_a_zone() -> None:
	"""
	Check that 08:30 UTC is 10:30 in Paris in summer.

	.. versionadded:: 0.1.0
	"""
	paris_column = attribute_utc_results(NAIVE_TIMES, PARIS)

	paris_times = paris_column.tolist()
	assert paris_times == EXPECTED_PARIS_CLOCK


def test_attribute_source_time_zone_moves_datetime_results_to_the_source_zone() -> None:
	"""
	Check datetime results of a column with a zone.

	.. versionadded:: 0.1.0
	"""
	results = attribute_source_time_zone(NAIVE_TIMES, PARIS_TIMES)

	result_times = results.tolist()
	assert result_times == EXPECTED_PARIS_CLOCK


@pytest.mark.parametrize(("results", "source"), [(NAIVE_TIMES, NAIVE_TIMES), (PRICES, PARIS_TIMES)])
def test_attribute_source_time_zone_keeps_other_results(results: pandas.Series, source: pandas.Series) -> None:
	"""
	Check that results of a column without zone, or results that are not datetimes, stay the same.

	.. versionadded:: 0.1.0

	Parameters
	----------
	results
		The results.
	source
		The column they are computed on.
	"""
	kept_results = attribute_source_time_zone(results, source)

	assert kept_results is results


def test_require_no_time_zone_rejects_a_column_with_a_zone() -> None:
	"""
	Check that a zone column raises TimeZoneMismatchError, and a Table without accepted.

	.. versionadded:: 0.1.0
	"""
	zone_frame = pandas.DataFrame({"time": PARIS_TIMES})
	naive_frame = pandas.DataFrame({"time": NAIVE_TIMES})

	require_no_time_zone(naive_frame, EXCEL_OPERATION)
	with pytest.raises(TimeZoneMismatchError):
		require_no_time_zone(zone_frame, EXCEL_OPERATION)
