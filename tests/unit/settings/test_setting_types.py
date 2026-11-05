"""
Unit tests of require_setting_type, require_list_not_text and require_object_not_class.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.invalid_setting_type_error import InvalidSettingTypeError
from numdaplot.settings.setting_types import require_list_not_text, require_object_not_class, require_setting_type
from numdaplot.statistics.mean import Mean

SETTING_NAME = "Preview side"
EXPECTED = "a number"
ACCEPTED_TYPES = (int, float)
ACCEPTED_NUMBER = 3
REJECTED_TEXT = "end"
COLUMN_NAMES = ["price"]
COLUMN_TEXT = "price"
EXPECTED_LIST_MESSAGE = "BarChart y expects a list such as ['price'], got 'price'."


def test_require_setting_type_accepts_an_accepted_kind() -> None:
	"""
	Check that a value of an accepted kind passes.

	.. versionadded:: 0.1.0
	"""
	require_setting_type(SETTING_NAME, EXPECTED, ACCEPTED_NUMBER, ACCEPTED_TYPES)


def test_require_setting_type_rejects_another_kind() -> None:
	"""
	Check that a value of another kind raises InvalidSettingTypeError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidSettingTypeError):
		require_setting_type(SETTING_NAME, EXPECTED, REJECTED_TEXT, ACCEPTED_TYPES)


def test_require_list_not_text_accepts_a_list() -> None:
	"""
	Check that a list passes.

	.. versionadded:: 0.1.0
	"""
	require_list_not_text("BarChart y", COLUMN_NAMES)


def test_require_list_not_text_shows_the_text_inside_a_list() -> None:
	"""
	Check that a single text raises InvalidSettingTypeError showing it inside a list.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidSettingTypeError) as error_info:
		require_list_not_text("BarChart y", COLUMN_TEXT)

	message = str(error_info.value)
	assert message == EXPECTED_LIST_MESSAGE


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
