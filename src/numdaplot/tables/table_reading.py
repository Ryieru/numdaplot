"""
Creation of a Table from a file.

.. versionadded:: 0.1.0
"""

from pathlib import Path
from typing import Self

from numdaplot.tables.files.csv_file import read_csv_file
from numdaplot.tables.files.csv_options import CsvOptions
from numdaplot.tables.files.excel_file import read_excel_file
from numdaplot.tables.files.excel_options import ExcelOptions
from numdaplot.tables.files.file_paths import FilePath, require_existing_file
from numdaplot.tables.files.json_file import read_json_file
from numdaplot.tables.files.json_options import JsonOptions
from numdaplot.tables.files.parquet_file import read_parquet_file
from numdaplot.tables.files.sas_file import read_sas_file, read_xpt_file
from numdaplot.tables.files.sas_options import SasOptions
from numdaplot.tables.files.stata_file import read_stata_file
from numdaplot.tables.files.xpt_options import XptOptions
from numdaplot.tables.table_data import TableData


class TableReading(TableData):
	"""
	Creation of a Table from a CSV, JSON, Excel, Parquet, Stata, SAS or XPT file.

	Integers become ``INT64``, decimals ``FLOAT64`` and true or false values ``BOOL``. Any other column of a CSV
	or JSON file becomes ``TEXT``, dates included: convert them afterwards. Empty cells and the usual markers
	such as ``NA`` or ``null`` are read as missing values.

	.. versionadded:: 0.1.0
	"""

	@classmethod
	def from_csv(cls, path: FilePath, options: CsvOptions | None = None) -> Self:
		r"""
		Return a Table read from a CSV file whose first row holds the column names.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the file.
		options
			The separator and the encoding, ``,`` and UTF-8 by default.

		Returns
		-------
		Self
			A new Table, empty for an empty file.

		Raises
		------
		FileNotFoundError
			When there is no file at the path.
		InvalidColumnNameError, DuplicateColumnError
			When a column name is empty or appears twice.

		Examples
		--------
		>>> import tempfile
		>>> from pathlib import Path
		>>> import numdaplot as ndp
		>>> path = Path(tempfile.mkdtemp()) / "sales.csv"
		>>> _ = path.write_text("city;price\nParis;1.5\nLyon;\n")
		>>> ndp.Table.from_csv(path, ndp.CsvOptions(separator=";"))
		city   price
		TEXT FLOAT64
		0  Paris     1.5
		1   Lyon     NaN
		"""
		file_path = Path(path)
		require_existing_file(file_path)
		if options is None:
			options = CsvOptions()

		frame = read_csv_file(file_path, options)
		table = cls._from_frame(frame)

		return table

	@classmethod
	def from_json(cls, path: FilePath, options: JsonOptions | None = None) -> Self:
		r"""
		Return a Table read from a JSON file in UTF-8 holding one object per row.

		Each column takes the type of its JSON values: a text that looks like a number or a date stays a text.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the file.
		options
			The layout of the rows, one list of objects by default.

		Returns
		-------
		Self
			A new Table, with one column per name found in the objects.

		Raises
		------
		FileNotFoundError
			When there is no file at the path.
		InvalidColumnNameError
			When a column name is empty.

		Examples
		--------
		>>> import tempfile
		>>> from pathlib import Path
		>>> import numdaplot as ndp
		>>> path = Path(tempfile.mkdtemp()) / "sales.jsonl"
		>>> _ = path.write_text('{"city": "Paris", "count": 2}\n{"city": "Lyon", "count": null}\n')
		>>> ndp.Table.from_json(path, ndp.JsonOptions(layout=ndp.JsonLayout.LINES))
		city count
		TEXT INT64
		0  Paris     2
		1   Lyon  <NA>
		"""
		file_path = Path(path)
		require_existing_file(file_path)
		if options is None:
			options = JsonOptions()

		frame = read_json_file(file_path, options)
		table = cls._from_frame(frame)

		return table

	@classmethod
	def from_excel(cls, path: FilePath, options: ExcelOptions | None = None) -> Self:
		"""
		Return a Table read from a sheet of an Excel file whose first row holds the column names.

		Needs the ``excel`` extra: ``pip install numdaplot[excel]``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the file.
		options
			The sheet to read, the first one by default.

		Returns
		-------
		Self
			A new Table. Dates of the sheet become ``DATETIME`` columns.

		Raises
		------
		FileNotFoundError
			When there is no file at the path.
		MissingDependencyError
			When the ``excel`` extra is not installed.
		InvalidColumnNameError, DuplicateColumnError
			When a cell of the first row is empty, is not a text, or repeats another one.

		Examples
		--------
		>>> import tempfile
		>>> from pathlib import Path
		>>> import numdaplot as ndp
		>>> path = Path(tempfile.mkdtemp()) / "sales.xlsx"
		>>> ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5])}).to_excel(path)
		>>> ndp.Table.from_excel(path).column_types
		{'price': <Type.FLOAT64: 10>}
		"""
		file_path = Path(path)
		require_existing_file(file_path)
		if options is None:
			options = ExcelOptions()

		frame = read_excel_file(file_path, options)
		table = cls._from_frame(frame)

		return table

	@classmethod
	def from_parquet(cls, path: FilePath) -> Self:
		"""
		Return a Table read from a Parquet file.

		Needs the ``parquet`` extra: ``pip install numdaplot[parquet]``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the file.

		Returns
		-------
		Self
			A new Table, with the types stored in the file.

		Raises
		------
		FileNotFoundError
			When there is no file at the path.
		MissingDependencyError
			When the ``parquet`` extra is not installed.

		Examples
		--------
		>>> import tempfile
		>>> from pathlib import Path
		>>> import numdaplot as ndp
		>>> path = Path(tempfile.mkdtemp()) / "sales.parquet"
		>>> ndp.Table.from_arrays({"count": ndp.Array.from_list([3])}).to_parquet(path)
		>>> ndp.Table.from_parquet(path).column_types
		{'count': <Type.INT64: 4>}
		"""
		file_path = Path(path)
		require_existing_file(file_path)
		frame = read_parquet_file(file_path)
		table = cls._from_frame(frame)

		return table

	@classmethod
	def from_stata(cls, path: FilePath) -> Self:
		"""
		Return a Table read from a Stata file (``.dta``).

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the file.

		Returns
		-------
		Self
			A new Table, with the types stored in the file.

		Raises
		------
		FileNotFoundError
			When there is no file at the path.

		Examples
		--------
		>>> import tempfile
		>>> from pathlib import Path
		>>> import numdaplot as ndp
		>>> path = Path(tempfile.mkdtemp()) / "sales.dta"
		>>> ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5])}).to_stata(path)
		>>> ndp.Table.from_stata(path).column_types
		{'price': <Type.FLOAT64: 10>}
		"""
		file_path = Path(path)
		require_existing_file(file_path)
		frame = read_stata_file(file_path)
		table = cls._from_frame(frame)

		return table

	@classmethod
	def from_sas(cls, path: FilePath, options: SasOptions | None = None) -> Self:
		"""
		Return a Table read from a SAS data file (``.sas7bdat``). numdaplot does not write this format.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the file.
		options
			The encoding of the texts, UTF-8 by default.

		Returns
		-------
		Self
			A new Table. SAS stores every number as a decimal, so numbers become ``FLOAT64``.

		Raises
		------
		FileNotFoundError
			When there is no file at the path.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> try:
		... 	ndp.Table.from_sas("missing.sas7bdat")
		... except ndp.FileNotFoundError as error:
		... 	print(error)
		No file found at missing.sas7bdat.
		"""
		file_path = Path(path)
		require_existing_file(file_path)
		if options is None:
			options = SasOptions()

		frame = read_sas_file(file_path, options)
		table = cls._from_frame(frame)

		return table

	@classmethod
	def from_xpt(cls, path: FilePath, options: XptOptions | None = None) -> Self:
		"""
		Return a Table read from a SAS transport file (``.xpt``). numdaplot does not write this format.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the file.
		options
			The encoding of the texts, UTF-8 by default.

		Returns
		-------
		Self
			A new Table. SAS stores every number as a decimal, so numbers become ``FLOAT64``.

		Raises
		------
		FileNotFoundError
			When there is no file at the path.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> try:
		... 	ndp.Table.from_xpt("missing.xpt")
		... except ndp.FileNotFoundError as error:
		... 	print(error)
		No file found at missing.xpt.
		"""
		file_path = Path(path)
		require_existing_file(file_path)
		if options is None:
			options = XptOptions()

		frame = read_xpt_file(file_path, options)
		table = cls._from_frame(frame)

		return table
