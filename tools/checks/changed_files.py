"""Files and lines a git action brings, read from git."""

import re
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

UPSTREAM_REF = "@{upstream}"
DEFAULT_BASE_REF = "origin/main"
INDEX_NAME = "index"
MISSING_COMMIT_MARK = "0"
CHANGED_FILTER = "--diff-filter=ACMR"
PYTHON_SUFFIX = ".py"
CHECKED_ROOTS = ("src", "tests", "tools")
HUNK_HEADER = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")
FILE_HEADER = "+++ b/"
ADDED_PREFIX = "+"
ADDED_FILE_PREFIX = "+++"
GIT_ERROR = "git {arguments} failed: {error}"
ARGUMENT_SEPARATOR = " "


class GitAction(Enum):
	"""The git action the checks run before."""

	COMMIT = "commit"
	"""A commit: the staged files are checked, with the fast checks."""

	PUSH = "push"
	"""A push: every file changed since the remote branch is checked, with every check."""

	CI = "ci"
	"""A CI run: every file changed since a given commit is checked, without the tools the CI jobs already run."""


class GitCommandError(Exception):
	"""A git command the checks need failed, so the checks cannot run."""


@dataclass(frozen=True)
class AddedLine:
	"""
	A line a git action adds to a file.

	Parameters
	----------
	path
		The file, relative to the repository.
	number
		The number of the line in the new file, from 1.
	text
		The text of the line.
	"""

	path: str
	number: int
	text: str


@dataclass(frozen=True)
class CheckScope:
	"""
	What a git action brings: the Python files changed and the lines added.

	Parameters
	----------
	action
		The git action.
	base_ref
		The commit the changes are compared with: the index for a commit, the remote branch for a push.
	python_files
		The Python files changed under src, tests and tools, that still exist.
	added_lines
		Every line added to these files.
	"""

	action: GitAction
	base_ref: str
	python_files: list[Path]
	added_lines: list[AddedLine]


def run_git(arguments: list[str]) -> str:
	"""
	Return the output of a git command.

	Parameters
	----------
	arguments
		The arguments after ``git``.

	Returns
	-------
	str
		The standard output.

	Raises
	------
	GitCommandError
		When the command fails, with its error output.
	"""
	command = ["git", *arguments]
	completed = subprocess.run(command, capture_output=True, text=True, check=False)
	if completed.returncode != 0:
		argument_text = ARGUMENT_SEPARATOR.join(arguments)
		error_text = completed.stderr.strip()
		message = GIT_ERROR.format(arguments=argument_text, error=error_text)
		raise GitCommandError(message)

	return completed.stdout


def find_base_ref() -> str:
	"""
	Return the remote branch a push is compared with: the upstream branch, else origin/main.

	Returns
	-------
	str
		A git reference.
	"""
	try:
		upstream = run_git(["rev-parse", "--abbrev-ref", UPSTREAM_REF])
	except GitCommandError:
		return DEFAULT_BASE_REF

	upstream_name = upstream.strip()

	return upstream_name


def find_ci_base_ref(given_base_ref: str) -> str:
	"""
	Return the commit a CI run is compared with: the given one, else origin/main.

	Parameters
	----------
	given_base_ref
		The commit before the push or the base of the pull request. GitHub gives a commit made of zeros, or nothing,
		when there is none.

	Returns
	-------
	str
		A git reference.

	Examples
	--------
	>>> find_ci_base_ref("93c40c3"), find_ci_base_ref("0000000"), find_ci_base_ref("")
	('93c40c3', 'origin/main', 'origin/main')
	"""
	stripped_base_ref = given_base_ref.strip(MISSING_COMMIT_MARK)
	if stripped_base_ref == "":
		return DEFAULT_BASE_REF

	return given_base_ref


def read_scope(action: GitAction, given_base_ref: str) -> CheckScope:
	"""
	Return the files and the lines a git action brings.

	Parameters
	----------
	action
		A commit, which brings the staged changes, a push, which brings the commits after the remote branch, or a CI
		run, which brings the commits after the given commit.
	given_base_ref
		The commit a CI run is compared with, unused by the other actions.

	Returns
	-------
	CheckScope
		The changed Python files and the added lines.
	"""
	diff_target = ["--cached"]
	base_ref = INDEX_NAME
	if action == GitAction.PUSH:
		base_ref = find_base_ref()
		diff_target = [f"{base_ref}..HEAD"]

	if action == GitAction.CI:
		base_ref = find_ci_base_ref(given_base_ref)
		diff_target = [f"{base_ref}..HEAD"]

	name_output = run_git(["diff", "--name-only", CHANGED_FILTER, *diff_target])
	changed_names = name_output.split()
	python_files = [Path(name) for name in changed_names if is_checked_python_file(name)]
	diff_output = run_git(["diff", "-U0", CHANGED_FILTER, *diff_target])
	added_lines = read_added_lines(diff_output)
	scope = CheckScope(action, base_ref, python_files, added_lines)

	return scope


def is_checked_python_file(name: str) -> bool:
	"""
	Return whether a changed file is a Python file of the checked folders that still exists.

	Parameters
	----------
	name
		The path of the file, relative to the repository.

	Returns
	-------
	bool
		True for an existing ``.py`` file under src, tests or tools.

	Examples
	--------
	>>> is_checked_python_file("README.md")
	False
	"""
	path = Path(name)
	is_python = path.suffix == PYTHON_SUFFIX
	is_checked_root = name.startswith(CHECKED_ROOTS)
	is_checked = is_python and is_checked_root and path.exists()

	return is_checked


def read_added_lines(diff_output: str) -> list[AddedLine]:
	r"""
	Return the lines a unified diff without context adds, with their file and their number.

	Parameters
	----------
	diff_output
		The output of ``git diff -U0``.

	Returns
	-------
	list[AddedLine]
		Every added line, in order.

	Examples
	--------
	>>> diff = "+++ b/src/a.py\n@@ -1,0 +2,1 @@\n+value = 1\n"
	>>> read_added_lines(diff)
	[AddedLine(path='src/a.py', number=2, text='value = 1')]
	"""
	added_lines = list[AddedLine]()
	current_path = ""
	next_number = 0

	for line in diff_output.splitlines():
		is_file_header = line.startswith(FILE_HEADER)
		if is_file_header:
			current_path = line.removeprefix(FILE_HEADER)
			continue

		header = HUNK_HEADER.match(line)
		if header is not None:
			next_number = int(header.group(1))
			continue

		is_added = line.startswith(ADDED_PREFIX) and not line.startswith(ADDED_FILE_PREFIX)
		if is_added:
			added_text = line.removeprefix(ADDED_PREFIX)
			added_lines.append(AddedLine(current_path, next_number, added_text))
			next_number += 1

	return added_lines
