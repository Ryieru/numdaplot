"""
Unit tests of Count.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.statistics.count import Count
from numdaplot.statistics.counted_missing import CountedMissing

INVALID_SETTING = "included"


def test_count_excludes_the_missing_values_by_default() -> None:
	"""
	Check the default setting.

	.. versionadded:: 0.1.0
	"""
	statistic = Count()

	assert statistic.missing == CountedMissing.EXCLUDED


def test_count_keeps_its_setting() -> None:
	"""
	Check that the setting is available as an attribute.

	.. versionadded:: 0.1.0
	"""
	statistic = Count(missing=CountedMissing.INCLUDED)

	assert statistic.missing == CountedMissing.INCLUDED


def test_count_refuses_a_setting_of_another_type() -> None:
	"""
	Check that the type of the setting is checked at creation.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidTypeError):
		Count(missing=INVALID_SETTING)  # pyright: ignore[reportArgumentType]
