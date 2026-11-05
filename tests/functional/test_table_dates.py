"""
Functional tests of dates and time zones in a Table: conversions, rules, statistics and files.

.. versionadded:: 0.1.0
"""

from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas
import pytest

import numdaplot as ndp

DAY_TEXTS = ["31/12/2026", "1.2.2026"]
ISO_DAY_TEXTS = ["2026-12-31", "2026-02-01"]
EXPECTED_DAYS = [date(2026, 12, 31), date(2026, 2, 1)]
EXPECTED_WRITTEN_DAYS = ["31/12/2026", "01/02/2026"]
IMPOSSIBLE_DAY = "31/02/2026"
PICKUP_TEXTS = ["2019-03-23 20:21:09", "2019-03-24T08:15", "2019-03-25"]
EXPECTED_PICKUPS = [datetime(2019, 3, 23, 20, 21, 9), datetime(2019, 3, 24, 8, 15), datetime(2019, 3, 25)]
PICKUP_DAY = "2019-03-25"
PICKUP_TIME = "2019-03-23 20:21:09"
THROUGH_DATETIME_HINT = "Convert the column to DATETIME first"
TRIPS_CSV_NAME = "trips.csv"
MIDNIGHT_PICKUPS = [datetime(2019, 3, 23), datetime(2019, 3, 24)]
VARIED_PICKUPS = [datetime(2019, 3, 23), datetime(2019, 3, 24, 8, 15)]
VISIT_TIMES = [datetime(2026, 7, 1, 10, 30), datetime(2026, 7, 1, 12, 30)]
SPRING_GAP = datetime(2026, 3, 29, 2, 30)
PARIS = ndp.TimeZone("Europe/Paris")
NEW_YORK = ndp.TimeZone("America/New_York")
ATTRIBUTE_PARIS = ndp.TimeZoneChange(mode=ndp.TimeZoneMode.ATTRIBUTE, zone=PARIS)
SHIFT_NEW_YORK = ndp.TimeZoneChange(mode=ndp.TimeZoneMode.SHIFT, zone=NEW_YORK)
REMOVE_ZONE = ndp.TimeZoneChange(mode=ndp.TimeZoneMode.REMOVE)
EXPECTED_PARIS_ZONES = {"time": PARIS}
EXPECTED_NAIVE_ZONES = {"time": None}
EXPECTED_NEW_YORK_TEXTS = ["2026-07-01 04:30:00-04:00", "2026-07-01 06:30:00-04:00"]
EXPECTED_HEADER = ["time", "DATETIME Europe/Paris"]
UTC_ELEVEN = datetime(2026, 7, 1, 9, tzinfo=ZoneInfo("UTC"))
EXPECTED_AFTER_ELEVEN = [False, True]
EXPECTED_LATEST = datetime(2026, 7, 1, 12, 30, tzinfo=ZoneInfo("Europe/Paris"))
SALE_DAYS = [date(2026, 1, 5), date(2026, 1, 28), date(2026, 2, 3)]
SALE_PRICES = [10.0, 20.0, 5.0]
EXPECTED_MONTHS = [date(2026, 1, 1), date(2026, 2, 1)]
EXPECTED_MONTH_TOTALS = [30.0, 5.0]
CSV_NAME = "visits.csv"
PANDAS_TIME_TEXTS = ["2026-07-01 10:30"]
PARQUET_NAME = "visits.parquet"
EXCEL_NAME = "visits.xlsx"
EXPECTED_CSV_TEXTS = ["2026-07-01 10:30:00+02:00", "2026-07-01 12:30:00+02:00"]


def build_text_days(texts: list[str]) -> ndp.Table:
	"""
	Return a Table of one text column named day.

	.. versionadded:: 0.1.0

	Parameters
	----------
	texts
		The texts of the column.

	Returns
	-------
	ndp.Table
		The Table.
	"""
	text_array = ndp.Array.from_list(texts)
	text_days = ndp.Table.from_arrays({"day": text_array})

	return text_days


def build_paris_visits() -> ndp.Table:
	"""
	Return a Table of two visit times in Paris.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Table
		The visits, of type DATETIME in Europe/Paris.
	"""
	visit_times = ndp.Array.from_list(VISIT_TIMES)
	visits = ndp.Table.from_arrays({"time": visit_times})
	paris_visits = visits.convert(ndp.Conversion(column="time", dtype=ndp.Type.DATETIME, timezone=ATTRIBUTE_PARIS))

	return paris_visits


def read_texts(table: ndp.Table, column_name: str) -> list[str]:
	"""
	Return a column converted to texts, as a list.

	.. versionadded:: 0.1.0

	Parameters
	----------
	table
		A Table.
	column_name
		The column to write as texts.

	Returns
	-------
	list[str]
		The texts.
	"""
	text_table = table.convert(ndp.Conversion(column=column_name, dtype=ndp.Type.TEXT))
	texts = text_table.column(column_name)
	text_list = texts.to_list()

	return text_list


def test_texts_written_day_first_become_dates() -> None:
	"""
	Check dates read day first, with two separators.

	.. versionadded:: 0.1.0
	"""
	text_days = build_text_days(DAY_TEXTS)
	day_first = ndp.Conversion(column="day", dtype=ndp.Type.DATE, format=ndp.DateFormat.DAY_MONTH_YEAR)

	days = text_days.convert(day_first)

	day_array = days.column("day")
	day_list = day_array.to_list()
	assert day_list == EXPECTED_DAYS


def test_texts_without_format_are_read_year_first() -> None:
	"""
	Check the default format.

	.. versionadded:: 0.1.0
	"""
	text_days = build_text_days(ISO_DAY_TEXTS)

	days = text_days.convert(ndp.Conversion(column="day", dtype=ndp.Type.DATE))

	day_array = days.column("day")
	day_list = day_array.to_list()
	assert day_list == EXPECTED_DAYS


def test_an_impossible_date_is_cited() -> None:
	"""
	Check that February 31 raises ValueConversionError citing the text.

	.. versionadded:: 0.1.0
	"""
	text_days = build_text_days([IMPOSSIBLE_DAY])
	day_first = ndp.Conversion(column="day", dtype=ndp.Type.DATE, format=ndp.DateFormat.DAY_MONTH_YEAR)

	with pytest.raises(ndp.ValueConversionError) as caught:
		text_days.convert(day_first)

	assert caught.value.rejected_value == IMPOSSIBLE_DAY


def test_dates_are_written_in_a_format() -> None:
	"""
	Check dates written back day first.

	.. versionadded:: 0.1.0
	"""
	text_days = build_text_days(ISO_DAY_TEXTS)
	days = text_days.convert(ndp.Conversion(column="day", dtype=ndp.Type.DATE))
	day_first = ndp.Conversion(column="day", dtype=ndp.Type.TEXT, format=ndp.DateFormat.DAY_MONTH_YEAR)

	written_days = days.convert(day_first)

	written_array = written_days.column("day")
	written_list = written_array.to_list()
	assert written_list == EXPECTED_WRITTEN_DAYS


def test_a_format_on_numbers_is_refused() -> None:
	"""
	Check that a format given to a number conversion raises InvalidConversionError.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Table.from_arrays({"price": ndp.Array.from_list(SALE_PRICES)})
	price_texts = ndp.Conversion(column="price", dtype=ndp.Type.TEXT, format=ndp.DateFormat.DAY_MONTH_YEAR)

	with pytest.raises(ndp.InvalidConversionError):
		prices.convert(price_texts)


def test_a_zone_is_attributed_shifted_and_removed() -> None:
	"""
	Check the zone after each change, and the clock times in New York.

	.. versionadded:: 0.1.0
	"""
	paris_visits = build_paris_visits()

	new_york_visits = paris_visits.convert(
		ndp.Conversion(column="time", dtype=ndp.Type.DATETIME, timezone=SHIFT_NEW_YORK)
	)
	naive_visits = new_york_visits.convert(ndp.Conversion(column="time", dtype=ndp.Type.DATETIME, timezone=REMOVE_ZONE))

	new_york_texts = read_texts(new_york_visits, "time")
	assert paris_visits.column_time_zones == EXPECTED_PARIS_ZONES
	assert new_york_texts == EXPECTED_NEW_YORK_TEXTS
	assert naive_visits.column_time_zones == EXPECTED_NAIVE_ZONES


def test_a_clock_time_skipped_by_the_spring_change_is_cited() -> None:
	"""
	Check that 02:30 on March 29, 2026 in Paris raises ValueConversionError.

	.. versionadded:: 0.1.0
	"""
	visits = ndp.Table.from_arrays({"time": ndp.Array.from_list([SPRING_GAP])})

	with pytest.raises(ndp.ValueConversionError):
		visits.convert(ndp.Conversion(column="time", dtype=ndp.Type.DATETIME, timezone=ATTRIBUTE_PARIS))


def test_shifting_datetimes_without_zone_is_refused() -> None:
	"""
	Check that SHIFT on datetimes without zone raises TimeZoneMismatchError.

	.. versionadded:: 0.1.0
	"""
	visits = ndp.Table.from_arrays({"time": ndp.Array.from_list(VISIT_TIMES)})

	with pytest.raises(ndp.TimeZoneMismatchError):
		visits.convert(ndp.Conversion(column="time", dtype=ndp.Type.DATETIME, timezone=SHIFT_NEW_YORK))


def test_print_shows_the_zone_under_the_column_name() -> None:
	"""
	Check the two header lines of a Table with a zone column.

	.. versionadded:: 0.1.0
	"""
	paris_visits = build_paris_visits()

	visit_text = repr(paris_visits)

	visit_lines = visit_text.splitlines()
	header_lines = [visit_line.strip() for visit_line in visit_lines[:2]]
	assert header_lines == EXPECTED_HEADER


def test_a_rule_compares_instants_across_zones() -> None:
	"""
	Check that 09:00 UTC is between 10:30 and 12:30 in Paris.

	.. versionadded:: 0.1.0
	"""
	paris_visits = build_paris_visits()

	after_eleven = paris_visits.check(ndp.Greater(UTC_ELEVEN))

	after_array = after_eleven.column("time")
	after_list = after_array.to_list()
	assert after_list == EXPECTED_AFTER_ELEVEN


def test_a_rule_without_zone_on_a_zone_column_is_refused() -> None:
	"""
	Check that a datetime without zone raises TimeZoneMismatchError on a zone column.

	.. versionadded:: 0.1.0
	"""
	paris_visits = build_paris_visits()
	first_visit_time = VISIT_TIMES[0]
	naive_rule = ndp.Greater(first_visit_time)

	with pytest.raises(ndp.TimeZoneMismatchError):
		paris_visits.filter(ndp.Filter(conditions=[ndp.Condition(rule=naive_rule)]))


def test_the_latest_visit_keeps_its_zone() -> None:
	"""
	Check that Max of a zone column gives a datetime in that zone.

	.. versionadded:: 0.1.0
	"""
	paris_visits = build_paris_visits()
	latest = ndp.Calculation(column="time", function=ndp.Max())
	latest_table = paris_visits.aggregate(ndp.Aggregation(calculations=[latest]))

	latest_visit = latest_table.to_value()

	assert latest_visit == EXPECTED_LATEST
	assert latest_visit.tzinfo is not None


def test_sales_are_grouped_by_month_through_a_period_column() -> None:
	"""
	Check the total of each month, computed from a DatePeriod column added to the Table.

	.. versionadded:: 0.1.0
	"""
	sale_days = ndp.Array.from_list(SALE_DAYS)
	prices = ndp.Array.from_list(SALE_PRICES)
	sales = ndp.Table.from_arrays({"day": sale_days, "price": prices})
	months = sale_days.apply(ndp.DatePeriod(unit=ndp.PeriodUnit.MONTH))
	sales_with_month = sales.add_column(ndp.NewColumn(name="month", values=months))
	total = ndp.Calculation(column="price", function=ndp.Sum())

	monthly_totals = sales_with_month.aggregate(ndp.Aggregation(calculations=[total], group_by=["month"]))

	month_array = monthly_totals.column("month")
	month_list = month_array.to_list()
	total_array = monthly_totals.column("price_sum")
	total_list = total_array.to_list()
	assert month_list == EXPECTED_MONTHS
	assert total_list == EXPECTED_MONTH_TOTALS


def test_a_zone_column_cannot_become_an_array() -> None:
	"""
	Check that column() on a zone column raises TimeZoneMismatchError.

	.. versionadded:: 0.1.0
	"""
	paris_visits = build_paris_visits()

	with pytest.raises(ndp.TimeZoneMismatchError):
		paris_visits.column("time")


def test_different_zones_are_never_equal() -> None:
	"""
	Check that the same instants in two zones make two different Tables.

	.. versionadded:: 0.1.0
	"""
	paris_visits = build_paris_visits()
	new_york_visits = paris_visits.convert(
		ndp.Conversion(column="time", dtype=ndp.Type.DATETIME, timezone=SHIFT_NEW_YORK)
	)

	is_equal = paris_visits.is_equal(ndp.Equality(other=new_york_visits))

	assert not is_equal


def test_a_csv_file_writes_the_offset_of_each_datetime(tmp_path: Path) -> None:
	"""
	Check that a zone column is written in CSV with its offset, and read back as texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / CSV_NAME
	paris_visits = build_paris_visits()

	paris_visits.to_csv(path)
	read_visits = ndp.Table.from_csv(path)

	read_texts_array = read_visits.column("time")
	read_texts_list = read_texts_array.to_list()
	assert read_texts_list == EXPECTED_CSV_TEXTS


def test_a_parquet_file_keeps_the_zone(tmp_path: Path) -> None:
	"""
	Check that a zone column read back from Parquet is equal.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / PARQUET_NAME
	paris_visits = build_paris_visits()

	paris_visits.to_parquet(path)
	read_visits = ndp.Table.from_parquet(path)

	is_equal = read_visits.is_equal(ndp.Equality(other=paris_visits))
	assert is_equal


def test_an_excel_file_refuses_a_zone_column(tmp_path: Path) -> None:
	"""
	Check that Excel files raise TimeZoneMismatchError for a zone column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / EXCEL_NAME
	paris_visits = build_paris_visits()

	with pytest.raises(ndp.TimeZoneMismatchError):
		paris_visits.to_excel(path)


def test_a_pandas_zone_column_becomes_a_datetime_column() -> None:
	"""
	Check that from_pandas keeps a zone.

	.. versionadded:: 0.1.0
	"""
	naive_times = pandas.to_datetime(PANDAS_TIME_TEXTS)
	paris_times = naive_times.tz_localize(PARIS.name)
	frame = pandas.DataFrame({"time": paris_times})

	visits = ndp.Table.from_pandas(frame)

	assert visits.column_time_zones == EXPECTED_PARIS_ZONES


def test_datetime_texts_without_format_keep_their_time_or_become_midnight() -> None:
	"""
	Check that texts with and without time are read as datetimes when no format is given.

	.. versionadded:: 0.1.0
	"""
	pickups = ndp.Array.from_list(PICKUP_TEXTS)
	trips = ndp.Table.from_arrays({"pickup": pickups})

	converted = trips.convert(ndp.Conversion(column="pickup", dtype=ndp.Type.DATETIME))

	pickup_list = converted.column("pickup").to_list()
	assert pickup_list == EXPECTED_PICKUPS


def test_a_given_time_format_refuses_a_text_without_time() -> None:
	"""
	Check that a format given explicitly stays strict, and that the message cites the text and the format.

	.. versionadded:: 0.1.0
	"""
	pickups = ndp.Array.from_list([PICKUP_DAY])
	trips = ndp.Table.from_arrays({"pickup": pickups})
	conversion = ndp.Conversion(column="pickup", dtype=ndp.Type.DATETIME, format=ndp.DateFormat.YEAR_MONTH_DAY_TIME)

	with pytest.raises(ndp.ValueConversionError, match="YEAR_MONTH_DAY_TIME") as caught_error:
		trips.convert(conversion)

	assert caught_error.value.rejected_value == PICKUP_DAY


def test_date_texts_with_a_time_are_refused_without_format() -> None:
	"""
	Check that reading a text with a time as a date is refused, since its time would be lost.

	.. versionadded:: 0.1.0
	"""
	pickups = ndp.Array.from_list([PICKUP_TIME])
	trips = ndp.Table.from_arrays({"pickup": pickups})

	with pytest.raises(ndp.ValueConversionError, match="YEAR_MONTH_DAY") as caught_error:
		trips.convert(ndp.Conversion(column="pickup", dtype=ndp.Type.DATE))

	assert caught_error.value.rejected_value == PICKUP_TIME


@pytest.mark.parametrize("pickups", [MIDNIGHT_PICKUPS, VARIED_PICKUPS])
def test_datetimes_written_in_a_csv_file_are_read_back_without_format(tmp_path: Path, pickups: list[datetime]) -> None:
	"""
	Check that datetimes come back from a CSV file, whether every time is midnight or not.

	.. versionadded:: 0.1.0
	"""
	csv_path = tmp_path / TRIPS_CSV_NAME
	pickup_values = ndp.Array.from_list(pickups)
	trips = ndp.Table.from_arrays({"pickup": pickup_values})
	trips.to_csv(csv_path)

	read_trips = ndp.Table.from_csv(csv_path)
	converted = read_trips.convert(ndp.Conversion(column="pickup", dtype=ndp.Type.DATETIME))

	pickup_list = converted.column("pickup").to_list()
	assert pickup_list == pickups


def test_a_time_format_on_dates_points_to_a_conversion_through_datetimes() -> None:
	"""
	Check that reading dates with a time format explains how to convert the column.

	.. versionadded:: 0.1.0
	"""
	trips = ndp.Table.from_arrays({"pickup": ndp.Array.from_list([PICKUP_TIME])})
	conversion = ndp.Conversion(column="pickup", dtype=ndp.Type.DATE, format=ndp.DateFormat.YEAR_MONTH_DAY_TIME)

	with pytest.raises(ndp.InvalidConversionError, match=THROUGH_DATETIME_HINT):
		trips.convert(conversion)
