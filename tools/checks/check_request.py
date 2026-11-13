"""What a run of the checks is asked: its git action, the families of checks, and the commit the CI compares with."""

from dataclasses import dataclass
from enum import Enum

from changed_files import GitAction

ACTION_POSITION = 1
FAMILY_POSITION = 2
BASE_REF_POSITION = 3


class CheckFamily(Enum):
	"""A family of checks the CI runs in its own job."""

	CODING_STYLE = "style"
	"""The coding style rules: sizes, repeated code, nested calls, history and examples in comments."""

	PUBLIC_API = "api"
	"""The public API documentation: version note, changelog entry and page of each added or removed public name."""


ALL_FAMILIES = (CheckFamily.CODING_STYLE, CheckFamily.PUBLIC_API)


@dataclass(frozen=True)
class CheckRequest:
	"""
	What a run of the checks is asked.

	Parameters
	----------
	action
		The git action the checks run before, or the CI.
	families
		The families of checks to run: every family before a commit or a push, one family in each CI job.
	given_base_ref
		The commit the CI compares with, empty for the other actions.
	"""

	action: GitAction
	families: tuple[CheckFamily, ...]
	given_base_ref: str


def read_request(arguments: list[str]) -> CheckRequest:
	"""
	Return the request written on the command line: ``commit``, ``push``, or ``ci <family> [base commit]``.

	Parameters
	----------
	arguments
		The command line, the script first.

	Returns
	-------
	CheckRequest
		Every family for a commit or a push, the given family and commit for the CI.

	Raises
	------
	ValueError
		When the action or the family is unknown.

	Examples
	--------
	>>> read_request(["run_checks.py", "push"]).families == ALL_FAMILIES
	True
	>>> read_request(["run_checks.py", "ci", "api", "93c40c3"])
	CheckRequest(action=<GitAction.CI: 'ci'>, families=(<CheckFamily.PUBLIC_API: 'api'>,), given_base_ref='93c40c3')
	"""
	action = GitAction(arguments[ACTION_POSITION])
	if action != GitAction.CI:
		every_family_request = CheckRequest(action, ALL_FAMILIES, "")
		return every_family_request

	family = CheckFamily(arguments[FAMILY_POSITION])
	given_base_ref = ""
	argument_count = len(arguments)
	if argument_count > BASE_REF_POSITION:
		given_base_ref = arguments[BASE_REF_POSITION]

	ci_request = CheckRequest(action, (family,), given_base_ref)

	return ci_request
