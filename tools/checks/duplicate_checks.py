"""Code repeated in the source: identical function bodies, and identical blocks of lines."""

import ast
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from check_report import CheckResult, Severity

COMPARED_ROOTS = ("src", "tools")
PYTHON_PATTERN = "*.py"
MINIMUM_BODY_STATEMENTS = 4
BLOCK_LINE_COUNT = 6
SKIPPED_STARTS = ("#", "from ", "import ", ")", "]", "}")
BODY_CHECK_NAME = "identical function bodies (at least 4 statements)"
BLOCK_CHECK_NAME = "identical blocks of 6 code lines"
BODY_PROBLEM = "same body: {places}"
BLOCK_PROBLEM = "same lines: {places}, starting with {first_line!r}"
PLACE_SEPARATOR = " | "
PLACE_PATH_END = ":"


@dataclass(frozen=True)
class CodeLine:
	"""
	A line of code, out of any docstring or comment.

	Parameters
	----------
	path
		The file.
	number
		The number of the line, from 1.
	text
		The line without its indentation.
	"""

	path: str
	number: int
	text: str


def list_compared_files() -> list[Path]:
	"""
	Return every Python file of src and tools, the code a change may repeat.

	Returns
	-------
	list[Path]
		The files, sorted.
	"""
	compared_files = list[Path]()

	for root in COMPARED_ROOTS:
		root_path = Path(root)
		root_files = root_path.rglob(PYTHON_PATTERN)
		compared_files.extend(root_files)

	sorted_files = sorted(compared_files)

	return sorted_files


def check_identical_bodies(scope_files: list[Path]) -> CheckResult:
	"""
	Return the function bodies of at least 4 statements that another function repeats, when a changed file holds one.

	Parameters
	----------
	scope_files
		The changed files.

	Returns
	-------
	CheckResult
		One problem per group of identical bodies.
	"""
	scope_names = {str(path) for path in scope_files}
	places_by_body = defaultdict[str, list[str]](list)

	for path in list_compared_files():
		text = path.read_text()
		tree = ast.parse(text)
		functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

		for function in functions:
			body_key = describe_body(function)
			if body_key != "":
				places_by_body[body_key].append(f"{path}:{function.lineno} {function.name}")

	problems = list[str]()

	for places in places_by_body.values():
		place_paths = set[str]()
		for place in places:
			place_path, _, _ = place.partition(PLACE_PATH_END)
			place_paths.add(place_path)

		is_repeated = len(places) > 1 and bool(place_paths & scope_names)
		if is_repeated:
			joined_places = PLACE_SEPARATOR.join(places)
			body_problem = BODY_PROBLEM.format(places=joined_places)
			problems.append(body_problem)

	result = CheckResult(BODY_CHECK_NAME, Severity.BLOCKING, problems)

	return result


def describe_body(function: ast.FunctionDef) -> str:
	r"""
	Return the structure of a function body without its docstring, empty when it is too short to compare.

	Parameters
	----------
	function
		The function node.

	Returns
	-------
	str
		The dump of each statement, one per line, or an empty text below 4 statements.

	Examples
	--------
	>>> describe_body(ast.parse("def f():\n\treturn 1\n").body[0])
	''
	"""
	statements = function.body
	first_statement = statements[0]
	has_docstring = isinstance(first_statement, ast.Expr) and isinstance(first_statement.value, ast.Constant)
	code_statements = statements[1:] if has_docstring else statements
	statement_count = len(code_statements)
	if statement_count < MINIMUM_BODY_STATEMENTS:
		return ""

	statement_dumps = [ast.dump(statement) for statement in code_statements]
	body_key = "\n".join(statement_dumps)

	return body_key


def check_identical_blocks(scope_files: list[Path]) -> CheckResult:
	"""
	Return the blocks of 6 code lines found twice, when a changed file holds one of them.

	Parameters
	----------
	scope_files
		The changed files.

	Returns
	-------
	CheckResult
		One warning per group of identical blocks: some are only alike, such as similar checks of settings.
	"""
	scope_names = {str(path) for path in scope_files}
	starts_by_block = defaultdict[tuple[str, ...], list[CodeLine]](list)

	for path in list_compared_files():
		code_lines = read_code_lines(path)
		code_line_count = len(code_lines)
		start_count = code_line_count - BLOCK_LINE_COUNT + 1

		for start in range(start_count):
			window = code_lines[start : start + BLOCK_LINE_COUNT]
			block = tuple(code_line.text for code_line in window)
			starts_by_block[block].append(window[0])

	problems = list[str]()

	for block, starts in starts_by_block.items():
		start_paths = {start.path for start in starts}
		is_repeated = len(starts) > 1 and bool(start_paths & scope_names)
		if is_repeated:
			places = ", ".join(f"{start.path}:{start.number}" for start in starts)
			first_line = block[0]
			block_problem = BLOCK_PROBLEM.format(places=places, first_line=first_line)
			problems.append(block_problem)

	result = CheckResult(BLOCK_CHECK_NAME, Severity.WARNING, problems)

	return result


def read_code_lines(path: Path) -> list[CodeLine]:
	"""
	Return the lines of code of a file, without docstrings, comments, imports, blank lines and closing brackets.

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
	code_lines = list[CodeLine]()

	path_text = str(path)
	text_lines = text.splitlines()

	for number, line in enumerate(text_lines, start=1):
		stripped_line = line.strip()
		is_skipped = number in docstring_lines or stripped_line == "" or stripped_line.startswith(SKIPPED_STARTS)
		if not is_skipped:
			code_line = CodeLine(path_text, number, stripped_line)
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
