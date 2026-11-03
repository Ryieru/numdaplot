"""
MkDocs hook removing the dash and the stray spaces mkdocstrings writes around parameter types.

The templates of mkdocstrings separate each parameter, return value or error from its description with
an en dash. The documentation never shows that character: this hook removes it, and
``stylesheets/symbols.css`` shows the description on the next line, indented, as the pandas documentation does.
The templates also break the line before the closing parenthesis of a type, which shows as a space:
the hook removes the spaces right after an opening parenthesis and right before a closing one.

.. versionadded:: 0.1.0
"""

import re
from typing import Any

EN_DASH_SEPARATOR = re.compile("\\s*\u2013")
SPACE_AFTER_OPENING = re.compile(r"\(\s+")
SPACE_BEFORE_CLOSING = re.compile(r"(?<=[>\w])\s+\)")


def replace_en_dashes(html: str) -> str:
	r"""
	Return HTML without its en dashes and the spaces before them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	html
		The HTML of a page.

	Returns
	-------
	str
		The same HTML without any en dash.

	Examples
	--------
	>>> from section_separators import replace_en_dashes
	>>> replace_en_dashes("<code>path</code>\n          \u2013\n<p>The path.</p>")
	'<code>path</code>\n<p>The path.</p>'
	"""
	replaced_html = EN_DASH_SEPARATOR.sub("", html)

	return replaced_html


def remove_parenthesis_spaces(html: str) -> str:
	r"""
	Return HTML without spaces right after an opening parenthesis or right before a closing one.

	A closing parenthesis keeps the space before it when it follows a punctuation sign, as in ``( )``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	html
		The HTML of a page.

	Returns
	-------
	str
		The same HTML with its parentheses next to their content.

	Examples
	--------
	>>> from section_separators import remove_parenthesis_spaces
	>>> remove_parenthesis_spaces("( <code>None</code>\n)")
	'(<code>None</code>)'
	"""
	opened_html = SPACE_AFTER_OPENING.sub("(", html)
	closed_html = SPACE_BEFORE_CLOSING.sub(")", opened_html)

	return closed_html


def on_page_content(html: str, **kwargs: Any) -> str:
	"""
	Clean the HTML of each page, called by MkDocs after rendering its Markdown.

	.. versionadded:: 0.1.0

	Parameters
	----------
	html
		The HTML of the page.
	**kwargs
		The page, the configuration and the files MkDocs gives to its hooks, unused.

	Returns
	-------
	str
		The HTML without any en dash, its parentheses next to their content.
	"""
	replaced_html = replace_en_dashes(html)
	tightened_html = remove_parenthesis_spaces(replaced_html)

	return tightened_html
