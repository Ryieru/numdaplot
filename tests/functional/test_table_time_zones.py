"""
Functional tests of time zones in a Table: attribution, shift, comparison, display and files.

.. versionadded:: 0.2.0
"""

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas
import pytest

import numdaplot as ndp

VISIT_TIMES = [datetime(2026, 7, 1, 10, 30), datetime(2026, 7, 1, 12, 30)]
PARIS = ndp.TimeZone("Europe/Paris")
NEW_YORK = ndp.TimeZone("America/New_York")
ATTRIBUTE_PARIS = ndp.TimeZoneChange(mode=ndp.TimeZoneMode.ATTRIBUTE, zone=PARIS)
SPRING_GAP = datetime(2026, 3, 29, 2, 30)
SHIFT_NEW_YORK = ndp.TimeZoneChange(mode=ndp.TimeZoneMode.SHIFT, zone=NEW_YORK)
REMOVE_ZONE = ndp.TimeZoneChange(mode=ndp.TimeZoneMode.REMOVE)
EXPECTED_PARIS_ZONES = {"time": PARIS}
EXPECTED_NAIVE_ZONES = {"time": None}
EXPECTED_NEW_YORK_TEXTS = ["2026-07-01 04:30:00-04:00", "2026-07-01 06:30:00-04:00"]
EXPECTED_HEADER = ["time", "DATETIME Europe/Paris"]
UTC_ELEVEN = datetime(2026, 7, 1, 9, tzinfo=ZoneInfo("UTC"))
EXPECTED_AFTER_ELEVEN = [False, True]
EXPECTED_LATEST = datetime(2026, 7, 1, 12, 30, tzinfo=ZoneInfo("Europe/Paris"))
CSV_NAME = "visits.csv"
PANDAS_TIME_TEXTS = ["2026-07-01 10:30"]
PARQUET_NAME = "visits.parquet"
EXCEL_NAME = "visits.xlsx"
EXPECTED_CSV_TEXTS = ["2026-07-01 10:30:00+02:00", "2026-07-01 12:30:00+02:00"]


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
	paris_visits = visits.convert(
		ndp.TableConversion(columns=["time"], dtype=ndp.Type.DATETIME, timezone=ATTRIBUTE_PARIS)
	)

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
	text_table = table.convert(ndp.TableConversion(columns=[column_name], dtype=ndp.Type.TEXT))
	texts = text_table.column(column_name)
	text_list = texts.to_list()

	return text_list


def test_a_zone_is_attributed_shifted_and_removed() -> None:
	"""
	Check the zone after each change, and the clock times in New York.

	.. versionadded:: 0.1.0
	"""
	paris_visits = build_paris_visits()

	new_york_visits = paris_visits.convert(
		ndp.TableConversion(columns=["time"], dtype=ndp.Type.DATETIME, timezone=SHIFT_NEW_YORK)
	)
	naive_visits = new_york_visits.convert(
		ndp.TableConversion(columns=["time"], dtype=ndp.Type.DATETIME, timezone=REMOVE_ZONE)
	)

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
		visits.convert(ndp.TableConversion(columns=["time"], dtype=ndp.Type.DATETIME, timezone=ATTRIBUTE_PARIS))


def test_shifting_datetimes_without_zone_is_refused() -> None:
	"""
	Check that SHIFT on datetimes without zone raises TimeZoneMismatchError.

	.. versionadded:: 0.1.0
	"""
	visits = ndp.Table.from_arrays({"time": ndp.Array.from_list(VISIT_TIMES)})

	with pytest.raises(ndp.TimeZoneMismatchError):
		visits.convert(ndp.TableConversion(columns=["time"], dtype=ndp.Type.DATETIME, timezone=SHIFT_NEW_YORK))


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
		ndp.TableConversion(columns=["time"], dtype=ndp.Type.DATETIME, timezone=SHIFT_NEW_YORK)
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
