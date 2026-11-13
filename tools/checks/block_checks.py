"""
Blocks of code lines repeated in the source, reported once each with their length.

.. versionadded:: 0.2.0
"""

import ast
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from check_report import CheckResult, Severity
from duplicate_checks import list_compared_files

MINIMUM_BLOCK_LINES = 5
SKIPPED_STARTS = ("#", ")", "]", "}")
ENUM_MEMBER = re.compile(r"[A-Z][A-Z0-9_]* = auto\(\)")
MODULE_REGION = 0
NEXT_STEP = 1
PREVIOUS_STEP = -1
REGION_NODES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
FUNCTION_NODES = (ast.FunctionDef, ast.AsyncFunctionDef)
IMPORT_NODES = (ast.Import, ast.ImportFrom)
BLOCK_CHECK_NAME = "identical blocks of 5 code lines or more"
BLOCK_PROBLEM = "same {line_count} code lines: {places}, starting with {first_line!r}"
BLOCK_PLACE = "{path}:{first_number}-{last_number}"
PLACE_SEPARATOR = ", "


@dataclass(frozen=True)
class CodeLine:
	"""
	A line of code, out of any docstring, comment or import.

	Parameters
	----------
	path
		The file.
	number
		The number of the line, from 1.
	text
		The line without its indentation.
	region
		The first line of the innermost function or class holding the line, 0 at the level of the module.
	"""

	path: str
	number: int
	text: str
	region: int


@dataclass(frozen=True)
class BlockPlace:
	"""
	Where a block of code lines starts: its file and the position of its first line among the code lines of the file.

	Parameters
	----------
	file_index
		The position of the file in the compared files.
	position
		The position of the first line in the code lines of the file, from 0.
	"""

	file_index: int
	position: int


def check_identical_blocks(scope_files: list[Path]) -> CheckResult:
	"""
	Return the blocks of at least 5 code lines found twice, when a changed file holds one of them.

	A block stays inside one function, one class body or the level of the module: lines of several functions in a
	row are not a copied block. Overlapping blocks repeated at the same places are merged, so each repetition is
	reported once with its length.

	Parameters
	----------
	scope_files
		The changed files.

	Returns
	-------
	CheckResult
		One warning per repeated block: some are only alike, such as similar checks of settings.
	"""
	scope_names = {str(path) for path in scope_files}
	files_lines = [read_code_lines(path) for path in list_compared_files()]
	blocks = collect_blocks(files_lines)
	places_by_place = index_repeated_places(blocks)
	place_sets = places_by_place.values()
	repeated_sets = set(place_sets)
	problems = list[str]()

	for place_set in repeated_sets:
		earlier_set = shift_places(place_set, PREVIOUS_STEP)
		is_continued = is_repeated_set(earlier_set, places_by_place)
		if is_continued:
			continue

		place_paths = {files_lines[block_place.file_index][block_place.position].path for block_place in place_set}
		is_in_scope = bool(place_paths & scope_names)
		if is_in_scope:
			block_problem = describe_repetition(place_set, files_lines, places_by_place)
			problems.append(block_problem)

	sorted_problems = sorted(problems)
	result = CheckResult(BLOCK_CHECK_NAME, Severity.WARNING, sorted_problems)

	return result


def collect_blocks(files_lines: list[list[CodeLine]]) -> dict[tuple[str, ...], list[BlockPlace]]:
	"""
	Return the places of every block of 5 code lines that stays inside one function, one class body or the module.

	Parameters
	----------
	files_lines
		The code lines of each compared file.

	Returns
	-------
	dict[tuple[str, ...], list[BlockPlace]]
		For each block of texts, the places where it starts.
	"""
	blocks = defaultdict[tuple[str, ...], list[BlockPlace]](list)

	for file_index, code_lines in enumerate(files_lines):
		line_count = len(code_lines)
		start_count = line_count - MINIMUM_BLOCK_LINES + 1

		for position in range(start_count):
			window = code_lines[position : position + MINIMUM_BLOCK_LINES]
			window_regions = {code_line.region for code_line in window}
			region_count = len(window_regions)
			if region_count > 1:
				continue

			block = tuple(code_line.text for code_line in window)
			block_place = BlockPlace(file_index, position)
			blocks[block].append(block_place)

	return blocks


def index_repeated_places(blocks: dict[tuple[str, ...], list[BlockPlace]]) -> dict[BlockPlace, frozenset[BlockPlace]]:
	"""
	Return, for each place of a block found at least twice, every place of that block.

	Parameters
	----------
	blocks
		The places of each block.

	Returns
	-------
	dict[BlockPlace, frozenset[BlockPlace]]
		The places of the repeated blocks, each with the set of places sharing its block.
	"""
	places_by_place = dict[BlockPlace, frozenset[BlockPlace]]()

	for places in blocks.values():
		place_count = len(places)
		if place_count < 2:
			continue

		place_set = frozenset(places)

		for block_place in places:
			places_by_place[block_place] = place_set

	return places_by_place


def shift_places(place_set: frozenset[BlockPlace], step: int) -> frozenset[BlockPlace]:
	"""
	Return the places of the blocks starting a number of code lines after or before given places.

	Parameters
	----------
	place_set
		The places.
	step
		How many code lines further, negative for earlier lines.

	Returns
	-------
	frozenset[BlockPlace]
		The shifted places.

	Examples
	--------
	>>> shift_places(frozenset({BlockPlace(0, 3)}), 1)
	frozenset({BlockPlace(file_index=0, position=4)})
	"""
	shifted_places = frozenset(
		BlockPlace(block_place.file_index, block_place.position + step) for block_place in place_set
	)

	return shifted_places


def is_repeated_set(place_set: frozenset[BlockPlace], places_by_place: dict[BlockPlace, frozenset[BlockPlace]]) -> bool:
	"""
	Return whether some places are exactly the places of one repeated block.

	Parameters
	----------
	place_set
		The places.
	places_by_place
		The places of each repeated block.

	Returns
	-------
	bool
		True when the block starting at one of the places is repeated at these places and nowhere else.
	"""
	first_place = min(place_set, key=lambda block_place: (block_place.file_index, block_place.position))
	repeated_set = places_by_place.get(first_place)
	is_repeated = repeated_set == place_set

	return is_repeated


def describe_repetition(
	place_set: frozenset[BlockPlace],
	files_lines: list[list[CodeLine]],
	places_by_place: dict[BlockPlace, frozenset[BlockPlace]],
) -> str:
	"""
	Return the warning of a repeated block, measured as long as the next blocks stay repeated at the same places.

	Parameters
	----------
	place_set
		The places where the first block of the repetition starts.
	files_lines
		The code lines of each compared file.
	places_by_place
		The places of each repeated block.

	Returns
	-------
	str
		The length, the first and last line numbers at each place, and the first line.
	"""
	extra_lines = 0
	next_set = shift_places(place_set, NEXT_STEP)
	is_continued = is_repeated_set(next_set, places_by_place)

	while is_continued:
		extra_lines += 1
		next_set = shift_places(next_set, NEXT_STEP)
		is_continued = is_repeated_set(next_set, places_by_place)

	line_count = MINIMUM_BLOCK_LINES + extra_lines
	ordered_places = sorted(place_set, key=lambda block_place: (block_place.file_index, block_place.position))
	place_texts = [describe_place(block_place, line_count, files_lines) for block_place in ordered_places]
	joined_places = PLACE_SEPARATOR.join(place_texts)
	first_place = ordered_places[0]
	first_code_line = files_lines[first_place.file_index][first_place.position]
	block_problem = BLOCK_PROBLEM.format(line_count=line_count, places=joined_places, first_line=first_code_line.text)

	return block_problem


def describe_place(block_place: BlockPlace, line_count: int, files_lines: list[list[CodeLine]]) -> str:
	"""
	Return the file and the first and last line numbers of a repeated block.

	Parameters
	----------
	block_place
		Where the block starts.
	line_count
		The number of code lines of the block.
	files_lines
		The code lines of each compared file.

	Returns
	-------
	str
		Such as ``src/a.py:12-20``.
	"""
	code_lines = files_lines[block_place.file_index]
	first_line = code_lines[block_place.position]
	last_position = block_place.position + line_count - 1
	last_line = code_lines[last_position]
	place_text = BLOCK_PLACE.format(path=first_line.path, first_number=first_line.number, last_number=last_line.number)

	return place_text


def read_code_lines(path: Path) -> list[CodeLine]:
	"""
	Return the lines of code of a file that a copy would repeat.

	Docstrings, comments, blank lines and closing brackets are left out, and so are the lines a copy does not make:
	every line of an import, every line of a function signature, imposed by the code it fits, and the members of an
	enum written ``NAME = auto()``.

	Parameters
	----------
	path
		The file.

	Returns
	-------
	list[CodeLine]
		The kept lines, in order.
	"""
	text = path.read_text()
	tree = ast.parse(text)
	docstring_lines = find_docstring_lines(tree)
	import_lines = find_import_lines(tree)
	signature_lines = find_signature_lines(tree)
	skipped_lines = docstring_lines | import_lines | signature_lines
	regions = find_regions(tree)
	code_lines = list[CodeLine]()

	path_text = str(path)
	text_lines = text.splitlines()

	for number, line in enumerate(text_lines, start=1):
		stripped_line = line.strip()
		is_member = ENUM_MEMBER.fullmatch(stripped_line) is not None
		is_skipped = number in skipped_lines or stripped_line == "" or stripped_line.startswith(SKIPPED_STARTS)
		is_skipped = is_skipped or is_member
		if not is_skipped:
			region = regions.get(number, MODULE_REGION)
			code_line = CodeLine(path_text, number, stripped_line, region)
			code_lines.append(code_line)

	return code_lines


def find_docstring_lines(tree: ast.Module) -> set[int]:
	r"""
	Return the numbers of the lines that belong to a docstring, of a module, a class, a function or an attribute.

	An attribute docstring, such as the one of an enum member, is a text alone right after an assignment.

	Parameters
	----------
	tree
		The parsed file.

	Returns
	-------
	set[int]
		The line numbers, from 1.

	Examples
	--------
	>>> sorted(find_docstring_lines(ast.parse("'''\nDoc.\n'''\nvalue = 1\n'''Value.'''\n")))
	[1, 2, 3, 5]
	"""
	docstring_lines = set[int]()

	statements = [node for node in ast.walk(tree) if isinstance(node, ast.Expr)]

	for statement in statements:
		value = statement.value
		is_text = isinstance(value, ast.Constant) and isinstance(value.value, str)
		if is_text:
			last_line = statement.end_lineno or statement.lineno
			line_after = last_line + 1
			statement_lines = range(statement.lineno, line_after)
			docstring_lines.update(statement_lines)

	return docstring_lines


def find_import_lines(tree: ast.Module) -> set[int]:
	r"""
	Return the numbers of the lines that belong to an import, the names of an import on several lines included.

	Parameters
	----------
	tree
		The parsed file.

	Returns
	-------
	set[int]
		The line numbers, from 1.

	Examples
	--------
	>>> sorted(find_import_lines(ast.parse("from os import (\n\tpath,\n\tsep,\n)\nvalue = 1\n")))
	[1, 2, 3, 4]
	"""
	import_lines = set[int]()

	imports = [node for node in ast.walk(tree) if isinstance(node, IMPORT_NODES)]

	for statement in imports:
		last_line = statement.end_lineno or statement.lineno
		line_after = last_line + 1
		statement_lines = range(statement.lineno, line_after)
		import_lines.update(statement_lines)

	return import_lines


def find_regions(tree: ast.Module) -> dict[int, int]:
	r"""
	Return, for each line inside a function or a class, the first line of the innermost one holding it.

	Parameters
	----------
	tree
		The parsed file.

	Returns
	-------
	dict[int, int]
		The region of each line inside a function or a class; the lines of the module level are absent.

	Examples
	--------
	>>> code = "class Sale:\n\tdef pay(self):\n\t\treturn 1\n\tdef refund(self):\n\t\treturn 2\n"
	>>> find_regions(ast.parse(code))
	{1: 1, 2: 2, 3: 2, 4: 4, 5: 4}
	"""
	regions = dict[int, int]()

	region_nodes = [node for node in ast.walk(tree) if isinstance(node, REGION_NODES)]
	# An inner function starts after the function holding it, so it is written last and wins.
	ordered_nodes = sorted(region_nodes, key=lambda node: node.lineno)

	for node in ordered_nodes:
		last_line = node.end_lineno or node.lineno
		line_after = last_line + 1
		node_lines = range(node.lineno, line_after)

		for line_number in node_lines:
			regions[line_number] = node.lineno

	return regions


def find_signature_lines(tree: ast.Module) -> set[int]:
	r"""
	Return the numbers of the lines of the function signatures, from ``def`` to the line before the body.

	Parameters
	----------
	tree
		The parsed file.

	Returns
	-------
	set[int]
		The line numbers, from 1.

	Examples
	--------
	>>> sorted(find_signature_lines(ast.parse("def pay(\n\tamount,\n):\n\treturn amount\n")))
	[1, 2, 3]
	"""
	signature_lines = set[int]()

	functions = [node for node in ast.walk(tree) if isinstance(node, FUNCTION_NODES)]

	for function in functions:
		first_statement = function.body[0]
		statement_lines = range(function.lineno, first_statement.lineno)
		signature_lines.update(statement_lines)

	return signature_lines
