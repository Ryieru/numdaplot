"""Results of the checks of the repository, and their report."""

import re
from dataclasses import dataclass, field
from enum import Enum

PASSED_MARK = "ok"
BLOCKING_MARK = "FAILED"
WARNING_MARK = "warning"
PROBLEM_PREFIX = "    - "
PLACED_PROBLEM = re.compile(r"^(?P<path>[^\s:]+):(?P<line>\d+) (?P<text>.*)$")
PLACED_ANNOTATION = "::{level} file={path},line={line}::{name}: {text}"
ANNOTATION = "::{level}::{name}: {problem}"
# GitHub reads these characters of an annotation as escapes, so they are escaped first.
ANNOTATION_ESCAPES = (("%", "%25"), ("\r", "%0D"), ("\n", "%0A"))
SUMMARY_BLOCKED = "{count} blocking check(s) failed: the git action is stopped."
SUMMARY_PASSED = "Every blocking check passed."
SUMMARY_WARNINGS = "{count} warning(s) to read before going on."


class Severity(Enum):
	"""Whether a failed check stops the git action or only warns."""

	BLOCKING = "blocking"
	"""The git action stops while the check fails."""

	WARNING = "warning"
	"""The check may be wrong, so its problems are only shown."""


ANNOTATION_LEVELS = {Severity.BLOCKING: "error", Severity.WARNING: "warning"}


@dataclass(frozen=True)
class CheckResult:
	"""
	The problems one check found, and how much they matter.

	Parameters
	----------
	name
		The name of the check, shown in the report.
	severity
		Whether a problem stops the git action.
	problems
		One line per problem, empty when the check passed.
	"""

	name: str
	severity: Severity
	problems: list[str] = field(default_factory=list[str])


def write_result(result: CheckResult) -> list[str]:
	"""
	Return the lines of the report of one check.

	Parameters
	----------
	result
		The result of the check.

	Returns
	-------
	list[str]
		The name of the check with its mark, then one line per problem.

	Examples
	--------
	>>> write_result(CheckResult("ruff", Severity.BLOCKING))
	['[ok] ruff']
	"""
	mark = PASSED_MARK
	if result.problems:
		mark = BLOCKING_MARK if result.severity == Severity.BLOCKING else WARNING_MARK

	lines = [f"[{mark}] {result.name}"]

	for problem in result.problems:
		lines.append(PROBLEM_PREFIX + problem)

	return lines


def escape_annotation(text: str) -> str:
	r"""
	Return a text written so that GitHub shows it as it is in an annotation.

	Parameters
	----------
	text
		The text of a problem, which may hold line breaks.

	Returns
	-------
	str
		The text with its percent signs and line breaks escaped.

	Examples
	--------
	>>> escape_annotation("100%\nok")
	'100%25%0Aok'
	"""
	escaped_text = text

	for character, escape in ANNOTATION_ESCAPES:
		escaped_text = escaped_text.replace(character, escape)

	return escaped_text


def write_annotation(result: CheckResult, problem: str) -> str:
	"""
	Return the GitHub workflow command showing one problem of a check, on its line when the problem names one.

	Parameters
	----------
	result
		The check that found the problem.
	problem
		The problem, starting with ``path:line`` when it is placed in a file.

	Returns
	-------
	str
		An ``::error`` command for a blocking check, a ``::warning`` command for a warning.

	Examples
	--------
	>>> nested = CheckResult("nested calls", Severity.WARNING)
	>>> write_annotation(nested, "src/a.py:3 call in a call: print(len(users))")
	'::warning file=src/a.py,line=3::nested calls: call in a call: print(len(users))'
	>>> write_annotation(CheckResult("pages", Severity.BLOCKING), "Share: no page")
	'::error::pages: Share: no page'
	"""
	level = ANNOTATION_LEVELS[result.severity]
	escaped_problem = escape_annotation(problem)
	placed_problem = PLACED_PROBLEM.match(escaped_problem)
	if placed_problem is None:
		annotation = ANNOTATION.format(level=level, name=result.name, problem=escaped_problem)
		return annotation

	problem_parts = placed_problem.groupdict()
	annotation = PLACED_ANNOTATION.format(level=level, name=result.name, **problem_parts)

	return annotation


def count_blocking_failures(results: list[CheckResult]) -> int:
	"""
	Return the number of blocking checks that found problems.

	Parameters
	----------
	results
		The results of every check.

	Returns
	-------
	int
		The number of failed blocking checks.

	Examples
	--------
	>>> count_blocking_failures([CheckResult("ruff", Severity.BLOCKING, ["E501"])])
	1
	"""
	failures = [result for result in results if result.problems and result.severity == Severity.BLOCKING]
	failure_count = len(failures)

	return failure_count


def write_summary(results: list[CheckResult]) -> list[str]:
	"""
	Return the last lines of the report: whether the git action goes on, and the number of warnings.

	Parameters
	----------
	results
		The results of every check.

	Returns
	-------
	list[str]
		One line for the blocking checks, and one for the warnings when there are some.

	Examples
	--------
	>>> write_summary([CheckResult("ruff", Severity.BLOCKING)])
	['Every blocking check passed.']
	"""
	failure_count = count_blocking_failures(results)
	warnings = [result for result in results if result.problems and result.severity == Severity.WARNING]
	warning_count = len(warnings)
	summary = [SUMMARY_PASSED]
	if failure_count > 0:
		summary = [SUMMARY_BLOCKED.format(count=failure_count)]

	if warning_count > 0:
		warning_line = SUMMARY_WARNINGS.format(count=warning_count)
		summary.append(warning_line)

	return summary
