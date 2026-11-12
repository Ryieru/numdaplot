"""
Unit tests of TableExchange.

.. versionadded:: 0.1.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

from datetime import datetime
from zoneinfo import ZoneInfo

import pandas
import pytest

from numdaplot.arrays.array import Array
from numdaplot.arrays.equality import Equality
from numdaplot.arrays.type_match import TypeMatch
from numdaplot.data_types.type import Type
from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.errors.not_single_value_error import NotSingleValueError
from numdaplot.errors.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.tables import table_exchange
from numdaplot.tables.table import Table
from numdaplot.tables.table_exchange import TableExchange

SOURCE_FRAME = {"count": [1, 2]}
CHANGED_COUNT = 99
EXPECTED_COUNTS = [1, 2]
PRICES = Array.from_list([1.5, 8.0])
EXPECTED_PRICES = [1.5, 8.0]
FRAME = pandas.DataFrame({"price": [1.5, 8.0]})
SINGLE_PRICE = pandas.DataFrame({"price": [1.5]})
SINGLE_PRICE_VALUE = 1.5
MISSING_COUNT = pandas.DataFrame({"count": pandas.Series([None], dtype="Int64")})
EXPECTED_VALUE_COUNT = 2
FAKE_TEXT = "fake table text"
FORMAT_TABLE_NAME = "format_table"
FORMAT_TABLE_HTML_NAME = "format_table_html"
FAKE_HTML = "<table>fake</table>"
ARE_FRAMES_EQUAL_NAME = "are_frames_equal"
PARIS_TIMES = (
	pandas.Series(pandas.to_datetime(["2026-07-01 10:30"])).astype("datetime64[ns]").dt.tz_localize("Europe/Paris")
)
TIME_FRAME = pandas.DataFrame({"time": PARIS_TIMES})
EXPECTED_PARIS_TIME = datetime(2026, 7, 1, 10, 30, tzinfo=ZoneInfo("Europe/Paris"))
TIME_COLUMN = "time"


class EqualityRecorder:
	"""
	Fake frame comparison recording its type setting.

	.. versionadded:: 0.1.0
	"""

	def __init__(self) -> None:
		"""
		Start without any recorded call.

		.. versionadded:: 0.1.0
		"""
		self.types = list[TypeMatch]()

	def __call__(self, left: pandas.DataFrame, right: pandas.DataFrame, types: TypeMatch) -> bool:
		"""
		Record the type setting and answer that the frames are equal.

		.. versionadded:: 0.1.0

		Parameters
		----------
		left
			The first frame.
		right
			The second frame.
		types
			Whether the types must be the same.

		Returns
		-------
		bool
			Always True.
		"""
		self.types.append(types)

		return True


def test_from_pandas_copies_the_dataframe() -> None:
	"""
	Check that changing the DataFrame afterwards does not change the Table.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame(SOURCE_FRAME)
	table = TableExchange.from_pandas(frame)

	frame.loc[0, "count"] = CHANGED_COUNT

	counts = table.column("count")
	count_list = counts.to_list()
	assert count_list == EXPECTED_COUNTS


def test_from_arrays_builds_one_column_per_array() -> None:
	"""
	Check the type of a column built from an Array.

	.. versionadded:: 0.1.0
	"""
	table = TableExchange.from_arrays({"price": PRICES})

	assert table.column_types == {"price": Type.FLOAT64}


def test_to_pandas_gives_a_copy() -> None:
	"""
	Check that changing the returned DataFrame does not change the Table.

	.. versionadded:: 0.1.0
	"""
	table = TableExchange._create(FRAME)
	frame = table.to_pandas()

	frame.loc[0, "price"] = CHANGED_COUNT

	prices = table.column("price")
	price_list = prices.to_list()
	assert price_list == EXPECTED_PRICES


def test_column_gives_an_array_of_the_column() -> None:
	"""
	Check the values of the Array.

	.. versionadded:: 0.1.0
	"""
	table = TableExchange._create(FRAME)

	prices = table.column("price")

	price_list = prices.to_list()
	assert price_list == EXPECTED_PRICES


def test_to_value_reads_the_single_value() -> None:
	"""
	Check the value of a Table of one row and one column.

	.. versionadded:: 0.1.0
	"""
	table = TableExchange._create(SINGLE_PRICE)

	value = table.to_value()

	assert value == SINGLE_PRICE_VALUE


def test_to_value_gives_none_for_a_missing_value() -> None:
	"""
	Check that a missing integer gives None.

	.. versionadded:: 0.1.0
	"""
	table = TableExchange._create(MISSING_COUNT)

	value = table.to_value()

	assert value is None


def test_to_value_rejects_several_values() -> None:
	"""
	Check that two values raise NotSingleValueError.

	.. versionadded:: 0.1.0
	"""
	table = TableExchange._create(FRAME)

	with pytest.raises(NotSingleValueError) as error_info:
		table.to_value()

	error = error_info.value
	assert error.value_count == EXPECTED_VALUE_COUNT


def test_is_equal_compares_the_frames_with_the_type_setting(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the comparison receives the type setting of the Equality.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the frame comparison with a fake.
	"""
	recorder = EqualityRecorder()
	monkeypatch.setattr(table_exchange, ARE_FRAMES_EQUAL_NAME, recorder)
	table = TableExchange._create(FRAME)
	other_table = Table._create(FRAME)
	equality = Equality(other=other_table, types=TypeMatch.STRICT)

	is_equal = table.is_equal(equality)

	assert is_equal
	assert recorder.types == [TypeMatch.STRICT]


def test_is_equal_rejects_an_array() -> None:
	"""
	Check that comparing a Table with an Array raises InvalidTypeError.

	.. versionadded:: 0.1.0
	"""
	table = TableExchange._create(FRAME)
	equality = Equality(other=PRICES)

	with pytest.raises(InvalidTypeError):
		table.is_equal(equality)


def test_to_value_keeps_the_time_zone_of_a_datetime() -> None:
	"""
	Check that the single datetime of a zone column keeps its zone.

	.. versionadded:: 0.1.0
	"""
	table = TableExchange._create(TIME_FRAME)

	single_value = table.to_value()

	assert single_value == EXPECTED_PARIS_TIME
	assert single_value.tzinfo is not None


def test_column_rejects_a_datetime_column_with_a_time_zone() -> None:
	"""
	Check that a zone column cannot become an Array.

	.. versionadded:: 0.1.0
	"""
	table = TableExchange._create(TIME_FRAME)

	with pytest.raises(TimeZoneMismatchError):
		table.column(TIME_COLUMN)
