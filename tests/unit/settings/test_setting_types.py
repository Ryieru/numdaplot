"""
Unit tests of require_object_not_class.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.invalid_setting_type_error import InvalidSettingTypeError
from numdaplot.settings.setting_types import require_object_not_class
from numdaplot.statistics.mean import Mean


def test_require_object_not_class_accepts_an_object() -> None:
	"""
	Check that an object passes.

	.. versionadded:: 0.1.0
	"""
	require_object_not_class("compute statistic", "a statistic", Mean())


def test_require_object_not_class_rejects_a_class() -> None:
	"""
	Check that a class raises InvalidSettingTypeError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidSettingTypeError):
		require_object_not_class("compute statistic", "a statistic", Mean)
