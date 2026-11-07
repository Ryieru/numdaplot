"""
Writing of a Table in a file.

.. versionadded:: 0.1.0
"""

from pathlib import Path

from numdaplot.settings.argument_types import checked_arguments
from numdaplot.tables.conflict import Conflict
from numdaplot.tables.files.csv_file import write_csv_file
from numdaplot.tables.files.csv_write_options import CsvWriteOptions
from numdaplot.tables.files.excel_file import write_excel_file
from numdaplot.tables.files.excel_write_options import ExcelWriteOptions
from numdaplot.tables.files.file_access import WRITE_OPERATION, FileAccessErrors
from numdaplot.tables.files.file_paths import FilePath, require_free_path
from numdaplot.tables.files.json_file import write_json_file
from numdaplot.tables.files.json_write_options import JsonWriteOptions
from numdaplot.tables.files.parquet_file import write_parquet_file
from numdaplot.tables.files.stata_file import write_stata_file
from numdaplot.tables.frames.time_columns import read_time_objects_frame, write_time_texts_frame
from numdaplot.tables.table_data import TableData


class TableWriting(TableData):
	"""
	Writing of a Table in a CSV, JSON, Excel, Parquet or Stata file.

	An existing file is never overwritten unless ``on_conflict`` is ``Conflict.REPLACE``.

	.. versionadded:: 0.1.0
	"""

	@checked_arguments
	def to_csv(
		self, path: FilePath, options: CsvWriteOptions | None = None, on_conflict: Conflict = Conflict.ERROR
	) -> None:
		"""
		Write the Table in a CSV file, column names on the first row, without row numbers.

		Missing values are written as empty values, and times of day as texts such as ``15:35:00``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the file, a ``FilePath`` such as ``"sales.csv"`` or ``Path("data/sales.csv")``.
		options
			The separator and the encoding, ``","`` and UTF-8 when omitted.
		on_conflict
			``ERROR`` by default, refusing to overwrite an existing file, or ``REPLACE`` to overwrite it.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		FileExistsError
			When a file exists at the path and ``on_conflict`` is ``ERROR``.
		FileAccessError
			When the file system refuses the file: missing folder, missing permission and so on.

		Examples
		--------
		>>> import tempfile
		>>> from pathlib import Path
		>>> import numdaplot as ndp
		>>> path = Path(tempfile.mkdtemp()) / "sales.csv"
		>>> table = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5, 8.0])})
		>>> table.to_csv(path, ndp.CsvWriteOptions(separator=";"))
		>>> print(path.read_text())
		price
		1.5
		8.0
		<BLANKLINE>
		"""
		file_path = Path(path)
		require_free_path(file_path, on_conflict)
		if options is None:
			options = CsvWriteOptions()

		with FileAccessErrors(WRITE_OPERATION, file_path):
			write_csv_file(write_time_texts_frame(self._frame), file_path, options)

	@checked_arguments
	def to_json(
		self, path: FilePath, options: JsonWriteOptions | None = None, on_conflict: Conflict = Conflict.ERROR
	) -> None:
		"""
		Write the Table in a JSON file in UTF-8, one object per row.

		Missing values are written as ``null``, dates and durations in the ISO 8601 format, times of day as texts such
		as ``15:35:00``, and decimals with every digit of their value unless ``options`` gives their number.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the file, a ``FilePath`` such as ``"sales.json"`` or ``Path("data/sales.json")``.
		options
			The layout of the rows and the number of decimals, one list of objects with every digit when omitted.
		on_conflict
			``ERROR`` by default, refusing to overwrite an existing file, or ``REPLACE`` to overwrite it.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		FileExistsError
			When a file exists at the path and ``on_conflict`` is ``ERROR``.
		FileAccessError
			When the file system refuses the file: missing folder, missing permission and so on.
		ValueConversionError
			At the first infinite value of a decimal column, which JSON cannot write: replace it first.

		Examples
		--------
		>>> import tempfile
		>>> from pathlib import Path
		>>> import numdaplot as ndp
		>>> path = Path(tempfile.mkdtemp()) / "sales.json"
		>>> ndp.Table.from_arrays({"city": ndp.Array.from_list(["Paris"])}).to_json(path)
		>>> path.read_text()
		'[{"city":"Paris"}]'
		"""
		file_path = Path(path)
		require_free_path(file_path, on_conflict)
		if options is None:
			options = JsonWriteOptions()

		with FileAccessErrors(WRITE_OPERATION, file_path):
			write_json_file(write_time_texts_frame(self._frame), file_path, options)

	@checked_arguments
	def to_excel(
		self, path: FilePath, options: ExcelWriteOptions | None = None, on_conflict: Conflict = Conflict.ERROR
	) -> None:
		"""
		Write the Table in a sheet of an Excel file, column names on the first row.

		Times of day are written as texts such as ``15:35:00``. Needs the ``excel`` extra:
		``pip install numdaplot[excel]``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the file, a ``FilePath`` such as ``"sales.xlsx"`` or ``Path("data/sales.xlsx")``.
		options
			The name of the sheet, ``"Sheet1"`` when omitted.
		on_conflict
			``ERROR`` by default, refusing to overwrite an existing file, or ``REPLACE`` to overwrite it.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		FileExistsError
			When a file exists at the path and ``on_conflict`` is ``ERROR``.
		FileAccessError
			When the file system refuses the file: missing folder, missing permission and so on.
		MissingDependencyError
			When the ``excel`` extra is not installed.

		Examples
		--------
		>>> import tempfile
		>>> from pathlib import Path
		>>> import numdaplot as ndp
		>>> path = Path(tempfile.mkdtemp()) / "sales.xlsx"
		>>> table = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5])})
		>>> table.to_excel(path, ndp.ExcelWriteOptions(sheet="Sales"))
		>>> ndp.Table.from_excel(path, ndp.ExcelReadOptions(sheet="Sales")).row_count
		1
		"""
		file_path = Path(path)
		require_free_path(file_path, on_conflict)
		if options is None:
			options = ExcelWriteOptions()

		with FileAccessErrors(WRITE_OPERATION, file_path):
			write_excel_file(write_time_texts_frame(self._frame), file_path, options)

	@checked_arguments
	def to_parquet(self, path: FilePath, on_conflict: Conflict = Conflict.ERROR) -> None:
		"""
		Write the Table in a Parquet file, which keeps the type of each column.

		Times of day are stored as Parquet times, read back as ``TIME``. Needs the ``parquet`` extra:
		``pip install numdaplot[parquet]``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the file, a ``FilePath`` such as ``"sales.parquet"`` or ``Path("data/sales.parquet")``.
		on_conflict
			``ERROR`` by default, refusing to overwrite an existing file, or ``REPLACE`` to overwrite it.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		FileExistsError
			When a file exists at the path and ``on_conflict`` is ``ERROR``.
		FileAccessError
			When the file system refuses the file: missing folder, missing permission and so on.
		MissingDependencyError
			When the ``parquet`` extra is not installed.

		Examples
		--------
		>>> import tempfile
		>>> from pathlib import Path
		>>> import numdaplot as ndp
		>>> path = Path(tempfile.mkdtemp()) / "sales.parquet"
		>>> ndp.Table.from_arrays({"count": ndp.Array.from_list([3])}).to_parquet(path)
		>>> path.exists()
		True
		"""
		file_path = Path(path)
		require_free_path(file_path, on_conflict)
		with FileAccessErrors(WRITE_OPERATION, file_path):
			write_parquet_file(read_time_objects_frame(self._frame), file_path)

	@checked_arguments
	def to_stata(self, path: FilePath, on_conflict: Conflict = Conflict.ERROR) -> None:
		"""
		Write the Table in a Stata file (``.dta``).

		Stata stores integers and booleans holding missing values as decimals, a missing text as an empty text, and
		times of day as texts such as ``15:35:00``, as it has no type for them. Column names that Stata refuses, such
		as names with spaces, are changed by pandas with a warning.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the file, a ``FilePath`` such as ``"sales.dta"`` or ``Path("data/sales.dta")``.
		on_conflict
			``ERROR`` by default, refusing to overwrite an existing file, or ``REPLACE`` to overwrite it.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		FileExistsError
			When a file exists at the path and ``on_conflict`` is ``ERROR``.
		FileAccessError
			When the file system refuses the file: missing folder, missing permission and so on.

		Examples
		--------
		>>> import tempfile
		>>> from pathlib import Path
		>>> import numdaplot as ndp
		>>> path = Path(tempfile.mkdtemp()) / "sales.dta"
		>>> ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5])}).to_stata(path)
		>>> path.exists()
		True
		"""
		file_path = Path(path)
		require_free_path(file_path, on_conflict)
		with FileAccessErrors(WRITE_OPERATION, file_path):
			write_stata_file(write_time_texts_frame(self._frame), file_path)
