"""
Griffe extension reading the tab indentation of the docstrings as the NumPy docstring parser expects it.

Python expands each tab of a docstring to 8 spaces, while the NumPy parser of griffe expects the description
of a parameter to be indented by 4 spaces: with 8, the description is shown as a block of code. This extension
turns each indentation level of 8 spaces back into 4 spaces when ``mkdocs`` reads the docstrings.

.. versionadded:: 0.1.0
"""

import re
from typing import Any

import griffe

EXPANDED_TAB_WIDTH = 8
PARSER_INDENT_WIDTH = 4
LEADING_SPACES = re.compile(r"^(?P<spaces> +)", re.MULTILINE)


def narrow_indentation(docstring_text: str) -> str:
	r"""
	Return a docstring whose indentation levels of 8 spaces are 4 spaces wide.

	.. versionadded:: 0.1.0

	Parameters
	----------
	docstring_text
		The text of a docstring whose tabs Python expanded to 8 spaces.

	Returns
	-------
	str
		The same text, each full level of 8 leading spaces replaced with 4 spaces.

	Examples
	--------
	>>> from tab_indentation import narrow_indentation
	>>> narrow_indentation("values\n        The values to store.")
	'values\n    The values to store.'
	"""
	narrowed_text = LEADING_SPACES.sub(narrow_leading_spaces, docstring_text)

	return narrowed_text


def narrow_leading_spaces(spaces_match: re.Match[str]) -> str:
	"""
	Return the leading spaces of a line with each level of 8 spaces narrowed to 4.

	.. versionadded:: 0.1.0

	Parameters
	----------
	spaces_match
		The match of the leading spaces of a line.

	Returns
	-------
	str
		The narrowed spaces; spaces beyond the last full level are kept.

	Examples
	--------
	>>> from tab_indentation import LEADING_SPACES, narrow_leading_spaces
	>>> spaces_match = LEADING_SPACES.search("                   text")
	>>> len(narrow_leading_spaces(spaces_match))
	11
	"""
	spaces = spaces_match.group("spaces")
	space_count = len(spaces)
	level_count, remaining_count = divmod(space_count, EXPANDED_TAB_WIDTH)
	narrowed_count = level_count * PARSER_INDENT_WIDTH + remaining_count
	narrowed_spaces = " " * narrowed_count

	return narrowed_spaces


class TabIndentation(griffe.Extension):
	"""
	Griffe extension narrowing the indentation of every docstring before the NumPy parser reads it.

	``mkdocs.yml`` loads it in the ``extensions`` option of the mkdocstrings Python handler.

	.. versionadded:: 0.1.0
	"""

	def on_object(self, *, obj: griffe.Object, **kwargs: Any) -> None:
		"""
		Narrow the indentation of the docstring of an object, if it has one.

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

		narrowed_text = narrow_indentation(obj.docstring.value)
		obj.docstring.value = narrowed_text
