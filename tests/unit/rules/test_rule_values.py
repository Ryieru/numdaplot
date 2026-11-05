"""
Unit tests of require_single_value.

.. versionadded:: 0.1.0
"""

from datetime import date

import numpy
import pytest

from numdaplot.errors.invalid_setting_type_error import InvalidSettingTypeError
from numdaplot.rules.rule_values import require_single_value

SETTING_NAME = "Greater value"
SINGLE_VALUES = [True, 10, 2.5, "Paris", date(2026, 1, 31), numpy.int64(10), numpy.float64(2.5)]
REJECTED_VALUES = [None, [1, 2], (1, 2), {"a": 1}]


@pytest.mark.parametrize("value", SINGLE_VALUES)
def test_require_single_value_accepts_single_values(value: object) -> None:
	"""
	Check that Python and numpy single values pass.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		A single value.
	"""
	require_single_value(SETTING_NAME, value)


@pytest.mark.parametrize("value", REJECTED_VALUES)
def test_require_single_value_rejects_other_values(value: object) -> None:
	"""
	Check that None and containers raise InvalidSettingTypeError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		A value that is not single.
	"""
	with pytest.raises(InvalidSettingTypeError):
		require_single_value(SETTING_NAME, value)
