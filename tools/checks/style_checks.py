"""Rules of writing a parser can only guess, checked on the added lines: nested calls, history, examples."""

import ast
import re
from collections import defaultdict
from pathlib import Path

from changed_files import AddedLine
from check_report import CheckResult, Severity

ALLOWED_OUTER_CALLS = frozenset({"cast", "isinstance", "issubclass", "type"})
# Wrapping a single call in one of these turns a numpy scalar into a Python value, which the project allows.
SCALAR_CONVERSIONS = frozenset({"bool", "int", "float", "str"})
NESTED_CHECK_NAME = "nested calls (CODE-10), a guess to read"
HISTORY_CHECK_NAME = "history of the code in comments and documents (COM-3, DOC-4), a guess to read"
NESTED_PROBLEM = "{path}:{line} {kind}: {code}"
TEXT_PROBLEM = "{path}:{line} {text}"
EXAMPLE_CHECK_NAME = "example of the code in place of a general rule in comments (COM-2), a guess to read"
EXAMPLE_WORDS = re.compile(r"\b(such as|as in|e\.g\.|for example|for instance)\b", re.IGNORECASE)
COMMENT_MARKS = {".py": "#", ".yml": "#", ".yaml": "#", ".toml": "#", ".css": "/*"}
HISTORY_WORDS = re.compile(
	r"\b(now|previously|no longer|used to|anymore|was renamed|changed to|new implementation|from now on|"
	r"for now|old version|we decided)\b",
	re.IGNORECASE,
)
ALLOWED_HISTORY_MARKS = ("versionchanged", "versionadded", "Renamed from")
DOCUMENT_SUFFIXES = (".py", ".md")
HISTORY_FREE_DOCUMENTS = frozenset({"CHANGELOG.md"})
COMMENT_MARK = "#"
MAX_SHOWN_CODE = 90


def check_nested_calls(scope_files: list[Path], added_lines: list[AddedLine]) -> CheckResult:
	"""
	Return the added lines that use the result of a call without naming it first.

	Parameters
	----------
	scope_files
		The changed Python files.
	added_lines
		The lines the git action adds.

	Returns
	-------
	CheckResult
		One warning per nested call on an added line.
	"""
	added_numbers = defaultdict[str, set[int]](set)

	for added_line in added_lines:
		added_numbers[added_line.path].add(added_line.number)

	problems = list[str]()

	for path in scope_files:
		text = path.read_text()
		tree = ast.parse(text)
		file_numbers = added_numbers[str(path)]

		for node in ast.walk(tree):
			kind = describe_nesting(node)
			node_line = getattr(node, "lineno", 0)
			if kind != "" and node_line in file_numbers:
				node_code = ast.unparse(node)
				code = node_code[:MAX_SHOWN_CODE]
				nested_problem = NESTED_PROBLEM.format(path=path, line=node_line, kind=kind, code=code)
				problems.append(nested_problem)

	result = CheckResult(NESTED_CHECK_NAME, Severity.WARNING, problems)

	return result


def describe_nesting(node: ast.AST) -> str:
	"""
	Return how a node uses the result of a call directly, or an empty text when it does not.

	Parameters
	----------
	node
		Any node of a parsed file.

	Returns
	-------
	str
		``"call in a call"``, ``"chained call"``, ``"indexed call"``, ``"returned call"``, ``"calculated call"`` or
		``"tested call"``, else an empty text.

	Examples
	--------
	>>> describe_nesting(ast.parse("print(len(users))").body[0].value)
	'call in a call'
	>>> describe_nesting(ast.parse("user_count = len(users)").body[0])
	''
	"""
	if isinstance(node, ast.Call):
		call_nesting = describe_call_nesting(node)
		return call_nesting

	if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Call):
		return "indexed call"

	if isinstance(node, ast.Return) and isinstance(node.value, ast.Call):
		return "returned call"

	if isinstance(node, ast.BinOp) and (isinstance(node.left, ast.Call) or isinstance(node.right, ast.Call)):
		return "calculated call"

	if isinstance(node, ast.If | ast.While):
		has_tested_call = holds_call(node.test)
		if has_tested_call:
			return "tested call"

	return ""


def describe_call_nesting(call: ast.Call) -> str:
	"""
	Return how a call uses the result of another call: as an argument, or by calling a method on it.

	Parameters
	----------
	call
		A call node.

	Returns
	-------
	str
		``"call in a call"``, ``"chained call"``, or an empty text.

	Examples
	--------
	>>> describe_call_nesting(ast.parse("name.strip().lower()").body[0].value)
	'chained call'
	"""
	is_chained = isinstance(call.func, ast.Attribute) and isinstance(call.func.value, ast.Call)
	is_parent = is_parent_access(call)
	if is_chained and not is_parent:
		return "chained call"

	outer_name = call.func.id if isinstance(call.func, ast.Name) else ""
	if outer_name in ALLOWED_OUTER_CALLS:
		return ""

	given_values = [*call.args, *(keyword.value for keyword in call.keywords)]
	is_scalar_conversion = outer_name in SCALAR_CONVERSIONS and len(given_values) == 1
	if is_scalar_conversion:
		return ""

	inner_calls = [value for value in given_values if isinstance(value, ast.Call)]
	computed_calls = [inner_call for inner_call in inner_calls if not is_construction(inner_call)]
	if computed_calls:
		return "call in a call"

	return ""


def is_parent_access(call: ast.Call) -> bool:
	"""
	Return whether a call reaches a method of the parent class through ``super()``, which Python requires.

	Parameters
	----------
	call
		A call whose called object is the attribute of another call.

	Returns
	-------
	bool
		True for ``super().method(...)``.

	Examples
	--------
	>>> is_parent_access(ast.parse("super().__init__(message)", mode="eval").body)
	True
	"""
	called = call.func
	inner_call = called.value if isinstance(called, ast.Attribute) else None
	is_super = (
		isinstance(inner_call, ast.Call) and isinstance(inner_call.func, ast.Name) and inner_call.func.id == "super"
	)

	return is_super


def is_construction(call: ast.Call) -> bool:
	"""
	Return whether a call creates an object of a class, such as a settings object given to an operation.

	The API takes one settings object per operation, created where it is given: ``table.filter(ndp.Filter(...))``.

	Parameters
	----------
	call
		A call node.

	Returns
	-------
	bool
		True when the called name, or the last part of a dotted name, starts with a capital letter.

	Examples
	--------
	>>> is_construction(ast.parse("ndp.Filter(conditions=[])", mode="eval").body)
	True
	"""
	called = call.func
	called_name = ""
	if isinstance(called, ast.Name):
		called_name = called.id

	if isinstance(called, ast.Attribute):
		called_name = called.attr

	is_class = called_name[:1].isupper()

	return is_class


def holds_call(test: ast.expr) -> bool:
	"""
	Return whether the test of a condition calls a function, which should be named before the condition.

	A type test such as ``isinstance`` stays in the condition, as everywhere in the project.

	Parameters
	----------
	test
		The test of an ``if`` or a ``while``.

	Returns
	-------
	bool
		True when a call appears anywhere in the test.

	Examples
	--------
	>>> holds_call(ast.parse("len(items) > 0", mode="eval").body)
	True
	>>> holds_call(ast.parse("not isinstance(bound, Array)", mode="eval").body)
	False
	"""
	walked_nodes = ast.walk(test)
	inner_nodes = list(walked_nodes)
	calls = [inner_node for inner_node in inner_nodes if isinstance(inner_node, ast.Call)]
	tested_calls = [call for call in calls if not is_type_test(call)]
	has_call = bool(tested_calls)

	return has_call


def is_type_test(call: ast.Call) -> bool:
	"""
	Return whether a call tests the type of a value, such as ``isinstance``.

	Parameters
	----------
	call
		A call node.

	Returns
	-------
	bool
		True for a call of ``isinstance``, ``issubclass`` or another allowed outer call.

	Examples
	--------
	>>> is_type_test(ast.parse("isinstance(value, int)", mode="eval").body)
	True
	"""
	called_name = call.func.id if isinstance(call.func, ast.Name) else ""
	is_allowed = called_name in ALLOWED_OUTER_CALLS

	return is_allowed


def check_history_words(added_lines: list[AddedLine]) -> CheckResult:
	"""
	Return the added comments, docstrings and document lines that may tell the history of the code.

	The changelog and the version notes tell the history on purpose, so they are left out.

	Parameters
	----------
	added_lines
		The lines the git action adds.

	Returns
	-------
	CheckResult
		One warning per line holding a word such as "now" or "previously".
	"""
	problems = list[str]()

	for added_line in added_lines:
		path = Path(added_line.path)
		is_document = path.suffix in DOCUMENT_SUFFIXES and path.name not in HISTORY_FREE_DOCUMENTS
		is_code_line = path.suffix == ".py" and not is_text_line(added_line.text)
		has_version_mark = any(mark in added_line.text for mark in ALLOWED_HISTORY_MARKS)
		match = HISTORY_WORDS.search(added_line.text)
		is_history = is_document and not is_code_line and not has_version_mark and match is not None
		if is_history:
			text = added_line.text.strip()
			history_problem = TEXT_PROBLEM.format(path=path, line=added_line.number, text=text)
			problems.append(history_problem)

	result = CheckResult(HISTORY_CHECK_NAME, Severity.WARNING, problems)

	return result


def is_text_line(text: str) -> bool:
	r"""
	Return whether a line of a Python file is text for a reader: a comment, or a line of a docstring.

	A line of a docstring is guessed from its shape: it is not a statement that Python can parse on its own.

	Parameters
	----------
	text
		The line.

	Returns
	-------
	bool
		True for a comment or a line that does not parse as code.

	Examples
	--------
	>>> is_text_line("\t# The provider rejects more decimals."), is_text_line("\tvalue = 1")
	(True, False)
	"""
	stripped_text = text.strip()
	is_comment = stripped_text.startswith(COMMENT_MARK)
	if is_comment:
		return True

	try:
		ast.parse(stripped_text)
	except SyntaxError:
		return True

	return False


def check_example_words(added_lines: list[AddedLine]) -> CheckResult:
	r"""
	Return the added comments that may cite a case of the code instead of stating the general rule.

	Docstrings are left out: their examples show a real use on purpose.

	Parameters
	----------
	added_lines
		The lines the git action adds.

	Returns
	-------
	CheckResult
		One warning per comment holding words such as "for example" or "as in".

	Examples
	--------
	>>> from changed_files import AddedLine
	>>> example_line = AddedLine("src/a.py", 3, "\t# A base class, such as Rule, has no page.")
	>>> rule_line = AddedLine("src/a.py", 4, "\t# A base class has no page.")
	>>> check_example_words([example_line, rule_line]).problems
	['src/a.py:3 # A base class, such as Rule, has no page.']
	"""
	problems = list[str]()

	for added_line in added_lines:
		path = Path(added_line.path)
		text = added_line.text.strip()
		comment_mark = COMMENT_MARKS.get(path.suffix)
		is_comment = comment_mark is not None and text.startswith(comment_mark)
		match = EXAMPLE_WORDS.search(text)
		is_example = is_comment and match is not None
		if is_example:
			example_problem = TEXT_PROBLEM.format(path=path, line=added_line.number, text=text)
			problems.append(example_problem)

	result = CheckResult(EXAMPLE_CHECK_NAME, Severity.WARNING, problems)

	return result
