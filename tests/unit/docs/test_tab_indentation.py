"""
Unit tests of the griffe extension narrowing the tab indentation of the docstrings.

.. versionadded:: 0.1.0
"""

import griffe
from tab_indentation import LEADING_SPACES, TabIndentation, narrow_indentation, narrow_leading_spaces

EXPANDED_TEXT = "Parameters\n----------\nvalues\n        The values.\n                Nested detail."
EXPECTED_NARROWED_TEXT = "Parameters\n----------\nvalues\n    The values.\n        Nested detail."
UNEVEN_LINE = "          text"
EXPECTED_UNEVEN_SPACE_COUNT = 6
TEXT_WITHOUT_INDENTATION = "Summary of the object."
MODULE_NAME = "sales"
EXPECTED_DESCRIPTION = "The values."


def test_narrow_indentation_halves_each_level_of_eight_spaces() -> None:
	"""
	Check that one and two levels of 8 spaces become 4 and 8 spaces.

	.. versionadded:: 0.1.0
	"""
	narrowed_text = narrow_indentation(EXPANDED_TEXT)

	assert narrowed_text == EXPECTED_NARROWED_TEXT


def test_narrow_indentation_keeps_a_text_without_indentation() -> None:
	"""
	Check that a text without leading spaces is unchanged.

	.. versionadded:: 0.1.0
	"""
	narrowed_text = narrow_indentation(TEXT_WITHOUT_INDENTATION)

	assert narrowed_text == TEXT_WITHOUT_INDENTATION


def test_narrow_leading_spaces_keeps_spaces_beyond_the_last_level() -> None:
	"""
	Check that 10 spaces give 4 for the level and 2 kept.

	.. versionadded:: 0.1.0
	"""
	spaces_match = LEADING_SPACES.search(UNEVEN_LINE)
	assert spaces_match is not None

	narrowed_spaces = narrow_leading_spaces(spaces_match)

	space_count = len(narrowed_spaces)
	assert space_count == EXPECTED_UNEVEN_SPACE_COUNT


def test_tab_indentation_lets_the_numpy_parser_read_parameter_descriptions() -> None:
	"""
	Check that a parameter description indented by 8 spaces is read as text after the extension.

	.. versionadded:: 0.1.0
	"""
	docstring = griffe.Docstring(EXPANDED_TEXT, parser=griffe.Parser.numpy)
	module = griffe.Module(MODULE_NAME, docstring=docstring)
	extension = TabIndentation()

	extension.on_object(obj=module)

	parameter_sections = [
		section for section in docstring.parsed if section.kind == griffe.DocstringSectionKind.parameters
	]
	parameters = parameter_sections[0].value
	first_description = parameters[0].description
	assert first_description.startswith(EXPECTED_DESCRIPTION)


def test_tab_indentation_skips_an_object_without_docstring() -> None:
	"""
	Check that an object without docstring is left without docstring.

	.. versionadded:: 0.1.0
	"""
	module = griffe.Module(MODULE_NAME)
	extension = TabIndentation()

	extension.on_object(obj=module)

	assert module.docstring is None
