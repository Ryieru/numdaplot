"""
Reading and writing Parquet files.

.. versionadded:: 0.1.0
"""

from pathlib import Path
from typing import Any, cast

import pandas

from numdaplot.tables.files.optional_package import require_package
from numdaplot.tables.files.pandas_backend import NULLABLE_DTYPE_BACKEND

PARQUET_PACKAGE = "pyarrow"
PARQUET_EXTRA = "parquet"


def read_parquet_file(path: Path) -> pandas.DataFrame:
	"""
	Return the columns of a Parquet file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of an existing Parquet file.

	Returns
	-------
	pandas.DataFrame
		The columns as pandas reads them.

	Raises
	------
	MissingDependencyError
		When ``pyarrow`` is not installed.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import pandas
	>>> from numdaplot.tables.files.parquet.parquet_file import read_parquet_file
	>>> path = Path(tempfile.mkdtemp()) / "sales.parquet"
	>>> pandas.DataFrame({"price": [1.5]}).to_parquet(path, index=False)
	>>> read_parquet_file(path)
	   price
	0    1.5
	"""
	require_package(PARQUET_PACKAGE, PARQUET_EXTRA)
	# Some versions of the pandas stubs leave the parameter types of read_parquet unknown.
	parquet_pandas = cast(Any, pandas)
	raw_frame = parquet_pandas.read_parquet(path, dtype_backend=NULLABLE_DTYPE_BACKEND)
	frame = cast(pandas.DataFrame, raw_frame)

	return frame


def write_parquet_file(frame: pandas.DataFrame, path: Path) -> None:
	"""
	Write the columns of a Table in a Parquet file, which keeps the type of each column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	path
		The path of the file, replaced when it exists.

	Raises
	------
	MissingDependencyError
		When ``pyarrow`` is not installed.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import pandas
	>>> from numdaplot.tables.files.parquet.parquet_file import write_parquet_file
	>>> path = Path(tempfile.mkdtemp()) / "sales.parquet"
	>>> write_parquet_file(pandas.DataFrame({"price": [1.5]}), path)
	>>> path.exists()
	True
	"""
	require_package(PARQUET_PACKAGE, PARQUET_EXTRA)
	frame.to_parquet(path, index=False)
