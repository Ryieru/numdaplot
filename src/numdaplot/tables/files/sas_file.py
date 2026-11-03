"""
Reading SAS data and SAS transport (XPT) files.

.. versionadded:: 0.1.0
"""

from pathlib import Path
from typing import Literal

import pandas

from numdaplot.tables.files.encoding import Encoding
from numdaplot.tables.files.sas_options import SasOptions
from numdaplot.tables.files.xpt_options import XptOptions

SAS_DATA_FORMAT = "sas7bdat"
SAS_TRANSPORT_FORMAT = "xport"

type SasFormat = Literal["sas7bdat", "xport"]
"""The names pandas gives to the SAS data and SAS transport formats.

.. versionadded:: 0.1.0
"""


def read_sas_file(path: Path, options: SasOptions) -> pandas.DataFrame:
	"""
	Return the columns of a SAS data file (``.sas7bdat``).

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of an existing SAS data file.
	options
		The encoding of the texts of the file.

	Returns
	-------
	pandas.DataFrame
		The columns as pandas reads them. SAS stores every number as a decimal.
	"""
	frame = read_sas_format(path, SAS_DATA_FORMAT, options.encoding)

	return frame


def read_xpt_file(path: Path, options: XptOptions) -> pandas.DataFrame:
	"""
	Return the columns of a SAS transport file (``.xpt``).

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of an existing SAS transport file.
	options
		The encoding of the texts of the file.

	Returns
	-------
	pandas.DataFrame
		The columns as pandas reads them. SAS stores every number as a decimal.
	"""
	frame = read_sas_format(path, SAS_TRANSPORT_FORMAT, options.encoding)

	return frame


def read_sas_format(path: Path, sas_format: SasFormat, encoding: Encoding) -> pandas.DataFrame:
	"""
	Return the columns of a SAS file of a given format.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of an existing SAS file.
	sas_format
		``sas7bdat`` for SAS data, ``xport`` for SAS transport.
	encoding
		The encoding of the texts of the file.

	Returns
	-------
	pandas.DataFrame
		The columns as pandas reads them.
	"""
	frame = pandas.read_sas(path, format=sas_format, encoding=encoding.value)

	return frame
