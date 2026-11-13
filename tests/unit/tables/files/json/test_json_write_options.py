"""
Unit tests of JsonWriteOptions.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.settings.invalid_count_error import InvalidCountError
from numdaplot.tables.files.json.json_layout import JsonLayout
from numdaplot.tables.files.json.json_write_options import JsonWriteOptions

NEGATIVE_DECIMALS = -1


def test_json_write_options_use_one_list_of_records_and_every_digit_by_default() -> None:
	"""
	Check the default layout and decimals.

	.. versionadded:: 0.1.0
	"""
	options = JsonWriteOptions()

	assert options.layout == JsonLayout.RECORDS
	assert options.decimals is None


def test_json_write_options_reject_negative_decimals() -> None:
	"""
	Check that the number of decimals is checked at creation.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidCountError):
		JsonWriteOptions(decimals=NEGATIVE_DECIMALS)
