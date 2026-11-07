"""
Unit tests of JoinSuffixes.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.invalid_suffixes_error import InvalidSuffixesError
from numdaplot.tables.joining.join_suffixes import JoinSuffixes

LEFT_SUFFIX = "_2024"
RIGHT_SUFFIX = "_2025"
EMPTY_SUFFIX = ""


def test_join_suffixes_keeps_two_different_suffixes() -> None:
	"""
	Check that two different non-empty suffixes are kept.

	.. versionadded:: 0.1.0
	"""
	suffixes = JoinSuffixes(left=LEFT_SUFFIX, right=RIGHT_SUFFIX)

	assert suffixes.left == LEFT_SUFFIX
	assert suffixes.right == RIGHT_SUFFIX


@pytest.mark.parametrize(
	("left", "right"), [(EMPTY_SUFFIX, RIGHT_SUFFIX), (LEFT_SUFFIX, EMPTY_SUFFIX), (LEFT_SUFFIX, LEFT_SUFFIX)]
)
def test_join_suffixes_rejects_an_empty_or_repeated_suffix(left: str, right: str) -> None:
	"""
	Check that an empty suffix or the same suffix twice raises InvalidSuffixesError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The suffix of the joined Table.
	right
		The suffix of the other Table.
	"""
	with pytest.raises(InvalidSuffixesError):
		JoinSuffixes(left=left, right=right)
