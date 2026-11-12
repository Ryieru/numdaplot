"""
Unit tests of the griffe extension showing the version directives.

.. versionadded:: 0.1.0
"""

import griffe
from version_directives import (
	DEPRECATED_DIRECTIVE,
	VersionDirectives,
	VersionNote,
	convert_version_directives,
	find_latest_position,
	find_version_key,
	read_detail_lines,
	read_note,
	read_note_group,
	write_deprecated_admonition,
	write_note_group,
)

DETAIL_INDENT = " " * 8
ADDED_TEXT = "Mean of the values.\n\n.. versionadded:: 0.1.0\n\nParameters"
EXPECTED_ADDED_TEXT = 'Mean of the values.\n\n!!! version-latest "Added in version 0.1.0"\n\nParameters'
RENAMED_TEXT = (
	"Settings.\n\n.. versionadded:: 0.1.0\n.. versionchanged:: 0.2.0\n"
	+ DETAIL_INDENT
	+ "Renamed from Old.\n\nParameters"
)
EXPECTED_RENAMED_TEXT = (
	'Settings.\n\n!!! version-latest "Changed in version 0.2.0"\n'
	+ DETAIL_INDENT
	+ 'Renamed from Old.\n??? version-history "Version history (1)"\n'
	+ DETAIL_INDENT
	+ '!!! version-added "Added in version 0.1.0"\n\nParameters'
)
INDENTED_TEXT = "    .. versionadded:: 0.1.0"
EXPECTED_INDENTED_TEXT = '    !!! version-latest "Added in version 0.1.0"'
DEPRECATED_TEXT = "    .. deprecated:: 0.3.0"
EXPECTED_DEPRECATED_TEXT = '    !!! warning "Deprecated since version 0.3.0"'
TEXT_WITHOUT_DIRECTIVE = "Mean of the values, written ``.. versionadded::`` in the source."
GROUP_LINES = [".. versionadded:: 0.1.0", ".. versionchanged:: 0.2.0", DETAIL_INDENT + "Renamed.", "", "Parameters"]
EXPECTED_GROUP_VERSIONS = ["0.1.0", "0.2.0"]
EXPECTED_LINE_AFTER_GROUP = 3
PLAIN_LINES = ["Parameters", ".. versionadded:: 0.1.0"]
DETAILS_THEN_SHALLOWER = [DETAIL_INDENT + "Renamed.", DETAIL_INDENT + "Moved.", "Parameters"]
EXPECTED_DETAILS = [DETAIL_INDENT + "Renamed.", DETAIL_INDENT + "Moved."]
DETAIL_THEN_BLANK = [DETAIL_INDENT + "Renamed.", "", DETAIL_INDENT + "Text of another block."]
EXPECTED_DETAIL_BEFORE_BLANK = [DETAIL_INDENT + "Renamed."]
TENTH_VERSION = "0.10.0"
NINTH_VERSION = "0.9.0"
ADDED_NOTE = VersionNote("versionadded", "0.1.0", "", [])
FIRST_CHANGE = VersionNote("versionchanged", "0.2.0", "", [DETAIL_INDENT + "Renamed."])
SECOND_CHANGE = VersionNote("versionchanged", "0.3.0", "", [])
SAME_VERSION_CHANGE = VersionNote("versionchanged", "0.2.0", "", [DETAIL_INDENT + "Moved."])
EXPECTED_TIE_POSITION = 1
EXPECTED_SINGLE_NOTE_LINES = ['!!! version-latest "Added in version 0.1.0"']
EXPECTED_HISTORY_LINES = [
	'!!! version-latest "Changed in version 0.3.0"',
	'??? version-history "Version history (2)"',
	DETAIL_INDENT + '!!! version-changed "Changed in version 0.2.0"',
	DETAIL_INDENT + DETAIL_INDENT + "Renamed.",
	DETAIL_INDENT + '!!! version-added "Added in version 0.1.0"',
]
MODULE_NAME = "sales"


def test_convert_version_directives_shows_a_single_note_as_the_latest() -> None:
	"""
	Check that a lone versionadded becomes the latest note, the rest of the text unchanged.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Renamed from ``test_convert_version_directives_turns_a_directive_into_an_admonition``, checks the latest note.
	"""
	converted_text = convert_version_directives(ADDED_TEXT)

	assert converted_text == EXPECTED_ADDED_TEXT


def test_convert_version_directives_folds_the_earlier_notes() -> None:
	"""
	Check that a change shows first with its detail, and the earlier addition goes into the folded history.

	.. versionadded:: 0.2.0
	"""
	converted_text = convert_version_directives(RENAMED_TEXT)

	assert converted_text == EXPECTED_RENAMED_TEXT


def test_convert_version_directives_keeps_the_indentation_of_a_note() -> None:
	"""
	Check that an indented directive gives an admonition at the same indentation.

	.. versionadded:: 0.2.0
	"""
	converted_text = convert_version_directives(INDENTED_TEXT)

	assert converted_text == EXPECTED_INDENTED_TEXT


def test_convert_version_directives_turns_a_deprecation_into_a_warning() -> None:
	"""
	Check that a deprecation stays a warning outside any history.

	.. versionadded:: 0.2.0
	"""
	converted_text = convert_version_directives(DEPRECATED_TEXT)

	assert converted_text == EXPECTED_DEPRECATED_TEXT


def test_convert_version_directives_keeps_a_text_without_directive_line() -> None:
	"""
	Check that a directive name inside a sentence is not a directive line.

	.. versionadded:: 0.1.0
	"""
	converted_text = convert_version_directives(TEXT_WITHOUT_DIRECTIVE)

	assert converted_text == TEXT_WITHOUT_DIRECTIVE


def test_read_note_group_reads_the_notes_that_follow_each_other() -> None:
	"""
	Check that the group holds both notes and ends at the blank line after the detail.

	.. versionadded:: 0.2.0
	"""
	notes, next_position = read_note_group(GROUP_LINES, 0)

	versions = [note.version for note in notes]
	assert versions == EXPECTED_GROUP_VERSIONS
	assert next_position == EXPECTED_LINE_AFTER_GROUP


def test_read_note_group_gives_no_note_on_another_line() -> None:
	"""
	Check that a line which is not a directive gives an empty group at the same position.

	.. versionadded:: 0.2.0
	"""
	notes, next_position = read_note_group(PLAIN_LINES, 0)

	assert notes == []
	assert next_position == 0


def test_read_note_gives_none_for_a_line_without_directive() -> None:
	"""
	Check that a plain line is not a note.

	.. versionadded:: 0.2.0
	"""
	note = read_note(PLAIN_LINES, 0)

	assert note is None


def test_read_detail_lines_stops_at_a_shallower_line() -> None:
	"""
	Check that the detail lines end at the first line not indented below the directive.

	.. versionadded:: 0.2.0
	"""
	detail_lines = read_detail_lines(DETAILS_THEN_SHALLOWER, "")

	assert detail_lines == EXPECTED_DETAILS


def test_read_detail_lines_stops_at_a_blank_line() -> None:
	"""
	Check that a blank line ends the detail lines.

	.. versionadded:: 0.2.0
	"""
	detail_lines = read_detail_lines(DETAIL_THEN_BLANK, "")

	assert detail_lines == EXPECTED_DETAIL_BEFORE_BLANK


def test_find_version_key_compares_versions_as_numbers() -> None:
	"""
	Check that 0.10.0 comes after 0.9.0, which a comparison of texts gets wrong.

	.. versionadded:: 0.2.0
	"""
	tenth_key = find_version_key(TENTH_VERSION)
	ninth_key = find_version_key(NINTH_VERSION)

	assert tenth_key > ninth_key


def test_find_latest_position_keeps_the_last_of_equal_versions() -> None:
	"""
	Check that between two notes of the same version, the last written one is the latest.

	.. versionadded:: 0.2.0
	"""
	latest_position = find_latest_position([FIRST_CHANGE, SAME_VERSION_CHANGE])

	assert latest_position == EXPECTED_TIE_POSITION


def test_write_note_group_has_no_history_for_a_single_note() -> None:
	"""
	Check that a lone note gives no version history.

	.. versionadded:: 0.2.0
	"""
	group_lines = write_note_group([ADDED_NOTE])

	assert group_lines == EXPECTED_SINGLE_NOTE_LINES


def test_write_note_group_lists_the_history_latest_first() -> None:
	"""
	Check that the earlier notes are nested in the history, the most recent first, with their details.

	.. versionadded:: 0.2.0
	"""
	group_lines = write_note_group([ADDED_NOTE, FIRST_CHANGE, SECOND_CHANGE])

	assert group_lines == EXPECTED_HISTORY_LINES


def test_write_deprecated_admonition_keeps_the_indentation() -> None:
	"""
	Check the warning line of an indented deprecation.

	.. versionadded:: 0.2.0
	"""
	directive_match = DEPRECATED_DIRECTIVE.search(DEPRECATED_TEXT)
	assert directive_match is not None

	admonition_line = write_deprecated_admonition(directive_match)

	assert admonition_line == EXPECTED_DEPRECATED_TEXT


def test_version_directives_convert_the_docstring_of_an_object() -> None:
	"""
	Check that the extension rewrites the docstring of a module.

	.. versionadded:: 0.1.0
	"""
	docstring = griffe.Docstring(ADDED_TEXT)
	module = griffe.Module(MODULE_NAME, docstring=docstring)
	extension = VersionDirectives()

	extension.on_object(obj=module)

	assert docstring.value == EXPECTED_ADDED_TEXT


def test_version_directives_skip_an_object_without_docstring() -> None:
	"""
	Check that an object without docstring is left without docstring.

	.. versionadded:: 0.1.0
	"""
	module = griffe.Module(MODULE_NAME)
	extension = VersionDirectives()

	extension.on_object(obj=module)

	assert module.docstring is None
