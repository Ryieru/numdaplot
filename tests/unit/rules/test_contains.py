"""
Unit tests of Contains.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.settings.empty_text_error import EmptyTextError
from numdaplot.rules.case import Case
from numdaplot.rules.contains import Contains

SEARCHED_TEXT = "paris"
EMPTY_TEXT = ""


def test_contains_is_case_sensitive_by_default() -> None:
	"""
	Check that upper and lower case are distinguished when case is omitted.

	.. versionadded:: 0.1.0
	"""
	rule = Contains(SEARCHED_TEXT)

	assert rule.case == Case.SENSITIVE


def test_contains_keeps_the_chosen_case() -> None:
	"""
	Check that the chosen case setting is kept.

	.. versionadded:: 0.1.0
	"""
	rule = Contains(SEARCHED_TEXT, case=Case.IGNORED)

	assert rule.case == Case.IGNORED


def test_contains_rejects_an_empty_text() -> None:
	"""
	Check that an empty searched text is rejected.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyTextError):
		Contains(EMPTY_TEXT)
