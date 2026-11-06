"""
Unit tests of the detection of texts holding a date out of range.

.. versionadded:: 0.1.0
"""

from datetime import datetime

from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.tables.columns.date_range import is_text_out_of_range, read_custom_text, read_moment_text

DATE_PATTERN = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
CUSTOM_FORMAT = CustomDateFormat("%Y/%m/%d")
FAR_TEXT = "3000-01-31"
FAR_MOMENT = datetime(3000, 1, 31)
CLOSE_TEXT = "2026-01-31"
FAR_CUSTOM_TEXT = "3000/01/31"
IMPOSSIBLE_TEXT = "3000-02-31"
OTHER_TEXT = "abc"
SPACED_FAR_TEXT = " 3000-01-31 "


def test_read_moment_text_reads_the_parts_of_the_pattern() -> None:
	"""
	Check a text following the pattern, the time counting as 0.

	.. versionadded:: 0.1.0
	"""
	moment = read_moment_text(FAR_TEXT, DATE_PATTERN)

	assert moment == FAR_MOMENT


def test_read_moment_text_gives_none_for_another_text() -> None:
	"""
	Check a text not following the pattern.

	.. versionadded:: 0.1.0
	"""
	moment = read_moment_text(OTHER_TEXT, DATE_PATTERN)

	assert moment is None


def test_read_moment_text_gives_none_for_an_impossible_date() -> None:
	"""
	Check a text following the pattern that is not a real date.

	.. versionadded:: 0.1.0
	"""
	moment = read_moment_text(IMPOSSIBLE_TEXT, DATE_PATTERN)

	assert moment is None


def test_read_custom_text_reads_the_pattern() -> None:
	"""
	Check a text following a custom pattern.

	.. versionadded:: 0.1.0
	"""
	moment = read_custom_text(FAR_CUSTOM_TEXT, CUSTOM_FORMAT)

	assert moment == FAR_MOMENT


def test_read_custom_text_gives_none_for_another_text() -> None:
	"""
	Check a text not following a custom pattern.

	.. versionadded:: 0.1.0
	"""
	moment = read_custom_text(OTHER_TEXT, CUSTOM_FORMAT)

	assert moment is None


def test_is_text_out_of_range_finds_a_far_date() -> None:
	"""
	Check a real date out of range, with spaces around it.

	.. versionadded:: 0.1.0
	"""
	is_out_of_range = is_text_out_of_range(SPACED_FAR_TEXT, DATE_PATTERN)

	assert is_out_of_range is True


def test_is_text_out_of_range_finds_a_far_date_of_a_custom_format() -> None:
	"""
	Check a real date out of range read with a custom pattern.

	.. versionadded:: 0.1.0
	"""
	is_out_of_range = is_text_out_of_range(FAR_CUSTOM_TEXT, CUSTOM_FORMAT)

	assert is_out_of_range is True


def test_is_text_out_of_range_leaves_a_close_date() -> None:
	"""
	Check a date in range.

	.. versionadded:: 0.1.0
	"""
	is_out_of_range = is_text_out_of_range(CLOSE_TEXT, DATE_PATTERN)

	assert is_out_of_range is False


def test_is_text_out_of_range_leaves_an_impossible_date() -> None:
	"""
	Check that a text that is not a date is not out of range.

	.. versionadded:: 0.1.0
	"""
	is_out_of_range = is_text_out_of_range(IMPOSSIBLE_TEXT, DATE_PATTERN)

	assert is_out_of_range is False
