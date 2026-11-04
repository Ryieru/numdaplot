"""
Unit tests of TableData.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

from numdaplot.data_types.type import Type
from numdaplot.dates.time_zone import TimeZone
from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.tables.frames.column import Column
from numdaplot.tables.table_data import TableData

FRAME = pandas.DataFrame({"city": pandas.Series(["Pau", "Lyon"], dtype="string"), "price": [1.5, 8.0]})
EXPECTED_ROW_COUNT = 2
EXPECTED_COLUMN_NAMES = ["city", "price"]
EXPECTED_COLUMN_TYPES = {"city": Type.TEXT, "price": Type.FLOAT64}
RAW_FRAME = pandas.DataFrame({"count": [1, 2]})
INTEGER_DTYPE_NAME = "Int64"
OTHER_FRAME = pandas.DataFrame({"price": [3.0]})
UNKNOWN_COLUMN = "prise"
PARIS_TIMES = (
	pandas.Series(pandas.to_datetime(["2026-07-01 10:30"])).astype("datetime64[ns]").dt.tz_localize("Europe/Paris")
)
TIME_FRAME = pandas.DataFrame({"time": PARIS_TIMES, "price": [1.5]})
EXPECTED_TIME_ZONES = {"time": TimeZone("Europe/Paris")}


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


def test_table_data_counts_its_rows() -> None:
	"""
	Check the number of rows.

	.. versionadded:: 0.1.0
	"""
	table = TableData(FRAME)

	assert table.row_count == EXPECTED_ROW_COUNT


def test_table_data_gives_a_copy_of_its_column_names() -> None:
	"""
	Check the names, and that changing the returned list changes nothing.

	.. versionadded:: 0.1.0
	"""
	table = TableData(FRAME)
	column_names = table.column_names

	column_names.clear()

	assert table.column_names == EXPECTED_COLUMN_NAMES


def test_table_data_gives_the_type_of_each_column() -> None:
	"""
	Check the types by column name.

	.. versionadded:: 0.1.0
	"""
	table = TableData(FRAME)

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
	table = ExposedTableData(FRAME)

	wrapped_table = table.wrap(OTHER_FRAME)

	assert type(wrapped_table) is ExposedTableData
	assert wrapped_table.column_names == ["price"]


def test_read_column_gives_the_stored_column() -> None:
	"""
	Check that the stored column is returned.

	.. versionadded:: 0.1.0
	"""
	table = ExposedTableData(FRAME)

	column = table.read_column("price")

	stored_frame = table.read_frame()
	stored_column = stored_frame["price"]
	assert column.equals(stored_column)


def test_read_column_rejects_an_unknown_column() -> None:
	"""
	Check that an unknown column raises ColumnNotFoundError.

	.. versionadded:: 0.1.0
	"""
	table = ExposedTableData(FRAME)

	with pytest.raises(ColumnNotFoundError):
		table.read_column(UNKNOWN_COLUMN)


def test_table_data_gives_the_time_zone_of_each_datetime_column() -> None:
	"""
	Check that only the datetime column is listed, with its zone.

	.. versionadded:: 0.1.0
	"""
	table = TableData(TIME_FRAME)

	assert table.column_time_zones == EXPECTED_TIME_ZONES
