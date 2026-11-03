"""
Unit tests of the griffe extension showing the version directives.

.. versionadded:: 0.1.0
"""

import griffe
import pytest
from version_directives import VERSION_DIRECTIVE, VersionDirectives, convert_version_directives, write_admonition

ADDED_TEXT = "Mean of the values.\n\n.. versionadded:: 0.1.0\n\nParameters"
EXPECTED_ADDED_TEXT = 'Mean of the values.\n\n!!! version-added "Added in version 0.1.0"\n\nParameters'
INDENTED_DIRECTIVE = "\t.. versionchanged:: 0.2.0"
EXPECTED_INDENTED_ADMONITION = '\t!!! version-changed "Changed in version 0.2.0"'
DEPRECATED_DIRECTIVE = ".. deprecated:: 0.3.0"
EXPECTED_DEPRECATED_ADMONITION = '!!! warning "Deprecated since version 0.3.0"'
TEXT_WITHOUT_DIRECTIVE = "Mean of the values, written ``.. versionadded::`` in the source."
MODULE_NAME = "sales"


def test_convert_version_directives_turns_a_directive_into_an_admonition() -> None:
	"""
	Check that versionadded becomes a version-added admonition, the rest of the text unchanged.

	.. versionadded:: 0.1.0
	"""
	converted_text = convert_version_directives(ADDED_TEXT)

	assert converted_text == EXPECTED_ADDED_TEXT


def test_convert_version_directives_keeps_a_text_without_directive_line() -> None:
	"""
	Check that a directive name inside a sentence is not a directive line.

	.. versionadded:: 0.1.0
	"""
	converted_text = convert_version_directives(TEXT_WITHOUT_DIRECTIVE)

	assert converted_text == TEXT_WITHOUT_DIRECTIVE


@pytest.mark.parametrize(
	("directive_line", "expected_admonition"),
	[
		(INDENTED_DIRECTIVE, EXPECTED_INDENTED_ADMONITION),
		(DEPRECATED_DIRECTIVE, EXPECTED_DEPRECATED_ADMONITION),
	],
)
def test_write_admonition_keeps_the_indentation_and_names_the_version(
	directive_line: str,
	expected_admonition: str,
) -> None:
	"""
	Check the admonition of versionchanged, indented, and of deprecated.

	.. versionadded:: 0.1.0

	Parameters
	----------
	directive_line
		A directive line.
	expected_admonition
		Its admonition line.
	"""
	directive_match = VERSION_DIRECTIVE.search(directive_line)
	assert directive_match is not None

	admonition_line = write_admonition(directive_match)

	assert admonition_line == expected_admonition


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
