"""
Unit tests of the text of a Table.

.. versionadded:: 0.1.0
"""

import numpy
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
SHOWN_TIME_FRAME = pandas.DataFrame({"hour": pandas.Series(numpy.array([56100000000, "NaT"], dtype="timedelta64[us]"))})
EXPECTED_TIME_TABLE = "       hour\n       TIME\n0  15:35:00\n1       NaT"


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


def test_format_table_keeps_the_header_of_a_table_without_rows() -> None:
	"""
	Check the names, the types and the note of a Table without rows, without any pandas word.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame({"price": pandas.Series(dtype="float64"), "city": pandas.Series(dtype="string")})

	table_text = format_table(frame)

	lines = table_text.splitlines()
	assert lines[0].split() == ["price", "city"]
	assert lines[1].split() == ["FLOAT64", "TEXT"]
	assert lines[2] == "(0 rows)"
	assert len(lines) == 3


def test_format_table_notes_a_table_without_columns() -> None:
	"""
	Check the single line of a Table without columns.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame(index=[0, 1])

	table_text = format_table(frame)

	assert table_text == "(no columns, 2 rows)"


def test_format_table_writes_one_row_without_columns() -> None:
	"""
	Check the singular of the note.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame(index=[0])

	table_text = format_table(frame)

	assert table_text == "(no columns, 1 row)"


def test_format_table_keeps_a_table_with_rows_unchanged() -> None:
	"""
	Check that a Table with values has no note.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame({"price": [1.5]})

	table_text = format_table(frame)

	assert "rows)" not in table_text


def test_format_table_wraps_the_wide_header_of_a_table_without_rows(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that every name stays visible, and no blank row remains, when the header goes on after a line break.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Sets the width of the terminal.
	"""
	monkeypatch.setenv("COLUMNS", "40")
	names = [f"long_column_name_{number}" for number in range(6)]
	frame = pandas.DataFrame({name: pandas.Series(dtype="float64") for name in names})

	table_text = format_table(frame)

	for name in names:
		assert name in table_text

	lines = table_text.splitlines()
	assert lines[-1] == "(0 rows)"
	assert not any(line.startswith("0") for line in lines)


def test_format_table_compacts_the_wide_header_without_dimensions(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check the compact header of a Table without rows, which gives no count of a blank row.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Sets the width of the terminal.
	"""
	monkeypatch.setenv("COLUMNS", "40")
	names = [f"long_column_name_{number}" for number in range(6)]
	frame = pandas.DataFrame({name: pandas.Series(dtype="float64") for name in names})

	table_text = format_table(frame, ShownColumns.COMPACT)

	assert "..." in table_text
	assert "1 rows" not in table_text
	assert table_text.splitlines()[-1] == "(0 rows)"


def test_format_table_writes_times_of_day() -> None:
	"""
	Check that a column of times is shown as 15:35:00, NaT where missing.

	.. versionadded:: 0.1.0
	"""
	table_text = format_table(SHOWN_TIME_FRAME)

	assert table_text == EXPECTED_TIME_TABLE
