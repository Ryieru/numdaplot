"""
Unit tests of the reading of SAS data and SAS transport files.

pandas cannot write these formats, so the pandas reader is replaced with a fake.

.. versionadded:: 0.1.0
"""

from pathlib import Path
from typing import Any

import pandas
import pytest

from numdaplot.tables.files.encoding import Encoding
from numdaplot.tables.files.sas_file import read_sas_file, read_sas_format, read_xpt_file
from numdaplot.tables.files.sas_options import SasOptions
from numdaplot.tables.files.xpt_options import XptOptions

FILE_PATH = Path("sales.sas7bdat")
READ_SAS_NAME = "read_sas"
SAS_DATA_FORMAT = "sas7bdat"
SAS_TRANSPORT_FORMAT = "xport"
FAKE_FRAME = pandas.DataFrame({"price": [1.5]})


class FakeSasReader:
	"""
	Fake ``pandas.read_sas`` recording its arguments.

	.. versionadded:: 0.1.0
	"""

	def __init__(self) -> None:
		"""
		Start without any recorded call.

		.. versionadded:: 0.1.0
		"""
		self.calls = list[dict[str, Any]]()

	def __call__(self, path: Path, format: str, encoding: str) -> pandas.DataFrame:
		"""
		Record the arguments and return a known DataFrame.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the file.
		format
			The SAS format.
		encoding
			The encoding of the texts.

		Returns
		-------
		pandas.DataFrame
			Always the fake DataFrame.
		"""
		call = {"path": path, "format": format, "encoding": encoding}
		self.calls.append(call)

		return FAKE_FRAME


def test_read_sas_file_reads_the_sas_data_format(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that a SAS data file is read with the sas7bdat format and its encoding.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the pandas reader with a fake.
	"""
	reader = FakeSasReader()
	monkeypatch.setattr(pandas, READ_SAS_NAME, reader)
	options = SasOptions(encoding=Encoding.LATIN_1)

	frame = read_sas_file(FILE_PATH, options)

	call = reader.calls[0]
	assert frame is FAKE_FRAME
	assert call["format"] == SAS_DATA_FORMAT
	assert call["encoding"] == Encoding.LATIN_1.value


def test_read_xpt_file_reads_the_sas_transport_format(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that an XPT file is read with the xport format.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the pandas reader with a fake.
	"""
	reader = FakeSasReader()
	monkeypatch.setattr(pandas, READ_SAS_NAME, reader)

	read_xpt_file(FILE_PATH, XptOptions())

	call = reader.calls[0]
	assert call["format"] == SAS_TRANSPORT_FORMAT
	assert call["encoding"] == Encoding.UTF_8.value


def test_read_sas_format_gives_the_path_to_pandas(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the path reaches the pandas reader unchanged.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the pandas reader with a fake.
	"""
	reader = FakeSasReader()
	monkeypatch.setattr(pandas, READ_SAS_NAME, reader)

	read_sas_format(FILE_PATH, SAS_DATA_FORMAT, Encoding.UTF_8)

	call = reader.calls[0]
	assert call["path"] == FILE_PATH
