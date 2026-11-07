"""
Unit tests of TableWriting.

.. versionadded:: 0.1.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pandas
import pytest

from numdaplot.errors.file_exists_error import FileExistsError
from numdaplot.tables import table_writing
from numdaplot.tables.conflict import Conflict
from numdaplot.tables.files.csv_write_options import CsvWriteOptions
from numdaplot.tables.files.excel_write_options import ExcelWriteOptions
from numdaplot.tables.files.json_write_options import JsonWriteOptions
from numdaplot.tables.table_writing import TableWriting

FILE_NAME = "sales.data"
FILE_CONTENT = "existing"
FRAME = pandas.DataFrame({"price": [1.5]})
CSV_WRITER_NAME = "write_csv_file"
WRITERS_WITHOUT_OPTIONS = [
	("write_parquet_file", TableWriting.to_parquet),
	("write_stata_file", TableWriting.to_stata),
]


@dataclass(frozen=True)
class WritingCase:
	"""
	A file format with options: its writer, its ``to_*`` method and its default options.

	.. versionadded:: 0.1.0

	Parameters
	----------
	writer_name
		The name of the file writer the method calls.
	write_table
		The ``to_*`` method.
	default_options
		The options the method uses when none are given.
	"""

	writer_name: str
	write_table: Callable[[TableWriting, str], None]
	default_options: object


WRITERS_WITH_OPTIONS = [
	WritingCase(CSV_WRITER_NAME, TableWriting.to_csv, CsvWriteOptions()),
	WritingCase("write_json_file", TableWriting.to_json, JsonWriteOptions()),
	WritingCase("write_excel_file", TableWriting.to_excel, ExcelWriteOptions()),
]


class WriteRecorder:
	"""
	Fake file writer recording its arguments.

	.. versionadded:: 0.1.0
	"""

	def __init__(self) -> None:
		"""
		Start without any recorded call.

		.. versionadded:: 0.1.0
		"""
		self.frames = list[pandas.DataFrame]()
		self.paths = list[Path]()
		self.options = list[object]()

	def __call__(self, frame: pandas.DataFrame, path: Path, options: object = None) -> None:
		"""
		Record the columns, the path and the options.

		.. versionadded:: 0.1.0

		Parameters
		----------
		frame
			The columns to write.
		path
			The path of the file.
		options
			The settings of the file, when the format has some.
		"""
		self.frames.append(frame)
		self.paths.append(path)
		self.options.append(options)


@pytest.mark.parametrize("writing_case", WRITERS_WITH_OPTIONS)
def test_writing_uses_the_default_options_of_the_format(
	monkeypatch: pytest.MonkeyPatch,
	tmp_path: Path,
	writing_case: WritingCase,
) -> None:
	"""
	Check that each format with options writes the columns with the default options.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the file writer with a fake.
	tmp_path
		A temporary folder.
	writing_case
		The format, its writer, its method and its default options.
	"""
	recorder = WriteRecorder()
	monkeypatch.setattr(table_writing, writing_case.writer_name, recorder)
	table = TableWriting._create(FRAME)
	path = tmp_path / FILE_NAME
	path_text = str(path)

	writing_case.write_table(table, path_text)

	assert recorder.frames == [FRAME]
	assert recorder.paths == [path]
	assert recorder.options == [writing_case.default_options]


@pytest.mark.parametrize(("writer_name", "write_table"), WRITERS_WITHOUT_OPTIONS)
def test_writing_accepts_formats_without_options(
	monkeypatch: pytest.MonkeyPatch,
	tmp_path: Path,
	writer_name: str,
	write_table: Callable[[TableWriting, Path], None],
) -> None:
	"""
	Check that Parquet and Stata files are written at their path.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the file writer with a fake.
	tmp_path
		A temporary folder.
	writer_name
		The name of the file writer.
	write_table
		The ``to_*`` method.
	"""
	recorder = WriteRecorder()
	monkeypatch.setattr(table_writing, writer_name, recorder)
	table = TableWriting._create(FRAME)
	path = tmp_path / FILE_NAME

	write_table(table, path)

	assert recorder.paths == [path]


def test_writing_refuses_to_overwrite_a_file_by_default(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
	"""
	Check that an existing file raises FileExistsError and nothing is written.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the file writer with a fake.
	tmp_path
		A temporary folder.
	"""
	recorder = WriteRecorder()
	monkeypatch.setattr(table_writing, CSV_WRITER_NAME, recorder)
	table = TableWriting._create(FRAME)
	path = tmp_path / FILE_NAME
	path.write_text(FILE_CONTENT)

	with pytest.raises(FileExistsError):
		table.to_csv(path)

	assert recorder.paths == []


def test_writing_overwrites_a_file_to_replace(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
	"""
	Check that Conflict.REPLACE writes over an existing file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the file writer with a fake.
	tmp_path
		A temporary folder.
	"""
	recorder = WriteRecorder()
	monkeypatch.setattr(table_writing, CSV_WRITER_NAME, recorder)
	table = TableWriting._create(FRAME)
	path = tmp_path / FILE_NAME
	path.write_text(FILE_CONTENT)

	table.to_csv(path, on_conflict=Conflict.REPLACE)

	assert recorder.paths == [path]
