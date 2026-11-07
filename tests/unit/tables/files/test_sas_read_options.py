"""
Unit tests of SasReadOptions.

.. versionadded:: 0.1.0
"""

from numdaplot.tables.files.encoding import Encoding
from numdaplot.tables.files.sas_read_options import SasReadOptions


def test_sas_read_options_use_utf_8_by_default() -> None:
	"""
	Check the default encoding of SAS data files.

	.. versionadded:: 0.1.0
	"""
	options = SasReadOptions()

	assert options.encoding == Encoding.UTF_8


def test_sas_read_options_keep_their_encoding() -> None:
	"""
	Check that a given encoding is available as an attribute.

	.. versionadded:: 0.1.0
	"""
	options = SasReadOptions(encoding=Encoding.LATIN_1)

	assert options.encoding == Encoding.LATIN_1
