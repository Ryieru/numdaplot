"""
Reading and writing CSV files.

.. versionadded:: 0.1.0
"""

import csv
import warnings
from pathlib import Path
from typing import Any, cast

import pandas
from pandas.api.types import infer_dtype

from numdaplot.tables.columns.column_names import require_column_names
from numdaplot.tables.files.csv_read_options import CsvReadOptions
from numdaplot.tables.files.csv_write_options import CsvWriteOptions
from numdaplot.tables.files.missing_texts import find_missing_settings
from numdaplot.tables.files.pandas_backend import NULLABLE_DTYPE_BACKEND
from numdaplot.tables.frames.frame_normalization import PYTHON_OBJECT_DTYPE
from numdaplot.tables.frames.pandas_decimals import find_exact_csv_settings

CSV_NEWLINE = ""
DECIMAL_FORMAT = "%.{decimals}f"
IGNORE_ACTION = "ignore"
# The kinds pandas infers for a column whose blocks were read as numbers or booleans in one place and texts in another.
MIXED_BLOCK_KINDS = frozenset({"mixed", "mixed-integer"})
TEXT_COLUMNS_SETTING = "usecols"
TEXT_DTYPE_SETTING = "dtype"


def read_csv_file(path: Path, options: CsvReadOptions) -> pandas.DataFrame:
	r"""
	Return the columns of a CSV file whose first row holds the column names, with the exact value of each decimal.

	pandas reads a long file in blocks, each block guessing its own types. A column whose blocks get different types,
	such as numbers then texts, is read again as texts, so every value keeps the text of the file, such as ``01``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of an existing CSV file.
	options
		The separator and the encoding of the file.

	Returns
	-------
	pandas.DataFrame
		The columns as pandas reads them, empty for an empty file.

	Raises
	------
	InvalidColumnNameError
		When a column name is empty.
	DuplicateColumnError
		When a column name appears twice.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.files.csv_file import read_csv_file
	>>> folder = Path(tempfile.mkdtemp())
	>>> path = folder / "sales.csv"
	>>> _ = path.write_text("city;price\nParis;1.5\n")
	>>> read_csv_file(path, ndp.CsvReadOptions(separator=";"))
	    city  price
	0  Paris    1.5
	"""
	header = read_csv_header(path, options)
	if header is None:
		empty_frame = pandas.DataFrame()
		return empty_frame

	require_column_names(header)
	block_frame = read_pandas_csv(path, options, {})
	mixed_names = find_mixed_columns(block_frame)
	if mixed_names == []:
		return block_frame

	text_settings = {TEXT_COLUMNS_SETTING: mixed_names, TEXT_DTYPE_SETTING: str}
	text_frame = read_pandas_csv(path, options, text_settings)
	text_columns = {name: text_frame[name] for name in mixed_names}
	frame = block_frame.assign(**text_columns)

	return frame


def read_pandas_csv(path: Path, options: CsvReadOptions, column_settings: dict[str, Any]) -> pandas.DataFrame:
	r"""
	Return the columns of a CSV file as ``pandas.read_csv`` reads them in blocks, with the exact value of each decimal.

	The ``DtypeWarning`` pandas emits when the blocks of a column get different types is not shown, as
	``read_csv_file`` reads such a column again as texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of an existing CSV file whose first row holds the column names.
	options
		The separator, the encoding and the texts read as missing.
	column_settings
		Other settings of ``pandas.read_csv``, such as the columns to read and their dtype.

	Returns
	-------
	pandas.DataFrame
		The columns as pandas reads them.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.files.csv_file import read_pandas_csv
	>>> path = Path(tempfile.mkdtemp()) / "codes.csv"
	>>> _ = path.write_text("code;price\n01;1.5\n")
	>>> read_pandas_csv(path, ndp.CsvReadOptions(separator=";"), {"usecols": ["code"], "dtype": str})
	  code
	0   01
	"""
	# Some versions of the pandas stubs leave the parameter types of read_csv unknown.
	csv_pandas = cast(Any, pandas)
	exact_settings = find_exact_csv_settings()
	missing_settings = find_missing_settings(options.missing_texts)
	with warnings.catch_warnings():
		warnings.simplefilter(IGNORE_ACTION, pandas.errors.DtypeWarning)
		raw_frame = csv_pandas.read_csv(
			path,
			sep=options.separator,
			encoding=options.encoding.value,
			dtype_backend=NULLABLE_DTYPE_BACKEND,
			**exact_settings,
			**missing_settings,
			**column_settings,
		)

	frame = cast(pandas.DataFrame, raw_frame)

	return frame


def find_mixed_columns(frame: pandas.DataFrame) -> list[str]:
	"""
	Return the names of the columns whose blocks pandas read with different types, such as numbers then texts.

	A block holding only ``01`` is read as the number 1, so the text of such a column is no longer the one of the file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a CSV file as ``pandas.read_csv`` reads them in blocks.

	Returns
	-------
	list[str]
		The names of the mixed columns, in the order of the file.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.files.csv_file import find_mixed_columns
	>>> codes = pandas.Series([1, "2A"], dtype=object)
	>>> prices = pandas.Series([1.5, 2.0])
	>>> find_mixed_columns(pandas.DataFrame({"code": codes, "price": prices}))
	['code']
	"""
	mixed_names = list[str]()
	for column_name, column in frame.items():
		if column.dtype != PYTHON_OBJECT_DTYPE:
			continue

		inferred_kind = infer_dtype(column, skipna=True)
		if inferred_kind in MIXED_BLOCK_KINDS:
			mixed_names.append(str(column_name))

	return mixed_names


def read_csv_header(path: Path, options: CsvReadOptions) -> list[str] | None:
	r"""
	Return the column names written on the first row of a CSV file, before pandas renames repeated ones.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of an existing CSV file.
	options
		The separator and the encoding of the file.

	Returns
	-------
	list[str] or None
		The names of the first row, ``None`` for an empty file.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.files.csv_file import read_csv_header
	>>> folder = Path(tempfile.mkdtemp())
	>>> path = folder / "sales.csv"
	>>> _ = path.write_text("price,price\n1,2\n")
	>>> read_csv_header(path, ndp.CsvReadOptions())
	['price', 'price']
	"""
	with path.open(encoding=options.encoding.value, newline=CSV_NEWLINE) as file:
		rows = csv.reader(file, delimiter=options.separator)
		header = next(rows, None)

	return header


def write_csv_file(frame: pandas.DataFrame, path: Path, options: CsvWriteOptions) -> None:
	"""
	Write the columns of a Table in a CSV file, column names on the first row and without row numbers.

	Missing values are written as empty values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	path
		The path of the file, replaced when it exists.
	options
		The separator and the encoding of the file.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.files.csv_file import write_csv_file
	>>> path = Path(tempfile.mkdtemp()) / "sales.csv"
	>>> write_csv_file(pandas.DataFrame({"price": [1.5]}), path, ndp.CsvWriteOptions())
	>>> print(path.read_text())
	price
	1.5
	<BLANKLINE>
	"""
	decimal_format = None
	if options.decimals is not None:
		decimal_format = DECIMAL_FORMAT.format(decimals=options.decimals)

	frame.to_csv(
		path,
		sep=options.separator,
		encoding=options.encoding.value,
		index=False,
		float_format=decimal_format,
	)
