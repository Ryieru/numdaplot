"""
Unit tests of the MkDocs hook removing the en dashes and the spaces inside parentheses.

.. versionadded:: 0.1.0
"""

from section_separators import on_page_content, remove_parenthesis_spaces, replace_en_dashes

EN_DASH = "\u2013"
SECTION_HTML = "<b><code>path</code></b> (<code>FilePath</code>)\n          " + EN_DASH + "\n<p>The path.</p>"
EXPECTED_SECTION_HTML = "<b><code>path</code></b> (<code>FilePath</code>)\n<p>The path.</p>"
HTML_WITHOUT_DASH = "<p>A text - with a hyphen.</p>"
SPACED_TYPE_HTML = "( <code>CsvOptions</code>, default:\n <code>None</code>\n)"
EXPECTED_TYPE_HTML = "(<code>CsvOptions</code>, default:\n <code>None</code>)"
PUNCTUATION_HTML = "(a, )"


def test_replace_en_dashes_removes_the_dash_after_the_name() -> None:
	"""
	Check that the spaces and the en dash disappear.

	.. versionadded:: 0.1.0
	"""
	replaced_html = replace_en_dashes(SECTION_HTML)

	assert replaced_html == EXPECTED_SECTION_HTML


def test_replace_en_dashes_keeps_html_without_en_dash() -> None:
	"""
	Check that a hyphen is not changed.

	.. versionadded:: 0.1.0
	"""
	replaced_html = replace_en_dashes(HTML_WITHOUT_DASH)

	assert replaced_html == HTML_WITHOUT_DASH


def test_on_page_content_removes_every_en_dash() -> None:
	"""
	Check that the hook leaves no en dash in a page.

	.. versionadded:: 0.1.0
	"""
	page_html = on_page_content(SECTION_HTML)

	assert EN_DASH not in page_html


def test_remove_parenthesis_spaces_joins_parentheses_to_their_content() -> None:
	"""
	Check that the spaces inside both parentheses disappear.

	.. versionadded:: 0.1.0
	"""
	tightened_html = remove_parenthesis_spaces(SPACED_TYPE_HTML)

	assert tightened_html == EXPECTED_TYPE_HTML


def test_remove_parenthesis_spaces_keeps_a_space_after_punctuation() -> None:
	"""
	Check that a space after a comma, before a closing parenthesis, is kept.

	.. versionadded:: 0.1.0
	"""
	tightened_html = remove_parenthesis_spaces(PUNCTUATION_HTML)

	assert tightened_html == PUNCTUATION_HTML


def test_on_page_content_joins_parentheses_to_their_content() -> None:
	"""
	Check that the hook also removes the spaces inside parentheses.

	.. versionadded:: 0.1.0
	"""
	page_html = on_page_content(SPACED_TYPE_HTML)

	assert page_html == EXPECTED_TYPE_HTML
