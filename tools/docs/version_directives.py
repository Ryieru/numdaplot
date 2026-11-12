"""
Griffe extension showing the version directives of the docstrings as notes of the documentation site.

Docstrings use the Sphinx directives ``.. versionadded::``, ``.. versionchanged::`` and ``.. deprecated::``,
which editors show as they are. The Markdown of the documentation site does not know them, so this
extension turns them into admonitions when ``mkdocs`` reads the docstrings. Of the added and changed notes that
follow each other, the latest is shown, and the earlier ones are folded in a version history, latest first. A
deprecation stays a warning, always shown. ``docs/stylesheets/symbols.css`` styles them as discreet lines.

.. versionadded:: 0.1.0
"""

import re
from dataclasses import dataclass
from typing import Any

import griffe

VERSION_NOTE = re.compile(
	r"^(?P<indent>[ \t]*)\.\. (?P<directive>versionadded|versionchanged):: (?P<version>\S+)[ \t]*$"
)
DEPRECATED_DIRECTIVE = re.compile(r"^(?P<indent>[ \t]*)\.\. deprecated:: (?P<version>\S+)[ \t]*$")
NOTE_TITLES = {
	"versionadded": "Added in version {version}",
	"versionchanged": "Changed in version {version}",
}
HISTORY_CLASSES = {
	"versionadded": "version-added",
	"versionchanged": "version-changed",
}
LATEST_CLASS = "version-latest"
ADMONITION = '!!! {css_class} "{title}"'
HISTORY_FOLD = '??? version-history "Version history ({note_count})"'
DEPRECATED_ADMONITION = '!!! warning "Deprecated since version {version}"'
# Python expands a docstring tab to 8 spaces, which the tab_indentation extension then narrows to 4.
NESTING_INDENT = " " * 8
LINE_SEPARATOR = "\n"
VERSION_SEPARATOR = "."


@dataclass(frozen=True)
class VersionNote:
	"""
	One added or changed note of a docstring, with the lines describing the change.

	.. versionadded:: 0.2.0

	Parameters
	----------
	directive
		``versionadded`` or ``versionchanged``.
	version
		The version, such as ``0.2.0``.
	indent
		The indentation of the directive line.
	detail_lines
		The lines indented below the directive, such as ``Renamed from Conversion.``, as written.
	"""

	directive: str
	version: str
	indent: str
	detail_lines: list[str]


def convert_version_directives(docstring_text: str) -> str:
	r"""
	Return a docstring whose version directives are written as Markdown admonitions.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Shows the latest of the notes that follow each other, and folds the earlier ones in a version history.

	Parameters
	----------
	docstring_text
		The text of a docstring.

	Returns
	-------
	str
		The same text, each group of added and changed notes replaced with its latest note and a folded history of
		the earlier ones, each deprecation replaced with a warning.

	Examples
	--------
	>>> from version_directives import convert_version_directives
	>>> convert_version_directives("Mean of the values.\n\n.. versionadded:: 0.1.0")
	'Mean of the values.\n\n!!! version-latest "Added in version 0.1.0"'
	"""
	lines = docstring_text.split(LINE_SEPARATOR)
	line_count = len(lines)
	converted_lines = list[str]()
	position = 0
	while position < line_count:
		notes, next_position = read_note_group(lines, position)
		if notes == []:
			line = lines[position]
			converted_line = DEPRECATED_DIRECTIVE.sub(write_deprecated_admonition, line)
			converted_lines.append(converted_line)
			position += 1
			continue

		group_lines = write_note_group(notes)
		converted_lines.extend(group_lines)
		position = next_position

	converted_text = LINE_SEPARATOR.join(converted_lines)

	return converted_text


def read_note_group(lines: list[str], position: int) -> tuple[list[VersionNote], int]:
	"""
	Return the added and changed notes that follow each other from a line, and the line after them.

	.. versionadded:: 0.2.0

	Parameters
	----------
	lines
		The lines of a docstring.
	position
		The line to start from.

	Returns
	-------
	tuple[list[VersionNote], int]
		The notes, empty when the line is not a note, and the position of the first line after them.

	Examples
	--------
	>>> from version_directives import read_note_group
	>>> notes, next_position = read_note_group([".. versionadded:: 0.1.0", ".. versionchanged:: 0.2.0", ""], 0)
	>>> [note.version for note in notes], next_position
	(['0.1.0', '0.2.0'], 2)
	"""
	notes = list[VersionNote]()
	line_count = len(lines)
	while position < line_count:
		note = read_note(lines, position)
		if note is None:
			break

		notes.append(note)
		detail_count = len(note.detail_lines)
		position += 1
		position += detail_count

	return notes, position


def read_note(lines: list[str], position: int) -> VersionNote | None:
	"""
	Return the added or changed note starting at a line, with its detail lines.

	.. versionadded:: 0.2.0

	Parameters
	----------
	lines
		The lines of a docstring.
	position
		The line of the directive.

	Returns
	-------
	VersionNote or None
		The note, or None when the line is not an added or changed directive.

	Examples
	--------
	>>> from version_directives import read_note
	>>> read_note([".. versionchanged:: 0.2.0", "        Renamed from Conversion.", ""], 0).detail_lines
	['        Renamed from Conversion.']
	"""
	line = lines[position]
	note_match = VERSION_NOTE.match(line)
	if note_match is None:
		return None

	directive = note_match.group("directive")
	version = note_match.group("version")
	indent = note_match.group("indent")
	first_detail_position = position + 1
	following_lines = lines[first_detail_position:]
	detail_lines = read_detail_lines(following_lines, indent)
	note = VersionNote(directive, version, indent, detail_lines)

	return note


def read_detail_lines(lines: list[str], indent: str) -> list[str]:
	"""
	Return the lines indented deeper than a directive, until the first blank or shallower line.

	.. versionadded:: 0.2.0

	Parameters
	----------
	lines
		The lines following a directive.
	indent
		The indentation of the directive.

	Returns
	-------
	list[str]
		The detail lines, as written.

	Examples
	--------
	>>> from version_directives import read_detail_lines
	>>> read_detail_lines(["        Renamed.", "Parameters"], "")
	['        Renamed.']
	"""
	indent_width = len(indent)
	detail_lines = list[str]()
	for line in lines:
		stripped_line = line.lstrip()
		line_width = len(line)
		stripped_width = len(stripped_line)
		line_indent_width = line_width - stripped_width
		is_deeper = line_indent_width > indent_width
		is_detail = stripped_line != "" and is_deeper
		if not is_detail:
			break

		detail_lines.append(line)

	return detail_lines


def find_version_key(version: str) -> tuple[int, ...]:
	"""
	Return the numbers of a version, which compare as the versions do.

	.. versionadded:: 0.2.0

	Parameters
	----------
	version
		A final version, such as ``0.10.0``.

	Returns
	-------
	tuple[int, ...]
		The numbers of the version, so that ``0.10.0`` comes after ``0.9.0``.

	Examples
	--------
	>>> from version_directives import find_version_key
	>>> find_version_key("0.10.0") > find_version_key("0.9.0")
	True
	"""
	version_parts = version.split(VERSION_SEPARATOR)
	version_numbers = [int(version_part) for version_part in version_parts]
	version_key = tuple(version_numbers)

	return version_key


def find_latest_position(notes: list[VersionNote]) -> int:
	"""
	Return the position of the latest note: the highest version, the last written one between equal versions.

	.. versionadded:: 0.2.0

	Parameters
	----------
	notes
		At least one note.

	Returns
	-------
	int
		The position of the latest note in the list.

	Examples
	--------
	>>> from version_directives import VersionNote, find_latest_position
	>>> added = VersionNote("versionadded", "0.1.0", "", [])
	>>> changed = VersionNote("versionchanged", "0.2.0", "", [])
	>>> find_latest_position([changed, added])
	0
	"""
	first_note = notes[0]
	latest_key = find_version_key(first_note.version)
	latest_position = 0
	for position, note in enumerate(notes):
		note_key = find_version_key(note.version)
		if note_key >= latest_key:
			latest_key = note_key
			latest_position = position

	return latest_position


def write_note_group(notes: list[VersionNote]) -> list[str]:
	"""
	Return the lines of the latest note of a group, then the folded history of the earlier ones, latest first.

	.. versionadded:: 0.2.0

	Parameters
	----------
	notes
		The added and changed notes that follow each other in a docstring.

	Returns
	-------
	list[str]
		The admonition lines.

	Examples
	--------
	>>> from version_directives import VersionNote, write_note_group
	>>> added = VersionNote("versionadded", "0.1.0", "", [])
	>>> changed = VersionNote("versionchanged", "0.2.0", "", ["        Renamed."])
	>>> for line in write_note_group([added, changed]):
	... 	print(line)
	!!! version-latest "Changed in version 0.2.0"
	        Renamed.
	??? version-history "Version history (1)"
	        !!! version-added "Added in version 0.1.0"
	"""
	latest_position = find_latest_position(notes)
	latest_note = notes[latest_position]
	group_lines = write_note(latest_note, LATEST_CLASS, "")
	earlier_notes = [note for position, note in enumerate(notes) if position != latest_position]
	if earlier_notes == []:
		return group_lines

	earlier_notes.reverse()
	history_lines = write_history(earlier_notes, latest_note.indent)
	group_lines.extend(history_lines)

	return group_lines


def write_note(note: VersionNote, css_class: str, nesting_indent: str) -> list[str]:
	"""
	Return the admonition line of a note and its detail lines, indented below it.

	.. versionadded:: 0.2.0

	Parameters
	----------
	note
		An added or changed note.
	css_class
		The admonition type, which the stylesheet colors.
	nesting_indent
		The indentation added to every line, to place the note inside the history.

	Returns
	-------
	list[str]
		The admonition line, then the detail lines.

	Examples
	--------
	>>> from version_directives import VersionNote, write_note
	>>> write_note(VersionNote("versionadded", "0.1.0", "", []), "version-added", "")
	['!!! version-added "Added in version 0.1.0"']
	"""
	title_template = NOTE_TITLES[note.directive]
	title = title_template.format(version=note.version)
	admonition = ADMONITION.format(css_class=css_class, title=title)
	admonition_line = nesting_indent + note.indent + admonition
	detail_lines = [nesting_indent + detail_line for detail_line in note.detail_lines]
	note_lines = [admonition_line, *detail_lines]

	return note_lines


def write_history(notes: list[VersionNote], indent: str) -> list[str]:
	"""
	Return the lines of a folded version history holding earlier notes.

	.. versionadded:: 0.2.0

	Parameters
	----------
	notes
		The earlier notes, in the order they are shown.
	indent
		The indentation of the group of notes.

	Returns
	-------
	list[str]
		The fold line, then the lines of each note, nested inside it.

	Examples
	--------
	>>> from version_directives import VersionNote, write_history
	>>> write_history([VersionNote("versionadded", "0.1.0", "", [])], "")[0]
	'??? version-history "Version history (1)"'
	"""
	note_count = len(notes)
	fold_line = HISTORY_FOLD.format(note_count=note_count)
	history_lines = [indent + fold_line]
	for note in notes:
		css_class = HISTORY_CLASSES[note.directive]
		note_lines = write_note(note, css_class, NESTING_INDENT)
		history_lines.extend(note_lines)

	return history_lines


def write_deprecated_admonition(directive_match: re.Match[str]) -> str:
	"""
	Return the warning line replacing a deprecation directive.

	.. versionadded:: 0.2.0

	Parameters
	----------
	directive_match
		The match of a deprecation line, with its indentation and its version.

	Returns
	-------
	str
		The warning line, at the indentation of the directive.

	Examples
	--------
	>>> from version_directives import DEPRECATED_DIRECTIVE, write_deprecated_admonition
	>>> directive_match = DEPRECATED_DIRECTIVE.search(".. deprecated:: 0.2.0")
	>>> write_deprecated_admonition(directive_match)
	'!!! warning "Deprecated since version 0.2.0"'
	"""
	indent = directive_match.group("indent")
	version = directive_match.group("version")
	admonition = DEPRECATED_ADMONITION.format(version=version)
	admonition_line = indent + admonition

	return admonition_line


class VersionDirectives(griffe.Extension):
	"""
	Griffe extension turning the version directives of every docstring into admonitions.

	``mkdocs.yml`` loads it in the ``extensions`` option of the mkdocstrings Python handler.

	.. versionadded:: 0.1.0
	"""

	def on_object(self, *, obj: griffe.Object, **kwargs: Any) -> None:
		"""
		Convert the version directives of the docstring of an object, if it has one.

		.. versionadded:: 0.1.0

		Parameters
		----------
		obj
			A module, class, function or attribute read by griffe.
		**kwargs
			The other arguments griffe gives to its extensions, unused.
		"""
		if obj.docstring is None:
			return

		converted_text = convert_version_directives(obj.docstring.value)
		obj.docstring.value = converted_text
