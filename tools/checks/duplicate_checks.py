"""Code repeated in the source: identical function bodies, and the files compared."""

import ast
from collections import defaultdict
from pathlib import Path

from check_report import CheckResult, Severity

COMPARED_ROOTS = ("src", "tools")
PYTHON_PATTERN = "*.py"
MINIMUM_BODY_STATEMENTS = 4
BODY_CHECK_NAME = "identical function bodies (at least 4 statements)"
BODY_PROBLEM = "same body: {places}"
PLACE_SEPARATOR = " | "
PLACE_PATH_END = ":"


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
