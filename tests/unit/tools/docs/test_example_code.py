"""
Unit tests of the griffe extension showing the doctest examples as plain Python code.

.. versionadded:: 0.1.0
"""

import doctest

import griffe
from example_code import (
	ExampleCode,
	rewrite_examples,
	separate_imports,
	write_code_block,
	write_example_lines,
	write_output_comment,
)

MODULE_NAME = "arrays"
SIMPLE_TEXT = "Prices.\n\n>>> prices = [1, 2]\n>>> sum(prices)\n3\n"
EXPECTED_SIMPLE_TEXT = "Prices.\n\n\n```python\nprices = [1, 2]\nsum(prices)\n# 3\n```\n\n"
SPLIT_TEXT = ">>> total = 1\n\n![Plot](image.svg)\n\n>>> total\n1\n"
EXPECTED_SPLIT_TEXT = "\n```python\ntotal = 1\n```\n\n\n![Plot](image.svg)\n\n\n```python\ntotal\n# 1\n```\n\n"
GROUPS_TEXT = ">>> first = 1\n\n>>> second = 2\n"
EXPECTED_GROUPS_TEXT = "\n```python\nfirst = 1\nsecond = 2\n```\n\n"
TEXT_WITHOUT_EXAMPLE = "Prices.\n\n    indented text"
CONTINUED_SOURCE = "try:\n    total = 1 / 0\nexcept ZeroDivisionError:\n    print('refused')\n"
DIRECTIVE_SOURCE = "print(path)  # doctest: +ELLIPSIS\n"
IMPORT_LINES = ["from datetime import date", "import numdaplot as ndp", "day = date(2026, 1, 1)"]
EXPECTED_SPACED_LINES = ["from datetime import date", "import numdaplot as ndp", "", "day = date(2026, 1, 1)"]
TABLE_OUTPUT = "    city price\n0  Paris  12.0\n"
EXPECTED_TABLE_COMMENTS = ["#     city price", "# 0  Paris  12.0"]


def test_rewrite_examples_writes_one_python_block_without_prompts() -> None:
	"""
	Check that the examples lose their prompts and their result becomes a comment.

	.. versionadded:: 0.1.0
	"""
	rewritten_text = rewrite_examples(SIMPLE_TEXT)

	assert rewritten_text == EXPECTED_SIMPLE_TEXT


def test_rewrite_examples_splits_the_block_at_text_between_examples() -> None:
	"""
	Check that an image between examples closes the block and the next examples open another one.

	.. versionadded:: 0.1.0
	"""
	rewritten_text = rewrite_examples(SPLIT_TEXT)

	assert rewritten_text == EXPECTED_SPLIT_TEXT


def test_rewrite_examples_joins_groups_separated_by_empty_lines() -> None:
	"""
	Check that examples separated by an empty line only share one block.

	.. versionadded:: 0.1.0
	"""
	rewritten_text = rewrite_examples(GROUPS_TEXT)

	assert rewritten_text == EXPECTED_GROUPS_TEXT


def test_rewrite_examples_keeps_a_docstring_without_example() -> None:
	"""
	Check that a docstring without ``>>>`` is returned as it is.

	.. versionadded:: 0.1.0
	"""
	rewritten_text = rewrite_examples(TEXT_WITHOUT_EXAMPLE)

	assert rewritten_text == TEXT_WITHOUT_EXAMPLE


def test_write_example_lines_keeps_the_continued_lines_of_a_statement() -> None:
	"""
	Check that a statement over several lines keeps its lines and indentation, its result below it.

	.. versionadded:: 0.1.0
	"""
	example = doctest.Example(CONTINUED_SOURCE, "refused\n")

	example_lines = write_example_lines(example)

	assert example_lines == [
		"try:",
		"    total = 1 / 0",
		"except ZeroDivisionError:",
		"    print('refused')",
		"# refused",
	]


def test_write_example_lines_removes_the_doctest_directives() -> None:
	"""
	Check that a doctest directive is not shown.

	.. versionadded:: 0.1.0
	"""
	example = doctest.Example(DIRECTIVE_SOURCE, "")

	example_lines = write_example_lines(example)

	assert example_lines == ["print(path)"]


def test_write_example_lines_keeps_the_alignment_of_a_result() -> None:
	"""
	Check that a result over several lines keeps its leading spaces after the comment sign.

	.. versionadded:: 0.1.0
	"""
	example = doctest.Example("sales\n", TABLE_OUTPUT)

	example_lines = write_example_lines(example)

	assert example_lines[1:] == EXPECTED_TABLE_COMMENTS


def test_write_output_comment_writes_an_empty_line_as_a_lone_sign() -> None:
	"""
	Check that ``<BLANKLINE>`` and an empty line become ``#``.

	.. versionadded:: 0.1.0
	"""
	blank_comment = write_output_comment("<BLANKLINE>")
	empty_comment = write_output_comment("")

	assert blank_comment == "#"
	assert empty_comment == "#"


def test_write_code_block_writes_nothing_without_line() -> None:
	"""
	Check that no line gives no block.

	.. versionadded:: 0.1.0
	"""
	code_block = write_code_block([])

	assert code_block == ""


def test_example_code_rewrites_the_docstring_of_an_object() -> None:
	"""
	Check that the extension rewrites the docstring of a module.

	.. versionadded:: 0.1.0
	"""
	docstring = griffe.Docstring(SIMPLE_TEXT)
	module = griffe.Module(MODULE_NAME, docstring=docstring)
	extension = ExampleCode()

	extension.on_object(obj=module)

	assert docstring.value == EXPECTED_SIMPLE_TEXT


def test_example_code_skips_an_object_without_docstring() -> None:
	"""
	Check that an object without docstring is left as it is.

	.. versionadded:: 0.1.0
	"""
	module = griffe.Module(MODULE_NAME)
	extension = ExampleCode()

	extension.on_object(obj=module)

	assert module.docstring is None


def test_separate_imports_adds_an_empty_line_after_the_imports() -> None:
	"""
	Check that the first imports are followed by an empty line before the code.

	.. versionadded:: 0.1.0
	"""
	spaced_lines = separate_imports(IMPORT_LINES)

	assert spaced_lines == EXPECTED_SPACED_LINES


def test_separate_imports_keeps_a_block_of_imports_only() -> None:
	"""
	Check that a block holding imports only gets no empty line.

	.. versionadded:: 0.1.0
	"""
	import_lines = IMPORT_LINES[:2]

	spaced_lines = separate_imports(import_lines)

	assert spaced_lines == import_lines


def test_separate_imports_keeps_a_block_without_imports() -> None:
	"""
	Check that a block starting with code is left as it is.

	.. versionadded:: 0.1.0
	"""
	code_lines = ["total = 1", "import math"]

	spaced_lines = separate_imports(code_lines)

	assert spaced_lines == code_lines
