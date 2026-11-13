"""Size of the files and of the functions, and number of arguments."""

import ast
from pathlib import Path

from check_report import CheckResult, Severity

MAX_FILE_LINES = 500
MAX_FUNCTION_LINES = 50
MAX_ARGUMENTS = 4
PACKAGE_FILE_NAME = "__init__.py"
BOUND_ARGUMENTS = frozenset({"self", "cls"})
FILE_CHECK_NAME = "file size (at most 500 lines, package __init__ excepted)"
FUNCTION_CHECK_NAME = "function size (at most 50 lines of code) and arguments (at most 4)"
FILE_PROBLEM = "{path}: {line_count} lines"
LONG_FUNCTION_PROBLEM = "{path}:{line} {name}: {code_lines} lines of code"
ARGUMENT_PROBLEM = "{path}:{line} {name}: {argument_count} arguments"


def check_file_sizes(python_files: list[Path]) -> CheckResult:
	"""
	Return the files longer than 500 lines, blank lines included.

	Parameters
	----------
	python_files
		The files checked.

	Returns
	-------
	CheckResult
		One problem per file too long.
	"""
	problems = list[str]()

	for path in python_files:
		if path.name == PACKAGE_FILE_NAME:
			continue

		text = path.read_text()
		line_count = text.count("\n")
		if line_count > MAX_FILE_LINES:
			file_problem = FILE_PROBLEM.format(path=path, line_count=line_count)
			problems.append(file_problem)

	result = CheckResult(FILE_CHECK_NAME, Severity.BLOCKING, problems)

	return result


def check_functions(python_files: list[Path]) -> CheckResult:
	"""
	Return the functions longer than 50 lines of code, and those taking more than 4 arguments.

	The docstring does not count in the size, since every function of numdaplot has a full docstring.

	Parameters
	----------
	python_files
		The files checked.

	Returns
	-------
	CheckResult
		One problem per function too long and per function taking too many arguments.
	"""
	problems = list[str]()

	for path in python_files:
		text = path.read_text()
		tree = ast.parse(text)
		functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)]

		for function in functions:
			function_problems = describe_function_problems(path, function)
			problems.extend(function_problems)

	result = CheckResult(FUNCTION_CHECK_NAME, Severity.BLOCKING, problems)

	return result


def describe_function_problems(path: Path, function: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
	"""
	Return the problems of one function: too many lines of code, too many arguments.

	Parameters
	----------
	path
		The file of the function.
	function
		The function node.

	Returns
	-------
	list[str]
		Zero, one or two problems.
	"""
	problems = list[str]()
	code_lines = count_code_lines(function)
	if code_lines > MAX_FUNCTION_LINES:
		long_problem = LONG_FUNCTION_PROBLEM.format(
			path=path, line=function.lineno, name=function.name, code_lines=code_lines
		)
		problems.append(long_problem)

	argument_count = count_arguments(function)
	if argument_count > MAX_ARGUMENTS:
		argument_problem = ARGUMENT_PROBLEM.format(
			path=path, line=function.lineno, name=function.name, argument_count=argument_count
		)
		problems.append(argument_problem)

	return problems


def count_code_lines(function: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
	r"""
	Return the number of lines of a function body after its docstring, blank lines included.

	Parameters
	----------
	function
		The function node.

	Returns
	-------
	int
		The number of lines, 0 for a function holding only its docstring.

	Examples
	--------
	>>> node = ast.parse("def f():\n\t'''Doc.'''\n\tvalue = 1\n\n\treturn value\n").body[0]
	>>> count_code_lines(node)
	3
	"""
	body = function.body
	first_statement = body[0]
	has_docstring = isinstance(first_statement, ast.Expr) and isinstance(first_statement.value, ast.Constant)
	code_statements = body[1:] if has_docstring else body
	if not code_statements:
		return 0

	first_code = code_statements[0]
	last_line = function.end_lineno or first_code.lineno
	code_lines = last_line - first_code.lineno + 1

	return code_lines


def count_arguments(function: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
	"""
	Return the number of arguments of a function, ``self`` and ``cls`` left out.

	Parameters
	----------
	function
		The function node.

	Returns
	-------
	int
		The positional, keyword and variadic arguments.

	Examples
	--------
	>>> count_arguments(ast.parse("def f(self, a, b=1, *c): pass").body[0])
	3
	"""
	arguments = function.args
	named_arguments = [*arguments.posonlyargs, *arguments.args, *arguments.kwonlyargs]
	counted_names = [argument.arg for argument in named_arguments if argument.arg not in BOUND_ARGUMENTS]
	argument_count = len(counted_names)
	if arguments.vararg is not None:
		argument_count += 1

	if arguments.kwarg is not None:
		argument_count += 1

	return argument_count
