"""
Unit tests of the texts read as missing values in CSV and Excel files.

.. versionadded:: 0.1.0
"""

from numdaplot.tables.files.missing_texts import DEFAULT_MISSING_TEXTS, find_missing_settings

GIVEN_TEXTS = ["N/A", "-"]
NO_TEXT = list[str]()
DEFAULT_TEXT_COUNT = 19
DEFAULT_MISSING_SETTING = "keep_default_na"
MISSING_VALUES_SETTING = "na_values"


def test_default_missing_texts_are_the_nineteen_pandas_texts() -> None:
	"""
	Check that the default list holds the 19 texts pandas reads as missing, the empty text included.

	.. versionadded:: 0.1.0
	"""
	text_count = len(DEFAULT_MISSING_TEXTS)
	distinct_texts = set(DEFAULT_MISSING_TEXTS)
	distinct_count = len(distinct_texts)

	assert text_count == DEFAULT_TEXT_COUNT
	assert distinct_count == DEFAULT_TEXT_COUNT
	assert "" in distinct_texts


def test_find_missing_settings_gives_the_default_texts_when_omitted() -> None:
	"""
	Check that None gives the default texts explicitly.

	.. versionadded:: 0.1.0
	"""
	missing_settings = find_missing_settings(None)

	read_texts = missing_settings[MISSING_VALUES_SETTING]
	assert read_texts == list(DEFAULT_MISSING_TEXTS)


def test_find_missing_settings_gives_only_the_given_texts() -> None:
	"""
	Check that a given list replaces the pandas default texts.

	.. versionadded:: 0.1.0
	"""
	missing_settings = find_missing_settings(GIVEN_TEXTS)

	read_texts = missing_settings[MISSING_VALUES_SETTING]
	keeps_pandas_texts = missing_settings[DEFAULT_MISSING_SETTING]
	assert read_texts == GIVEN_TEXTS
	assert not keeps_pandas_texts


def test_find_missing_settings_gives_no_text_for_an_empty_list() -> None:
	"""
	Check that an empty list reads no text as missing.

	.. versionadded:: 0.1.0
	"""
	missing_settings = find_missing_settings(NO_TEXT)

	read_texts = missing_settings[MISSING_VALUES_SETTING]
	assert read_texts == NO_TEXT
