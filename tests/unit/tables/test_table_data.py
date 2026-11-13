"""
Unit tests of TableData.

.. versionadded:: 0.1.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

import numpy
import pandas
import pytest

from numdaplot.column_storage.column import Column
from numdaplot.dates.time_zone import TimeZone
from numdaplot.errors.settings.refused_operation_error import RefusedOperationError
from numdaplot.errors.tables.column_not_found_error import ColumnNotFoundError
from numdaplot.positions.shape import Shape
from numdaplot.tables.files.column_names import ColumnNames
from numdaplot.tables.table_data import TableData, read_stored_frame
from numdaplot.types.type import Type

FRAME = pandas.DataFrame({"city": pandas.Series(["Pau", "Lyon"], dtype="string"), "price": [1.5, 8.0]})
NO_COLUMN_FRAME = pandas.DataFrame()
EXPECTED_ROW_COUNT = 2
EXPECTED_COLUMN_COUNT = 2
EXPECTED_SHAPE = Shape([2, 2])
NO_ROW_FRAME = pandas.DataFrame({"price": pandas.Series([], dtype="float64")})
EXPECTED_NO_ROW_SHAPE = Shape([0, 1])
EXPECTED_EMPTY_SHAPE = Shape([0, 0])
EXPECTED_COLUMN_NAMES = ["city", "price"]
EXPECTED_COLUMN_TYPES = {"city": Type.TEXT, "price": Type.FLOAT64}
RAW_FRAME = pandas.DataFrame({"count": [1, 2]})
INTEGER_DTYPE_NAME = "Int64"
OTHER_FRAME = pandas.DataFrame({"price": [3.0]})
UNKNOWN_COLUMN = "prise"
SPACED_FRAME = pandas.DataFrame({" count\n": [1, 2]})
EXPECTED_CLEANED_NAMES = ["count"]
EXPECTED_KEPT_NAMES = [" count\n"]
MICROSECOND_WAIT_FRAME = pandas.DataFrame({"wait": pandas.Series(numpy.array([5], dtype="timedelta64[us]"))})
PARIS_TIMES = (
	pandas.Series(pandas.to_datetime(["2026-07-01 10:30"])).astype("datetime64[ns]").dt.tz_localize("Europe/Paris")
)
TIME_FRAME = pandas.DataFrame({"time": PARIS_TIMES, "price": [1.5]})
EXPECTED_TIME_ZONES = {"time": TimeZone("Europe/Paris")}
HOUR_DTYPE_NAME = "timedelta64[us]"
MINUTE_AFTER_MIDNIGHT = numpy.array([60000000], dtype=HOUR_DTYPE_NAME)
HOUR_FRAME = pandas.DataFrame({"hour": MINUTE_AFTER_MIDNIGHT})


class ExposedTableData(TableData):
	"""
	TableData giving the tests access to its protected helpers.

	.. versionadded:: 0.1.0
	"""

	def wrap(self, frame: pandas.DataFrame) -> TableData:
		"""
		Call the protected wrapping.

		.. versionadded:: 0.1.0

		Parameters
		----------
		frame
			Other columns.

		Returns
		-------
		TableData
			What the protected helper returns.
		"""
		wrapped_table = self._wrap(frame)

		return wrapped_table

	def read_column(self, column_name: str) -> Column:
		"""
		Call the protected column reading.

		.. versionadded:: 0.1.0

		Parameters
		----------
		column_name
			The name of a column.

		Returns
		-------
		Column
			What the protected helper returns.
		"""
		column = self._read_column(column_name)

		return column

	@classmethod
	def from_frame(cls, frame: pandas.DataFrame) -> TableData:
		"""
		Call the protected creation from a DataFrame.

		.. versionadded:: 0.1.0

		Parameters
		----------
		frame
			Any DataFrame.

		Returns
		-------
		TableData
			What the protected helper returns.
		"""
		table = cls._from_frame(frame)

		return table

	@classmethod
	def from_read_frame(cls, frame: pandas.DataFrame, column_names: ColumnNames) -> TableData:
		"""
		Call the protected creation from a DataFrame read from outside numdaplot.

		.. versionadded:: 0.1.0

		Parameters
		----------
		frame
			Any DataFrame.
		column_names
			Whether its names are cleaned.

		Returns
		-------
		TableData
			What the protected helper returns.
		"""
		table = cls._from_read_frame(frame, column_names)

		return table

	def read_frame(self) -> pandas.DataFrame:
		"""
		Return the stored columns.

		.. versionadded:: 0.1.0

		Returns
		-------
		pandas.DataFrame
			The stored columns.
		"""
		return self._frame


def test_table_data_refuses_its_constructor() -> None:
	"""
	Check that creating TableData by its constructor raises RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedOperationError):
		TableData()


def test_table_data_create_stores_the_columns_without_copy() -> None:
	"""
	Check that _create keeps the given pandas DataFrame itself.

	.. versionadded:: 0.1.0
	"""
	table = TableData._create(FRAME)

	assert table._frame is FRAME


def test_table_data_gives_its_rows_then_its_columns_as_shape() -> None:
	"""
	Check that the shape holds the number of rows, then the number of columns.

	.. versionadded:: 0.2.0
	"""
	table = TableData._create(FRAME)

	assert table.shape == EXPECTED_SHAPE


def test_table_data_shape_keeps_the_columns_of_a_table_without_rows() -> None:
	"""
	Check that a table with columns and no row has a first dimension of zero.

	.. versionadded:: 0.2.0
	"""
	table = TableData._create(NO_ROW_FRAME)

	assert table.shape == EXPECTED_NO_ROW_SHAPE


def test_table_data_shape_is_zero_by_zero_without_columns() -> None:
	"""
	Check that a table without columns has a shape of zero rows and zero columns.

	.. versionadded:: 0.2.0
	"""
	table = TableData._create(NO_COLUMN_FRAME)

	assert table.shape == EXPECTED_EMPTY_SHAPE


def test_table_data_counts_its_rows() -> None:
	"""
	Check the number of rows.

	.. versionadded:: 0.1.0
	"""
	table = TableData._create(FRAME)

	assert table.row_count == EXPECTED_ROW_COUNT


def test_table_data_counts_its_columns() -> None:
	"""
	Check the number of columns.

	.. versionadded:: 0.1.0
	"""
	table = TableData._create(FRAME)

	assert table.column_count == EXPECTED_COLUMN_COUNT


def test_table_data_counts_zero_columns_when_it_has_none() -> None:
	"""
	Check that a table without columns counts zero columns.

	.. versionadded:: 0.1.0
	"""
	table = TableData._create(NO_COLUMN_FRAME)

	assert table.column_count == 0


def test_table_data_gives_a_copy_of_its_column_names() -> None:
	"""
	Check the names, and that changing the returned list changes nothing.

	.. versionadded:: 0.1.0
	"""
	table = TableData._create(FRAME)
	column_names = table.column_names

	column_names.clear()

	assert table.column_names == EXPECTED_COLUMN_NAMES


def test_table_data_gives_the_type_of_each_column() -> None:
	"""
	Check the types by column name.

	.. versionadded:: 0.1.0
	"""
	table = TableData._create(FRAME)

	assert table.column_types == EXPECTED_COLUMN_TYPES


def test_from_frame_normalizes_the_columns() -> None:
	"""
	Check that numpy integers are stored as nullable integers.

	.. versionadded:: 0.1.0
	"""
	table = ExposedTableData.from_frame(RAW_FRAME)

	assert table.column_types == {"count": Type.INT64}


def test_wrap_keeps_the_class_of_the_table() -> None:
	"""
	Check that a wrapped table has the same class and the new columns.

	.. versionadded:: 0.1.0
	"""
	table = ExposedTableData._create(FRAME)

	wrapped_table = table.wrap(OTHER_FRAME)

	assert type(wrapped_table) is ExposedTableData
	assert wrapped_table.column_names == ["price"]


def test_read_column_gives_the_stored_column() -> None:
	"""
	Check that the stored column is returned.

	.. versionadded:: 0.1.0
	"""
	table = ExposedTableData._create(FRAME)

	column = table.read_column("price")

	stored_frame = table.read_frame()
	stored_column = stored_frame["price"]
	assert column.equals(stored_column)


def test_read_column_rejects_an_unknown_column() -> None:
	"""
	Check that an unknown column raises ColumnNotFoundError.

	.. versionadded:: 0.1.0
	"""
	table = ExposedTableData._create(FRAME)

	with pytest.raises(ColumnNotFoundError):
		table.read_column(UNKNOWN_COLUMN)


def test_table_data_gives_the_time_zone_of_each_datetime_column() -> None:
	"""
	Check that only the datetime column is listed, with its zone.

	.. versionadded:: 0.1.0
	"""
	table = TableData._create(TIME_FRAME)

	assert table.column_time_zones == EXPECTED_TIME_ZONES


def test_from_read_frame_cleans_the_column_names() -> None:
	"""
	Check that CLEANED removes the spaces and line breaks around each name.

	.. versionadded:: 0.1.0
	"""
	table = ExposedTableData.from_read_frame(SPACED_FRAME, ColumnNames.CLEANED)

	assert table.column_names == EXPECTED_CLEANED_NAMES


def test_from_read_frame_keeps_the_column_names() -> None:
	"""
	Check that KEPT leaves each name as written.

	.. versionadded:: 0.1.0
	"""
	table = ExposedTableData.from_read_frame(SPACED_FRAME, ColumnNames.KEPT)

	assert table.column_names == EXPECTED_KEPT_NAMES


def test_from_read_frame_reads_an_outside_duration_as_a_duration() -> None:
	"""
	Check that a pandas duration in microseconds becomes DURATION, not TIME.

	.. versionadded:: 0.1.0
	"""
	table = ExposedTableData.from_read_frame(MICROSECOND_WAIT_FRAME, ColumnNames.CLEANED)

	assert table.column_types == {"wait": Type.DURATION}


def test_read_stored_frame_keeps_the_storage_of_times() -> None:
	"""
	Check that a column of times stays in microseconds, unlike to_pandas.

	.. versionadded:: 0.1.0
	"""
	table = ExposedTableData.from_frame(HOUR_FRAME)

	stored_frame = read_stored_frame(table)

	hour_column = stored_frame["hour"]
	hour_dtype = str(hour_column.dtype)
	assert hour_dtype == HOUR_DTYPE_NAME
