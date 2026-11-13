"""
Unit tests of the search of the first text a conversion could not read.

.. versionadded:: 0.2.0
"""

import pandas

from numdaplot.conversions.unread_texts import find_first_unread_text

TEXT_DTYPE = "string"
READ_TEXTS = ["12:30", "13:00"]
READ_TIMES = [pandas.Timedelta(hours=12, minutes=30), pandas.Timedelta(hours=13)]
TEXTS_WITH_UNREAD = ["12:30", "noon", "midnight"]
TIMES_WITH_UNREAD = [pandas.Timedelta(hours=12, minutes=30), None, None]
FIRST_UNREAD_TEXT = "noon"
TEXTS_WITH_MISSING = ["12:30", None]
TIMES_WITH_MISSING = [pandas.Timedelta(hours=12, minutes=30), None]


def test_find_first_unread_text_gives_the_first_text_not_read() -> None:
	"""
	Check that the first of two texts read as missing is given.

	.. versionadded:: 0.2.0
	"""
	texts = pandas.Series(TEXTS_WITH_UNREAD, dtype=TEXT_DTYPE)
	times = pandas.Series(TIMES_WITH_UNREAD)
	missing_texts = texts.isna()
	missing = missing_texts.to_numpy()

	first_unread_text = find_first_unread_text(texts, times, missing)

	assert first_unread_text == FIRST_UNREAD_TEXT


def test_find_first_unread_text_gives_none_when_every_text_is_read() -> None:
	"""
	Check that None is given when every text was read.

	.. versionadded:: 0.2.0
	"""
	texts = pandas.Series(READ_TEXTS, dtype=TEXT_DTYPE)
	times = pandas.Series(READ_TIMES)
	missing_texts = texts.isna()
	missing = missing_texts.to_numpy()

	first_unread_text = find_first_unread_text(texts, times, missing)

	assert first_unread_text is None


def test_find_first_unread_text_leaves_out_the_missing_texts() -> None:
	"""
	Check that a missing text read as missing is not a reading failure.

	.. versionadded:: 0.2.0
	"""
	texts = pandas.Series(TEXTS_WITH_MISSING, dtype=TEXT_DTYPE)
	times = pandas.Series(TIMES_WITH_MISSING)
	missing_texts = texts.isna()
	missing = missing_texts.to_numpy()

	first_unread_text = find_first_unread_text(texts, times, missing)

	assert first_unread_text is None
