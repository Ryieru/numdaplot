"""
Unit tests of the conversion of text columns to booleans.

.. versionadded:: 0.2.0
"""

import pandas
import pytest

from numdaplot.conversions.text_conversion import parse_booleans
from numdaplot.errors.types.value_conversion_error import ValueConversionError

WORD_TEXTS = pandas.Series(["yes"], dtype="string")
REJECTED_WORD = "yes"


def test_parse_booleans_names_the_first_unknown_text() -> None:
	"""
	Check that a text other than true or false raises ValueConversionError naming it.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ValueConversionError) as error_info:
		parse_booleans(WORD_TEXTS)

	error = error_info.value
	assert error.rejected_value == REJECTED_WORD
