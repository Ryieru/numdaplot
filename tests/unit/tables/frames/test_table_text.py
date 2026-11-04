"""
Unit tests of the text of a Table.

.. versionadded:: 0.1.0
"""

import pandas

from numdaplot.tables.frames.table_text import build_typed_frame, format_table

FRAME = pandas.DataFrame({"city": pandas.Series(["Pau"], dtype="string"), "price": [1.5]})
EXPECTED_HEADER = [("city", "TEXT"), ("price", "FLOAT64")]
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
