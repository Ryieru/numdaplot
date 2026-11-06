"""
Reading and writing CSV files.

.. versionadded:: 0.1.0
"""

import csv
from pathlib import Path
from typing import Any, cast

import pandas

from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.tables.columns.column_names import require_column_names
from numdaplot.tables.files.csv_options import CsvOptions
from numdaplot.tables.files.pandas_backend import NULLABLE_DTYPE_BACKEND

CSV_NEWLINE = ""
DECIMAL_FORMAT = "%.{decimals}f"
DECIMALS_SETTING = "decimals"
FROM_CSV_NAME = "Table.from_csv"


def require_read_options(options: CsvOptions) -> None:
	"""
	Check that the settings of a CSV file apply to its reading.

	.. versionadded:: 0.1.0

	Parameters
	----------
	options
		The settings of the file.

	Raises
	------
	RefusedSettingError
		When ``decimals`` is given, which only applies to the writing.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.files.csv_file import require_read_options
	>>> try:
	... 	require_read_options(ndp.CsvOptions(decimals=2))
	... except ndp.RefusedSettingError as error:
	... 	print(error)
	Table.from_csv does not accept decimals.
	"""
	if options.decimals is not None:
		raise RefusedSettingError(DECIMALS_SETTING, FROM_CSV_NAME)


def read_csv_file(path: Path, options: CsvOptions) -> pandas.DataFrame:
	r"""
	Return the columns of a CSV file whose first row holds the column names.

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
	>>> read_csv_file(path, ndp.CsvOptions(separator=";"))
	    city  price
	0  Paris    1.5
	"""
	header = read_csv_header(path, options)
	if header is None:
		empty_frame = pandas.DataFrame()
		return empty_frame

	require_column_names(header)
	# Some versions of the pandas stubs leave the parameter types of read_csv unknown.
	csv_pandas = cast(Any, pandas)
	raw_frame = csv_pandas.read_csv(
		path,
		sep=options.separator,
		encoding=options.encoding.value,
		dtype_backend=NULLABLE_DTYPE_BACKEND,
	)
	frame = cast(pandas.DataFrame, raw_frame)

	return frame


def read_csv_header(path: Path, options: CsvOptions) -> list[str] | None:
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
	>>> read_csv_header(path, ndp.CsvOptions())
	['price', 'price']
	"""
	with path.open(encoding=options.encoding.value, newline=CSV_NEWLINE) as file:
		rows = csv.reader(file, delimiter=options.separator)
		header = next(rows, None)

	return header


def write_csv_file(frame: pandas.DataFrame, path: Path, options: CsvOptions) -> None:
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
	>>> write_csv_file(pandas.DataFrame({"price": [1.5]}), path, ndp.CsvOptions())
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
