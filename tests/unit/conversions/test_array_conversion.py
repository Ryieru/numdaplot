"""
Unit tests of ArrayConversion.

.. versionadded:: 0.2.0
"""

from typing import Any, cast

import pytest

from numdaplot.brackets.brackets import Brackets
from numdaplot.conversions.array_conversion import ArrayConversion
from numdaplot.conversions.boolean_rule import BooleanRule
from numdaplot.dates.date_format import DateFormat
from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.types.type import Type

CATEGORY_REFUSAL = "ArrayConversion does not accept Type.CATEGORY."
AGE_BRACKETS = Brackets(limits=[0, 18, 65])


def test_array_conversion_keeps_its_settings() -> None:
	"""
	Check that the type, the format and the boolean rule are available as attributes.

	.. versionadded:: 0.2.0
	"""
	conversion = ArrayConversion(dtype=Type.DATE, format=DateFormat.DAY_MONTH_YEAR, booleans=BooleanRule.ZERO_ONE)

	assert conversion.dtype == Type.DATE
	assert conversion.format == DateFormat.DAY_MONTH_YEAR
	assert conversion.booleans == BooleanRule.ZERO_ONE


def test_array_conversion_has_no_format_nor_boolean_rule_by_default() -> None:
	"""
	Check that the format and the boolean rule are omitted when not given.

	.. versionadded:: 0.2.0
	"""
	conversion = ArrayConversion(dtype=Type.TEXT)

	assert conversion.format is None
	assert conversion.booleans is None


def test_array_conversion_refuses_categories() -> None:
	"""
	Check that CATEGORY raises RefusedSettingError naming it.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(RefusedSettingError) as error_info:
		ArrayConversion(dtype=Type.CATEGORY)

	error_text = str(error_info.value)
	assert error_text == CATEGORY_REFUSAL


def test_array_conversion_refuses_brackets_as_format() -> None:
	"""
	Check that Brackets, a format of Table columns only, raise InvalidTypeError.

	.. versionadded:: 0.2.0
	"""
	brackets = cast(Any, AGE_BRACKETS)

	with pytest.raises(InvalidTypeError):
		ArrayConversion(dtype=Type.TEXT, format=brackets)
