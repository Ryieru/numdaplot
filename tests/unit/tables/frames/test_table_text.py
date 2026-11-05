"""
Unit tests of the text of a Table.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

from numdaplot.tables.frames.table_text import build_typed_frame, format_table
from numdaplot.tables.preview.shown_columns import ShownColumns

FRAME = pandas.DataFrame({"city": pandas.Series(["Pau"], dtype="string"), "price": [1.5]})
EXPECTED_HEADER = [("city", "TEXT"), ("price", "FLOAT64")]
LONG_NAME = "long_column_name_"
WIDE_COLUMN_COUNT = 30
WIDE_FRAME = pandas.DataFrame({f"{LONG_NAME}{number}": [float(number)] for number in range(WIDE_COLUMN_COUNT)})
COMPACT_MARK = "..."
TERMINAL_WIDTH_VARIABLE = "COLUMNS"
NARROW_TERMINAL_WIDTH = 60
MAX_COLUMNS_OPTION = "display.max_columns"
USER_COLUMN_LIMIT = 2
EXPECTED_TEXT_LINES = ["city   price", "TEXT FLOAT64", "0  Pau     1.5"]
EXPECTED_COLUMN_NAMES = ["city", "price"]
PARIS_TIMES = (
	pandas.Series(pandas.to_datetime(["2026-07-01 10:30"])).astype("datetime64[ns]").dt.tz_localize("Europe/Paris")
)
EXPECTED_ZONE_HEADER = [("time", "DATETIME Europe/Paris")]


def test_build_typed_frame_puts_the_type_under_each_name() -> None:
	"""
	Check the two-level header of names and types.

	.. versionadded:: 0.1.0
	"""
	typed_frame = build_typed_frame(FRAME)

	header = typed_frame.columns.tolist()
	assert header == EXPECTED_HEADER


def test_build_typed_frame_does_not_change_the_columns() -> None:
	"""
	Check that the given DataFrame keeps its column names.

	.. versionadded:: 0.1.0
	"""
	build_typed_frame(FRAME)

	column_names = FRAME.columns.tolist()
	assert column_names == EXPECTED_COLUMN_NAMES


def test_format_table_shows_names_types_and_rows() -> None:
	"""
	Check each line of the text, without the alignment spaces.

	.. versionadded:: 0.1.0
	"""
	table_text = format_table(FRAME)

	text_lines = table_text.splitlines()
	stripped_lines = [text_line.strip() for text_line in text_lines]
	assert stripped_lines == EXPECTED_TEXT_LINES


def test_build_typed_frame_shows_the_time_zone_after_the_type() -> None:
	"""
	Check the header of a datetime column with a zone.

	.. versionadded:: 0.1.0
	"""
	time_frame = pandas.DataFrame({"time": PARIS_TIMES})

	typed_frame = build_typed_frame(time_frame)

	header = typed_frame.columns.tolist()
	assert header == EXPECTED_ZONE_HEADER


def test_format_table_shows_every_column_by_default() -> None:
	"""
	Check that no column of a wide frame is replaced by dots.

	.. versionadded:: 0.1.0
	"""
	table_text = format_table(WIDE_FRAME)

	assert table_text.count(LONG_NAME) == WIDE_COLUMN_COUNT
	assert COMPACT_MARK not in table_text


def test_format_table_breaks_the_lines_at_the_terminal_width(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that no line goes beyond the width of the terminal.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Sets the width of the terminal.
	"""
	monkeypatch.setenv(TERMINAL_WIDTH_VARIABLE, str(NARROW_TERMINAL_WIDTH))

	table_text = format_table(WIDE_FRAME)

	line_widths = [len(text_line) for text_line in table_text.splitlines()]
	assert max(line_widths) <= NARROW_TERMINAL_WIDTH


def test_format_table_replaces_the_columns_that_do_not_fit_when_compact() -> None:
	"""
	Check that a compact text keeps some columns and marks the others.

	.. versionadded:: 0.1.0
	"""
	table_text = format_table(WIDE_FRAME, ShownColumns.COMPACT)

	assert table_text.count(LONG_NAME) < WIDE_COLUMN_COUNT
	assert COMPACT_MARK in table_text


def test_format_table_keeps_a_narrow_frame_identical_in_both_modes() -> None:
	"""
	Check that the setting only matters when the columns do not fit.

	.. versionadded:: 0.1.0
	"""
	every_column_text = format_table(FRAME, ShownColumns.ALL)
	compact_text = format_table(FRAME, ShownColumns.COMPACT)

	assert every_column_text == compact_text


def test_format_table_ignores_the_pandas_settings_of_the_user() -> None:
	"""
	Check that a limit set in pandas does not hide columns.

	.. versionadded:: 0.1.0
	"""
	with pandas.option_context(MAX_COLUMNS_OPTION, USER_COLUMN_LIMIT):
		table_text = format_table(WIDE_FRAME)

	assert table_text.count(LONG_NAME) == WIDE_COLUMN_COUNT
