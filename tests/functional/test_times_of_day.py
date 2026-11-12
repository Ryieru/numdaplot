"""
Functional tests of the times of day of Arrays and Tables.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence
from datetime import UTC, datetime, time, timedelta
from pathlib import Path

import numpy
import openpyxl
import pandas
import pytest

import numdaplot as ndp

ACCIDENT_TIMES = [time(15, 35), time(8, 0), None, time(23, 59, 59, 999999)]
EXPECTED_ARRAY_TEXT = "Array(['15:35:00', '08:00:00', 'NaT', '23:59:59.999999'], dtype=TIME)"
EXPECTED_TABLE_TEXT = (
	"              hrmn\n              TIME\n0         15:35:00\n1         08:00:00\n2              NaT\n"
	"3  23:59:59.999999"
)
MORNING = time(8, 0)
NIGHT = time(22, 0)
EXPECTED_MORNING_FLAGS = [False, True, False, False]
EXPECTED_SORTED = [time(8, 0), time(15, 35), time(23, 59, 59, 999999), None]
MICROSECOND_WAITS = pandas.Series(numpy.array([5], dtype="timedelta64[us]"))
NUMPY_WAITS = numpy.array([5], dtype="timedelta64[us]")
ONE_HOUR = timedelta(hours=1)
ZONED_TIME = time(8, tzinfo=UTC)
BAAC_HOURS = ["15:35", "08:05", None]
EXPECTED_BAAC_TIMES = [time(15, 35), time(8, 5), None]
COMPACT_HOURS = ["1535", "0805"]
EXPECTED_COMPACT_TIMES = [time(15, 35), time(8, 5)]
WRONG_HOURS = ["15:35", "25:00"]
EXPECTED_WRONG_HOUR_MESSAGE = (
	"Cannot read the TEXT value '25:00' of the column 'hrmn' as TIME with the format HH:MM:SS. Give the format of "
	"the values with format=, using a CustomDateFormat of a time only."
)
EXPECTED_HOUR_TEXTS = ["15h35", "08h00", None, "23h59"]
BAAC_DAYS = [14, 1]
BAAC_MONTHS = [7, 1]
BAAC_YEARS = [2025, 2025]
BAAC_TIMES = [time(15, 35), time(0, 5)]
EXPECTED_MOMENTS = [datetime(2025, 7, 14, 15, 35), datetime(2025, 1, 1, 0, 5)]
EXPECTED_HOURS = [15.0, 8.0, 23.0]
LATE_EVENING = time(23, 30)
LAST_TIME = time(23, 59, 59, 999999)
EXPECTED_STATA_TEXTS = ["15:35:00", "08:00:00", "", "23:59:59.999999"]
EXCEL_HOURS = [time(15, 35), None, time(8, 5)]
EXCEL_WAITS = [timedelta(hours=30), None, timedelta(minutes=5)]
EXPECTED_EXCEL_TYPES = {"hrmn": ndp.Type.TIME, "wait": ndp.Type.DURATION}
EXPECTED_EXCEL_HOURS = [time(15, 35), None, time(8, 5)]


def build_accident_times() -> ndp.Array:
	"""
	Return the hours of four accidents, one of them missing.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Array
		A TIME Array.
	"""
	times = ndp.Array.from_list(ACCIDENT_TIMES)

	return times


def test_an_array_of_times_shows_and_gives_back_its_times() -> None:
	"""
	Check the type, the text, to_list and to_numpy of an Array of times.

	.. versionadded:: 0.1.0
	"""
	times = build_accident_times()

	array_text = repr(times)
	time_list = times.to_list()
	numpy_values = times.to_numpy()
	numpy_list = numpy_values.tolist()
	assert times.dtype == ndp.Type.TIME
	assert array_text == EXPECTED_ARRAY_TEXT
	assert time_list == ACCIDENT_TIMES
	assert numpy_list == ACCIDENT_TIMES


def test_a_table_of_times_goes_to_pandas_and_back() -> None:
	"""
	Check the display of a Table of times, and its round trip through pandas as datetime.time objects.

	.. versionadded:: 0.1.0
	"""
	times = build_accident_times()
	accidents = ndp.Table.from_arrays({"hrmn": times})

	table_text = str(accidents)
	frame = accidents.to_pandas()
	read_accidents = ndp.Table.from_pandas(frame)

	frame_column = frame["hrmn"]
	frame_times = frame_column.tolist()
	is_same_table = read_accidents.is_equal(ndp.Equality(other=accidents))
	assert table_text == EXPECTED_TABLE_TEXT
	assert frame_times == ACCIDENT_TIMES
	assert is_same_table


def test_rules_compare_times_of_day() -> None:
	"""
	Check Equal on an Array and Greater in a Table filter.

	.. versionadded:: 0.1.0
	"""
	times = build_accident_times()
	accidents = ndp.Table.from_arrays({"hrmn": times})

	morning_flags = times.check(ndp.Equal(MORNING))
	night = accidents.filter(ndp.Filter(conditions=[ndp.Condition(rule=ndp.Greater(NIGHT))]))

	morning_list = morning_flags.to_list()
	assert morning_list == EXPECTED_MORNING_FLAGS
	assert night.row_count == 1


def test_times_are_sorted_with_missing_values_last() -> None:
	"""
	Check the sort of an Array of times.

	.. versionadded:: 0.1.0
	"""
	times = build_accident_times()

	sorted_times = times.sort()

	sorted_list = sorted_times.to_list()
	assert sorted_list == EXPECTED_SORTED


def test_outside_durations_in_microseconds_stay_durations() -> None:
	"""
	Check that pandas and numpy durations in microseconds give DURATION, never TIME.

	.. versionadded:: 0.1.0
	"""
	wait_frame = pandas.DataFrame({"wait": MICROSECOND_WAITS})
	waits = ndp.Table.from_pandas(wait_frame)

	numpy_waits = ndp.Array.from_numpy(NUMPY_WAITS)

	assert waits.column_types["wait"] == ndp.Type.DURATION
	assert numpy_waits.dtype == ndp.Type.DURATION


def test_a_mean_of_times_is_refused() -> None:
	"""
	Check that the mean of times of day raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	times = build_accident_times()

	with pytest.raises(ndp.IncompatibleTypesError):
		times.compute(ndp.Mean())


def test_a_time_is_never_compared_with_a_duration() -> None:
	"""
	Check that a duration given to a rule on times raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	times = build_accident_times()

	with pytest.raises(ndp.IncompatibleTypesError):
		times.check(ndp.Equal(ONE_HOUR))


def test_a_time_with_a_time_zone_is_refused() -> None:
	"""
	Check that a time of day with a zone raises TimeZoneMismatchError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.TimeZoneMismatchError):
		ndp.Array.from_list([ZONED_TIME])


def convert_hours(hours: Sequence[str | None], conversion: ndp.TableConversion) -> ndp.Table:
	"""
	Return a Table of one hrmn column of texts, converted.

	.. versionadded:: 0.1.0

	Parameters
	----------
	hours
		The texts of the column.
	conversion
		The conversion of the column hrmn.

	Returns
	-------
	ndp.Table
		The converted Table.
	"""
	hour_texts = ndp.Array.from_list(hours)
	accidents = ndp.Table.from_arrays({"hrmn": hour_texts})
	converted_accidents = accidents.convert(conversion)

	return converted_accidents


def test_baac_hours_written_as_texts_become_times() -> None:
	"""
	Check the BAAC use: the hrmn column of texts such as 15:35 becomes TIME without any format.

	.. versionadded:: 0.1.0
	"""
	accidents = convert_hours(BAAC_HOURS, ndp.TableConversion(column="hrmn", dtype=ndp.Type.TIME))

	hour_column = accidents.column("hrmn")
	hours = hour_column.to_list()
	assert hours == EXPECTED_BAAC_TIMES


def test_hours_without_separator_are_read_with_a_custom_format() -> None:
	"""
	Check texts such as 1535 read with the pattern %H%M.

	.. versionadded:: 0.1.0
	"""
	conversion = ndp.TableConversion(column="hrmn", dtype=ndp.Type.TIME, format=ndp.CustomDateFormat("%H%M"))

	accidents = convert_hours(COMPACT_HOURS, conversion)

	hour_column = accidents.column("hrmn")
	hours = hour_column.to_list()
	assert hours == EXPECTED_COMPACT_TIMES


def test_an_hour_that_does_not_exist_is_named_in_the_error() -> None:
	"""
	Check the message of 25:00.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.ValueConversionError) as error_info:
		convert_hours(WRONG_HOURS, ndp.TableConversion(column="hrmn", dtype=ndp.Type.TIME))

	error_text = str(error_info.value)
	assert error_text == EXPECTED_WRONG_HOUR_MESSAGE


def test_times_are_written_with_a_custom_format() -> None:
	"""
	Check TIME written as texts with the pattern %Hh%M.

	.. versionadded:: 0.1.0
	"""
	times = build_accident_times()
	accidents = ndp.Table.from_arrays({"hrmn": times})
	conversion = ndp.TableConversion(column="hrmn", dtype=ndp.Type.TEXT, format=ndp.CustomDateFormat("%Hh%M"))

	written_accidents = accidents.convert(conversion)

	hour_column = written_accidents.column("hrmn")
	hour_texts = hour_column.to_list()
	assert hour_texts == EXPECTED_HOUR_TEXTS


def test_times_are_never_converted_to_datetimes() -> None:
	"""
	Check that TIME to DATETIME raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	times = build_accident_times()
	accidents = ndp.Table.from_arrays({"hrmn": times})

	with pytest.raises(ndp.IncompatibleTypesError):
		accidents.convert(ndp.TableConversion(column="hrmn", dtype=ndp.Type.DATETIME))


def test_baac_day_parts_and_hours_become_moments() -> None:
	"""
	Check the BAAC use: jour, mois and an give a DATE, and the DATE plus hrmn gives a DATETIME.

	.. versionadded:: 0.1.0
	"""
	days = ndp.Array.from_list(BAAC_DAYS)
	months = ndp.Array.from_list(BAAC_MONTHS)
	years = ndp.Array.from_list(BAAC_YEARS)
	dates = ndp.Array.from_date_parts(ndp.DateParts(year=years, month=months, day=days))
	hours = ndp.Array.from_list(BAAC_TIMES)

	moments = dates + hours

	moment_list = moments.to_list()
	assert moments.dtype == ndp.Type.DATETIME
	assert moment_list == EXPECTED_MOMENTS


def test_the_hour_of_each_accident_is_read() -> None:
	"""
	Check DatePart HOUR on times of day.

	.. versionadded:: 0.1.0
	"""
	times = build_accident_times()

	hours = times.apply(ndp.DatePart(unit=ndp.DatePartUnit.HOUR))

	present_hours = hours.select(ndp.IsPresent())
	hour_list = present_hours.to_list()
	assert hour_list == EXPECTED_HOURS


def test_a_time_moved_past_midnight_is_refused() -> None:
	"""
	Check that 23:30 plus one hour raises TimeOverflowError.

	.. versionadded:: 0.1.0
	"""
	late = ndp.Array.from_list([LATE_EVENING])

	with pytest.raises(ndp.TimeOverflowError):
		_ = late + ONE_HOUR


def test_the_earliest_and_latest_times_are_computed_per_group() -> None:
	"""
	Check Min and Max of times of day in an aggregation.

	.. versionadded:: 0.1.0
	"""
	times = build_accident_times()
	accidents = ndp.Table.from_arrays({"hrmn": times})
	calculations = [
		ndp.Calculation(column="hrmn", function=ndp.Min()),
		ndp.Calculation(column="hrmn", function=ndp.Max()),
	]

	extremes = accidents.aggregate(ndp.Aggregation(calculations=calculations))

	earliest_column = extremes.column("hrmn_min")
	latest_column = extremes.column("hrmn_max")
	earliest = earliest_column.to_value()
	latest = latest_column.to_value()
	assert earliest == MORNING
	assert latest == LAST_TIME


@pytest.mark.parametrize("file_name", ["accidents.csv", "accidents.json", "accidents.xlsx"])
def test_text_files_hold_times_as_texts_read_back_as_times(tmp_path: Path, file_name: str) -> None:
	"""
	Check that CSV, JSON and Excel files hold 15:35:00, which a conversion reads back as times.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	file_name
		The name of the file, whose extension chooses the format.
	"""
	times = build_accident_times()
	accidents = ndp.Table.from_arrays({"hrmn": times})
	path = tmp_path / file_name
	write_methods = {".csv": accidents.to_csv, ".json": accidents.to_json, ".xlsx": accidents.to_excel}
	read_methods = {".csv": ndp.Table.from_csv, ".json": ndp.Table.from_json, ".xlsx": ndp.Table.from_excel}
	write_table = write_methods[path.suffix]
	read_table = read_methods[path.suffix]

	write_table(path)
	read_accidents = read_table(path)
	converted_accidents = read_accidents.convert(ndp.TableConversion(column="hrmn", dtype=ndp.Type.TIME))

	hour_column = converted_accidents.column("hrmn")
	hours = hour_column.to_list()
	assert read_accidents.column_types["hrmn"] == ndp.Type.TEXT
	assert hours == ACCIDENT_TIMES


def test_a_parquet_file_keeps_times_of_day(tmp_path: Path) -> None:
	"""
	Check that a Parquet file gives back the same Table of times.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	times = build_accident_times()
	accidents = ndp.Table.from_arrays({"hrmn": times})
	path = tmp_path / "accidents.parquet"

	accidents.to_parquet(path)
	read_accidents = ndp.Table.from_parquet(path)

	is_same_table = read_accidents.is_equal(ndp.Equality(other=accidents, types=ndp.TypeMatch.STRICT))
	assert is_same_table


def test_a_stata_file_holds_times_as_texts(tmp_path: Path) -> None:
	"""
	Check that a Stata file holds times as texts, a missing time being an empty text as for any Stata text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	times = build_accident_times()
	accidents = ndp.Table.from_arrays({"hrmn": times})
	path = tmp_path / "accidents.dta"

	accidents.to_stata(path)
	read_accidents = ndp.Table.from_stata(path)

	hour_column = read_accidents.column("hrmn")
	hour_texts = hour_column.to_list()
	assert hour_texts == EXPECTED_STATA_TEXTS


def test_an_excel_file_typed_by_hand_gives_times_of_day_and_durations(tmp_path: Path) -> None:
	"""
	Check that time cells and duration cells of an Excel file become TIME and DURATION columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder given by pytest.
	"""
	path = tmp_path / "accidents.xlsx"
	book = openpyxl.Workbook()
	sheet = book.active
	assert sheet is not None
	sheet.append(["hrmn", "wait"])

	for hour, wait in zip(EXCEL_HOURS, EXCEL_WAITS, strict=True):
		sheet.append([hour, wait])

	book.save(path)

	table = ndp.Table.from_excel(path)

	frame = table.to_pandas()
	hour_column = frame["hrmn"]
	hours = hour_column.tolist()
	assert table.column_types == EXPECTED_EXCEL_TYPES
	assert hours == EXPECTED_EXCEL_HOURS
