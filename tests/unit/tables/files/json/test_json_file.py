"""
Unit tests of the reading and writing of JSON files.

.. versionadded:: 0.1.0
"""

from pathlib import Path

import pandas

from numdaplot.tables.files.json.json_file import read_json_file, read_json_lines, write_json_file
from numdaplot.tables.files.json.json_layout import JsonLayout
from numdaplot.tables.files.json.json_read_options import JsonReadOptions
from numdaplot.tables.files.json.json_write_options import JsonWriteOptions

FILE_NAME = "sales.json"
RECORDS_CONTENT = '[{"date": "2026-01-31", "count": 2}, {"date": "2026-02-01", "count": null}]'
EXPECTED_DATES = ["2026-01-31", "2026-02-01"]
EXPECTED_COUNTS = [2, None]
LINES_CONTENT = '{"price": 1}\n\n{"price": 2}\n'
EXPECTED_RECORDS = [{"price": 1}, {"price": 2}]
EXPECTED_LINE_PRICES = [1, 2]
OBJECT_DTYPE_NAME = "object"
WRITTEN_FRAME = {"city": ["Paris", None]}
EXPECTED_RECORDS_TEXT = '[{"city":"Paris"},{"city":null}]'
EXPECTED_LINES_TEXT = '{"city":"Paris"}\n{"city":null}\n'
ACCENTED_FRAME = {"city": ["B\u00e9ziers"]}
EXPECTED_ACCENTED_TEXT = '[{"city":"B\u00e9ziers"}]'
JSON_ENCODING = "utf-8"


def test_read_json_file_keeps_texts_that_look_like_dates(tmp_path: Path) -> None:
	"""
	Check that a column named date holding texts is not read as dates.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	path.write_text(RECORDS_CONTENT)

	frame = read_json_file(path, JsonReadOptions())

	date_column = frame["date"]
	dates = date_column.tolist()
	assert dates == EXPECTED_DATES


def test_read_json_file_keeps_python_objects(tmp_path: Path) -> None:
	"""
	Check that integers with a null stay Python objects, so a Table can read them as integers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	path.write_text(RECORDS_CONTENT)

	frame = read_json_file(path, JsonReadOptions())

	count_column = frame["count"]
	counts = count_column.tolist()
	dtype_name = str(count_column.dtype)
	assert counts == EXPECTED_COUNTS
	assert dtype_name == OBJECT_DTYPE_NAME


def test_read_json_file_reads_one_object_per_line(tmp_path: Path) -> None:
	"""
	Check that the LINES layout reads one row per line.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	path.write_text(LINES_CONTENT)
	options = JsonReadOptions(layout=JsonLayout.LINES)

	frame = read_json_file(path, options)

	price_column = frame["price"]
	prices = price_column.tolist()
	assert prices == EXPECTED_LINE_PRICES


def test_read_json_lines_skips_blank_lines() -> None:
	"""
	Check that blank lines give no object.

	.. versionadded:: 0.1.0
	"""
	records = read_json_lines(LINES_CONTENT)

	assert records == EXPECTED_RECORDS


def test_write_json_file_writes_one_list_of_objects(tmp_path: Path) -> None:
	"""
	Check the RECORDS text, missing values written as null.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	frame = pandas.DataFrame(WRITTEN_FRAME)

	write_json_file(frame, path, JsonWriteOptions())

	content = path.read_text()
	assert content == EXPECTED_RECORDS_TEXT


def test_write_json_file_writes_one_object_per_line(tmp_path: Path) -> None:
	"""
	Check the LINES text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	frame = pandas.DataFrame(WRITTEN_FRAME)
	options = JsonWriteOptions(layout=JsonLayout.LINES)

	write_json_file(frame, path, options)

	content = path.read_text()
	assert content == EXPECTED_LINES_TEXT


def test_write_json_file_keeps_accented_letters(tmp_path: Path) -> None:
	"""
	Check that accented letters are written as UTF-8, not escaped.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	frame = pandas.DataFrame(ACCENTED_FRAME)

	write_json_file(frame, path, JsonWriteOptions())

	content = path.read_text(encoding=JSON_ENCODING)
	assert content == EXPECTED_ACCENTED_TEXT
