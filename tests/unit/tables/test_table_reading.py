"""
Unit tests of TableReading.

.. versionadded:: 0.1.0
"""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pandas
import pytest

from numdaplot.errors.file_not_found_error import FileNotFoundError
from numdaplot.tables import table_reading
from numdaplot.tables.files.csv_read_options import CsvReadOptions
from numdaplot.tables.files.excel_read_options import ExcelReadOptions
from numdaplot.tables.files.json_read_options import JsonReadOptions
from numdaplot.tables.files.sas_read_options import SasReadOptions
from numdaplot.tables.files.xpt_read_options import XptReadOptions
from numdaplot.tables.table_reading import TableReading

FILE_NAME = "sales.data"
FILE_CONTENT = "ignored"
FAKE_FRAME = pandas.DataFrame({"count": [1, 2]})
EXPECTED_COLUMN_NAMES = ["count"]
CSV_READER_NAME = "read_csv_file"
SEMICOLON = ";"
READERS_WITHOUT_OPTIONS = [
	("read_parquet_file", TableReading.from_parquet),
	("read_stata_file", TableReading.from_stata),
]


@dataclass(frozen=True)
class ReadingCase:
	"""
	A file format with options: its reader, its ``from_*`` method and its default options.

	.. versionadded:: 0.1.0

	Parameters
	----------
	reader_name
		The name of the file reader the method calls.
	read_table
		The ``from_*`` class method.
	default_options
		The options the method uses when none are given.
	"""

	reader_name: str
	read_table: Callable[[str], TableReading]
	default_options: object


READERS_WITH_OPTIONS = [
	ReadingCase(CSV_READER_NAME, TableReading.from_csv, CsvReadOptions()),
	ReadingCase("read_json_file", TableReading.from_json, JsonReadOptions()),
	ReadingCase("read_excel_file", TableReading.from_excel, ExcelReadOptions()),
	ReadingCase("read_sas_file", TableReading.from_sas, SasReadOptions()),
	ReadingCase("read_xpt_file", TableReading.from_xpt, XptReadOptions()),
]


class ReadRecorder:
	"""
	Fake file reader recording its arguments and returning a known DataFrame.

	.. versionadded:: 0.1.0
	"""

	def __init__(self) -> None:
		"""
		Start without any recorded call.

		.. versionadded:: 0.1.0
		"""
		self.paths = list[Path]()
		self.options = list[object]()

	def __call__(self, path: Path, options: object = None) -> pandas.DataFrame:
		"""
		Record the path and the options.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the file.
		options
			The settings of the file, when the format has some.

		Returns
		-------
		pandas.DataFrame
			Always the fake DataFrame.
		"""
		self.paths.append(path)
		self.options.append(options)

		return FAKE_FRAME


def write_file(folder: Path) -> Path:
	"""
	Write a file to read and return its path.

	.. versionadded:: 0.1.0

	Parameters
	----------
	folder
		A temporary folder.

	Returns
	-------
	Path
		The path of the file.
	"""
	path = folder / FILE_NAME
	path.write_text(FILE_CONTENT)

	return path


@pytest.mark.parametrize("reading_case", READERS_WITH_OPTIONS)
def test_reading_uses_the_default_options_of_the_format(
	monkeypatch: pytest.MonkeyPatch,
	tmp_path: Path,
	reading_case: ReadingCase,
) -> None:
	"""
	Check that each format with options reads its file with the default options, as a normalized Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the file reader with a fake.
	tmp_path
		A temporary folder.
	reading_case
		The format, its reader, its method and its default options.
	"""
	recorder = ReadRecorder()
	monkeypatch.setattr(table_reading, reading_case.reader_name, recorder)
	path = write_file(tmp_path)
	path_text = str(path)

	table = reading_case.read_table(path_text)

	assert recorder.paths == [path]
	assert recorder.options == [reading_case.default_options]
	assert table.column_names == EXPECTED_COLUMN_NAMES


@pytest.mark.parametrize(("reader_name", "read_table"), READERS_WITHOUT_OPTIONS)
def test_reading_accepts_formats_without_options(
	monkeypatch: pytest.MonkeyPatch,
	tmp_path: Path,
	reader_name: str,
	read_table: Callable[[Path], TableReading],
) -> None:
	"""
	Check that Parquet and Stata files are read from their path.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the file reader with a fake.
	tmp_path
		A temporary folder.
	reader_name
		The name of the file reader.
	read_table
		The ``from_*`` class method.
	"""
	recorder = ReadRecorder()
	monkeypatch.setattr(table_reading, reader_name, recorder)
	path = write_file(tmp_path)

	table = read_table(path)

	assert recorder.paths == [path]
	assert table.column_names == EXPECTED_COLUMN_NAMES


def test_reading_passes_the_given_options(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
	"""
	Check that given options reach the file reader.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the file reader with a fake.
	tmp_path
		A temporary folder.
	"""
	recorder = ReadRecorder()
	monkeypatch.setattr(table_reading, CSV_READER_NAME, recorder)
	path = write_file(tmp_path)
	options = CsvReadOptions(separator=SEMICOLON)

	TableReading.from_csv(path, options)

	assert recorder.options == [options]


def test_reading_rejects_a_missing_file(tmp_path: Path) -> None:
	"""
	Check that a missing file raises FileNotFoundError before any reading.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME

	with pytest.raises(FileNotFoundError):
		TableReading.from_csv(path)
