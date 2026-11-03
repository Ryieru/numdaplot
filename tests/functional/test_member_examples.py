"""
Functional tests running the examples of the documented enum members.

doctest only collects the docstrings of modules, classes and functions: the docstring written under an enum
member, such as ``Type.INT8``, is checked here instead.

.. versionadded:: 0.1.0
"""

import ast
import doctest
import inspect
import io
from pathlib import Path

import pytest

SOURCE_FOLDER = Path(__file__).parent.parent.parent / "src" / "numdaplot"
EXAMPLES_HEADER = "Examples"
EXAMPLE_NAME = "{path}:{class_name}.{member_name}"


def find_member_docstrings(path: Path) -> list[tuple[str, str]]:
	"""
	Return the docstrings with examples written under the members of the classes of a file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		A source file.

	Returns
	-------
	list[tuple[str, str]]
		The name of each member, such as ``type.py:Type.INT8``, and its cleaned docstring.
	"""
	tree = ast.parse(path.read_text())
	member_docstrings = list[tuple[str, str]]()
	class_nodes = [node for node in tree.body if isinstance(node, ast.ClassDef)]

	for class_node in class_nodes:
		statements = class_node.body
		statement_pairs = zip(statements, statements[1:], strict=False)

		for assignment, following in statement_pairs:
			member_docstring = read_member_docstring(assignment, following)
			if member_docstring is None:
				continue

			member_name, docstring = member_docstring
			name = EXAMPLE_NAME.format(path=path.name, class_name=class_node.name, member_name=member_name)
			member_docstrings.append((name, docstring))

	return member_docstrings


def read_member_docstring(assignment: ast.stmt, following: ast.stmt) -> tuple[str, str] | None:
	"""
	Return the name of a class member and the docstring with examples written under it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	assignment
		A statement of a class body.
	following
		The statement right after it.

	Returns
	-------
	tuple[str, str] or None
		The member name and its cleaned docstring, or ``None`` when the statements are not
		a member followed by a docstring holding examples.
	"""
	if not isinstance(assignment, ast.Assign):
		return None

	target = assignment.targets[0]
	if not isinstance(target, ast.Name):
		return None

	if not isinstance(following, ast.Expr):
		return None

	constant = following.value
	if not isinstance(constant, ast.Constant):
		return None

	raw_docstring = constant.value
	if not isinstance(raw_docstring, str):
		return None

	if EXAMPLES_HEADER not in raw_docstring:
		return None

	docstring = inspect.cleandoc(raw_docstring)

	return target.id, docstring


def find_all_member_docstrings() -> list[tuple[str, str]]:
	"""
	Return the docstrings with examples of the enum members of the whole package.

	.. versionadded:: 0.1.0

	Returns
	-------
	list[tuple[str, str]]
		The name and the docstring of each member, in the order of the files.
	"""
	all_docstrings = list[tuple[str, str]]()
	source_paths = sorted(SOURCE_FOLDER.rglob("*.py"))

	for source_path in source_paths:
		member_docstrings = find_member_docstrings(source_path)
		all_docstrings.extend(member_docstrings)

	return all_docstrings


MEMBER_DOCSTRINGS = find_all_member_docstrings()
MEMBER_NAMES = [name for name, _ in MEMBER_DOCSTRINGS]


def test_every_enum_member_with_a_docstring_was_found() -> None:
	"""
	Check that the member docstrings are found, Type.INT8 among them.

	.. versionadded:: 0.1.0
	"""
	assert "type.py:Type.INT8" in MEMBER_NAMES


@pytest.mark.parametrize(("name", "docstring"), MEMBER_DOCSTRINGS, ids=MEMBER_NAMES)
def test_member_example_gives_its_written_output(name: str, docstring: str) -> None:
	"""
	Check that each example of an enum member gives the output written under it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		The name of the member.
	docstring
		Its docstring.
	"""
	parser = doctest.DocTestParser()
	example_test = parser.get_doctest(docstring, {}, name, None, 0)
	runner = doctest.DocTestRunner(optionflags=doctest.NORMALIZE_WHITESPACE)
	report = io.StringIO()

	result = runner.run(example_test, out=report.write)

	assert result.failed == 0, report.getvalue()
