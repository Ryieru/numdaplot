"""
Griffe extension showing the doctest examples of the docstrings as plain Python code.

Docstrings write their examples as doctest does: ``>>>`` before each statement, ``...`` before the lines
continuing it, and the printed result below. Copied from the documentation site as they are, such examples
cannot run. When ``mkdocs`` reads a docstring, this extension writes its examples as a Python code block
without prompts, each result written below its statement as comments, so the copy button gives code that
runs as it is. The docstrings keep the doctest form the tests run.

.. versionadded:: 0.1.0
"""

import doctest
import re
from typing import Any

import griffe

PROMPT = ">>>"
CODE_FENCE_START = "```python"
CODE_FENCE_END = "```"
OUTPUT_PREFIX = "# "
EMPTY_OUTPUT_LINE = "#"
BLANK_LINE_MARKER = "<BLANKLINE>"
LINE_SEPARATOR = "\n"
DOCTEST_DIRECTIVE = re.compile(r"\s*#\s*doctest:.*$")
IMPORT_STARTS = ("import ", "from ")


def rewrite_examples(docstring_text: str) -> str:
	r"""
	Return a docstring with each run of doctest examples written as one Python code block.

	Text between examples, such as the image of a Plot, closes the block, and the next examples open another one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	docstring_text
		The text of a docstring.

	Returns
	-------
	str
		The same text, its examples without prompts and their results as comments. A docstring without
		``>>>`` is returned unchanged.

	Examples
	--------
	>>> from example_code import rewrite_examples
	>>> print(rewrite_examples("Sum.\n\n>>> 1 + 2\n3\n"))
	Sum.
	<BLANKLINE>
	```python
	1 + 2
	# 3
	```
	<BLANKLINE>
	"""
	if PROMPT not in docstring_text:
		return docstring_text

	parser = doctest.DocTestParser()
	pieces = parser.parse(docstring_text)
	rewritten_parts = list[str]()
	code_lines = list[str]()

	for piece in pieces:
		if isinstance(piece, doctest.Example):
			example_lines = write_example_lines(piece)
			code_lines.extend(example_lines)
			continue

		stripped_piece = piece.strip()
		is_blank = stripped_piece == ""
		is_inside_block = code_lines != []
		joins_examples = is_blank and is_inside_block
		if joins_examples:
			continue

		code_block = write_code_block(code_lines)
		rewritten_parts.append(code_block)
		rewritten_parts.append(piece)
		code_lines = list[str]()

	last_block = write_code_block(code_lines)
	rewritten_parts.append(last_block)
	rewritten_text = "".join(rewritten_parts)

	return rewritten_text


def write_example_lines(example: doctest.Example) -> list[str]:
	r"""
	Return the lines of a doctest example as Python code: its statement, then its result as comments.

	.. versionadded:: 0.1.0

	Parameters
	----------
	example
		One doctest example.

	Returns
	-------
	list[str]
		The lines of the statement without prompt and doctest directive, then one comment per line of result.

	Examples
	--------
	>>> import doctest
	>>> from example_code import write_example_lines
	>>> example = doctest.Example("print(5)  # doctest: +ELLIPSIS\n", "5\n")
	>>> write_example_lines(example)
	['print(5)', '# 5']
	"""
	source_text = example.source.rstrip(LINE_SEPARATOR)
	source_lines = source_text.split(LINE_SEPARATOR)
	code_lines = [DOCTEST_DIRECTIVE.sub("", line) for line in source_lines]
	output_text = example.want.rstrip(LINE_SEPARATOR)
	if output_text == "":
		return code_lines

	output_lines = output_text.split(LINE_SEPARATOR)
	comment_lines = [write_output_comment(line) for line in output_lines]
	example_lines = [*code_lines, *comment_lines]

	return example_lines


def write_output_comment(output_line: str) -> str:
	"""
	Return a line of the result of an example as a Python comment.

	.. versionadded:: 0.1.0

	Parameters
	----------
	output_line
		One line of the result, ``<BLANKLINE>`` standing for an empty line.

	Returns
	-------
	str
		The line after ``# ``, or a lone ``#`` for an empty line.

	Examples
	--------
	>>> from example_code import write_output_comment
	>>> write_output_comment("Array([30.], dtype=FLOAT64)"), write_output_comment("<BLANKLINE>")
	('# Array([30.], dtype=FLOAT64)', '#')
	"""
	stripped_line = output_line.strip()
	is_empty = stripped_line in ("", BLANK_LINE_MARKER)
	if is_empty:
		return EMPTY_OUTPUT_LINE

	comment_line = OUTPUT_PREFIX + output_line

	return comment_line


def write_code_block(code_lines: list[str]) -> str:
	r"""
	Return lines of code as a fenced Python block surrounded by empty lines, or nothing without line.

	The first imports of the block are separated from the code after them by an empty line.

	.. versionadded:: 0.1.0

	Parameters
	----------
	code_lines
		The lines of the block.

	Returns
	-------
	str
		The Markdown block, or an empty text.

	Examples
	--------
	>>> from example_code import write_code_block
	>>> write_code_block(["total = 1 + 2"])
	'\n```python\ntotal = 1 + 2\n```\n\n'
	>>> write_code_block([])
	''
	"""
	if code_lines == []:
		return ""

	spaced_lines = separate_imports(code_lines)
	block_lines = ["", CODE_FENCE_START, *spaced_lines, CODE_FENCE_END, "", ""]
	code_block = LINE_SEPARATOR.join(block_lines)

	return code_block


def separate_imports(code_lines: list[str]) -> list[str]:
	"""
	Return lines of code with an empty line between the imports they start with and the code after them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	code_lines
		The lines of an example.

	Returns
	-------
	list[str]
		The same lines, an empty line added after the first imports when code follows them.

	Examples
	--------
	>>> from example_code import separate_imports
	>>> separate_imports(["import numdaplot as ndp", "prices = ndp.Array.from_list([1.5])"])
	['import numdaplot as ndp', '', 'prices = ndp.Array.from_list([1.5])']
	"""
	import_count = 0

	for line in code_lines:
		if not line.startswith(IMPORT_STARTS):
			break

		import_count += 1

	line_count = len(code_lines)
	has_imports = import_count > 0
	has_code_after = import_count < line_count
	needs_separation = has_imports and has_code_after
	if not needs_separation:
		return code_lines

	import_lines = code_lines[:import_count]
	other_lines = code_lines[import_count:]
	spaced_lines = [*import_lines, "", *other_lines]

	return spaced_lines


class ExampleCode(griffe.Extension):
	"""
	Griffe extension showing the doctest examples of the docstrings as plain Python code.

	``mkdocs.yml`` loads it in the ``extensions`` option of the mkdocstrings Python handler, after the extension
	inserting the images of the plot examples and before the one narrowing the indentation.

	.. versionadded:: 0.1.0
	"""

	def on_object(self, *, obj: griffe.Object, **kwargs: Any) -> None:
		"""
		Rewrite the examples of the docstring of an object, if it has one.

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

		rewritten_text = rewrite_examples(obj.docstring.value)
		obj.docstring.value = rewritten_text
