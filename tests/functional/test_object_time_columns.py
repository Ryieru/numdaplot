"""
Functional tests of the columns of Python dates, datetimes and durations a Table receives.

.. versionadded:: 0.1.0
"""

from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any, cast

import pandas
import pytest

import numdaplot as ndp
from numdaplot.column_storage.column import Column

COLUMN_NAME = "when"
NEAR_DATE = date(2026, 1, 31)
FAR_DATE = date(3000, 1, 1)
NEAR_MOMENT = datetime(2026, 1, 31, 10)
FAR_MOMENT = datetime(3000, 1, 1, 10)
OLD_MOMENT = datetime(1000, 1, 1)
TWO_HOURS = timedelta(hours=2)
FAR_DURATION = timedelta(days=200000)
PARQUET_NAME = "sales.parquet"
EXCEL_NAME = "sales.xlsx"
CREATION_MESSAGE = (
	"The operation Table creation gives values of the column 'when' outside the range of DATETIME, from 1677 to 2262."
)


def build_object_table(values: list[object]) -> ndp.Table:
	"""
	Return a Table read from a pandas column of Python objects.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of the column.

	Returns
	-------
	ndp.Table
		The column ``when``.
	"""
	column = pandas.Series(values, dtype=object)
	frame = pandas.DataFrame({COLUMN_NAME: column})
	table = ndp.Table.from_pandas(frame)

	return table


def write_excel(column: Column, path: Path) -> None:
	"""
	Write a column in an Excel file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The values of the column ``when``.
	path
		The path of the file.
	"""
	# The pandas stubs leave the types of the Excel engines unknown.
	frame = cast(Any, pandas.DataFrame({COLUMN_NAME: column}))
	frame.to_excel(path, index=False)


@pytest.mark.parametrize(
	("values", "expected_type"),
	[
		([NEAR_DATE], ndp.Type.DATE),
		([NEAR_DATE, None], ndp.Type.DATE),
		([FAR_DATE], ndp.Type.DATE),
		([NEAR_MOMENT], ndp.Type.DATETIME),
		([NEAR_MOMENT, None], ndp.Type.DATETIME),
		([pandas.Timestamp(NEAR_MOMENT)], ndp.Type.DATETIME),
		([NEAR_DATE, NEAR_MOMENT], ndp.Type.DATETIME),
		([NEAR_MOMENT, NEAR_DATE], ndp.Type.DATETIME),
		([TWO_HOURS], ndp.Type.DURATION),
		([TWO_HOURS, None], ndp.Type.DURATION),
	],
)
def test_python_times_take_their_type(values: list[object], expected_type: ndp.Type) -> None:
	"""
	Check dates, datetimes and durations, with missing values and mixed with each other.

	.. versionadded:: 0.1.0
	"""
	table = build_object_table(values)

	column_type = table.column_types[COLUMN_NAME]
	assert column_type == expected_type


@pytest.mark.parametrize(
	"values",
	[
		[NEAR_MOMENT, "abc"],
		[NEAR_DATE, 5],
		[TWO_HOURS, NEAR_MOMENT],
		[NEAR_MOMENT.replace(tzinfo=UTC)],
		[NEAR_DATE, NEAR_MOMENT.replace(tzinfo=UTC)],
	],
)
def test_other_mixtures_stay_texts(values: list[object]) -> None:
	"""
	Check mixtures without a common type, and datetimes with a time zone, which lose nothing as texts.

	.. versionadded:: 0.1.0
	"""
	table = build_object_table(values)

	column_type = table.column_types[COLUMN_NAME]
	assert column_type == ndp.Type.TEXT


def test_a_date_beside_a_datetime_counts_as_midnight() -> None:
	"""
	Check that the mixture keeps every time.

	.. versionadded:: 0.1.0
	"""
	table = build_object_table([NEAR_DATE, NEAR_MOMENT])

	moments = table.column(COLUMN_NAME)
	moment_list = moments.to_list()
	assert moment_list == [datetime(2026, 1, 31), NEAR_MOMENT]


def test_python_dates_keep_their_values() -> None:
	"""
	Check dates, one of them beyond the range of nanoseconds.

	.. versionadded:: 0.1.0
	"""
	table = build_object_table([NEAR_DATE, FAR_DATE])

	dates = table.column(COLUMN_NAME)
	date_list = dates.to_list()
	assert date_list == [NEAR_DATE, FAR_DATE]


@pytest.mark.parametrize("value", [FAR_MOMENT, OLD_MOMENT, FAR_DURATION])
def test_a_python_time_out_of_range_is_refused(value: object) -> None:
	"""
	Check datetimes and durations beyond the range of nanoseconds.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.TimeOverflowError):
		build_object_table([value])


def test_a_date_column_of_pandas_stays_a_date() -> None:
	"""
	Check the column ``.dt.date`` gives, the usual way to drop the time of a datetime.

	.. versionadded:: 0.1.0
	"""
	moments = pandas.Series(pandas.to_datetime([NEAR_MOMENT]))
	frame = pandas.DataFrame({COLUMN_NAME: moments.dt.date})

	table = ndp.Table.from_pandas(frame)

	column_type = table.column_types[COLUMN_NAME]
	assert column_type == ndp.Type.DATE


def test_a_date_column_of_a_parquet_file_stays_a_date(tmp_path: Path) -> None:
	"""
	Check a file whose reading gives Python dates.

	.. versionadded:: 0.1.0
	"""
	path = tmp_path / PARQUET_NAME
	column = pandas.Series([NEAR_DATE], dtype=object)
	pandas.DataFrame({COLUMN_NAME: column}).to_parquet(path)

	table = ndp.Table.from_parquet(path)

	dates = table.column(COLUMN_NAME)
	date_list = dates.to_list()
	assert table.column_types[COLUMN_NAME] == ndp.Type.DATE
	assert date_list == [NEAR_DATE]


@pytest.mark.parametrize("values", [[FAR_MOMENT], [NEAR_MOMENT, FAR_MOMENT], [FAR_MOMENT, None]])
def test_from_excel_refuses_a_far_datetime_on_every_version_of_pandas(tmp_path: Path, values: list[object]) -> None:
	"""
	Check a sheet holding a datetime out of range, alone or beside other values.

	.. versionadded:: 0.1.0
	"""
	path = tmp_path / EXCEL_NAME
	column = pandas.Series(values, dtype=object)
	write_excel(column, path)

	with pytest.raises(ndp.TimeOverflowError) as error_info:
		ndp.Table.from_excel(path)

	error_text = str(error_info.value)
	assert error_text == CREATION_MESSAGE


def test_from_excel_keeps_a_date_beside_a_text_as_text(tmp_path: Path) -> None:
	"""
	Check a sheet without a common type.

	.. versionadded:: 0.1.0
	"""
	path = tmp_path / EXCEL_NAME
	column = pandas.Series([NEAR_MOMENT, "abc"], dtype=object)
	write_excel(column, path)

	table = ndp.Table.from_excel(path)

	column_type = table.column_types[COLUMN_NAME]
	assert column_type == ndp.Type.TEXT
