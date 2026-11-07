"""
Unit tests of the cleaning of the column names a Table reads.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.tables.files.column_names import ColumnNames
from numdaplot.tables.frames.cleaned_names import clean_frame_names, clean_names, require_distinct_cleaned_names

SPACED_FRAME = pandas.DataFrame({"id_vehicule\n": [1], " speed\t": [50], " road ": ["A1"]})
EXPECTED_CLEANED_NAMES = ["id_vehicule", "speed", "road"]
INNER_SPACE_NAMES = ["id vehicule"]
NUMBER_NAME = 2024
NAMES_WITH_NUMBER = [" count ", NUMBER_NAME]
EXPECTED_NAMES_WITH_NUMBER = ["count", NUMBER_NAME]
COLLIDING_NAMES = ["id", "id\n"]
CLEANED_COLLIDING_NAMES = ["id", "id"]
EXPECTED_ORIGINAL_NAMES = ["id", "id\n"]
REPEATED_NAMES = ["id", "id"]


def test_clean_frame_names_removes_spaces_tabs_and_line_breaks_around_names() -> None:
	"""
	Check that CLEANED removes line breaks, tabs and non-breaking spaces at both ends.

	.. versionadded:: 0.1.0
	"""
	cleaned_frame = clean_frame_names(SPACED_FRAME, ColumnNames.CLEANED)

	column_names = cleaned_frame.columns.tolist()
	assert column_names == EXPECTED_CLEANED_NAMES


def test_clean_frame_names_keeps_the_names_with_kept() -> None:
	"""
	Check that KEPT gives back the same DataFrame.

	.. versionadded:: 0.1.0
	"""
	kept_frame = clean_frame_names(SPACED_FRAME, ColumnNames.KEPT)

	assert kept_frame is SPACED_FRAME


def test_clean_frame_names_leaves_the_given_frame_unchanged() -> None:
	"""
	Check that the DataFrame given keeps its names.

	.. versionadded:: 0.1.0
	"""
	frame = SPACED_FRAME.copy()
	expected_names = frame.columns.tolist()

	clean_frame_names(frame, ColumnNames.CLEANED)

	column_names = frame.columns.tolist()
	assert column_names == expected_names


def test_clean_names_keeps_spaces_inside_a_name() -> None:
	"""
	Check that only the start and the end of a name change.

	.. versionadded:: 0.1.0
	"""
	cleaned_names = clean_names(list(INNER_SPACE_NAMES))

	assert cleaned_names == INNER_SPACE_NAMES


def test_clean_names_keeps_a_name_that_is_not_a_text() -> None:
	"""
	Check that a number stays as it is, for the check of the names to refuse it.

	.. versionadded:: 0.1.0
	"""
	cleaned_names = clean_names(list(NAMES_WITH_NUMBER))

	assert cleaned_names == EXPECTED_NAMES_WITH_NUMBER


def test_require_distinct_cleaned_names_names_both_original_names() -> None:
	"""
	Check that two names becoming the same raise DuplicateColumnError with both of them.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError) as error_info:
		require_distinct_cleaned_names(list(COLLIDING_NAMES), list(CLEANED_COLLIDING_NAMES))

	original_names = error_info.value.original_names
	assert original_names == EXPECTED_ORIGINAL_NAMES


def test_require_distinct_cleaned_names_leaves_a_repeated_name_to_the_name_check() -> None:
	"""
	Check that a name written twice the same way raises nothing here.

	.. versionadded:: 0.1.0
	"""
	require_distinct_cleaned_names(list(REPEATED_NAMES), list(REPEATED_NAMES))
