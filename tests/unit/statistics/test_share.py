"""
Unit tests of Share.

.. versionadded:: 0.2.0
"""

import pytest

from numdaplot.errors.types.invalid_type_error import InvalidTypeError
from numdaplot.rules.is_missing import IsMissing
from numdaplot.statistics.counted_missing import CountedMissing
from numdaplot.statistics.share import Share

NOT_A_RULE = "missing"


def test_share_excludes_the_missing_values_by_default() -> None:
	"""
	Check the default setting.

	.. versionadded:: 0.2.0
	"""
	statistic = Share(rule=IsMissing())

	assert statistic.missing == CountedMissing.EXCLUDED


def test_share_refuses_a_rule_of_another_type() -> None:
	"""
	Check that the type of the rule is checked at creation.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidTypeError):
		Share(rule=NOT_A_RULE)  # pyright: ignore[reportArgumentType]
