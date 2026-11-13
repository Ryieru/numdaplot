"""Entry point of the checks: ``python tools/checks/run_checks.py commit|push|ci [base commit]``."""

import sys

from changed_files import GitAction
from check_plan import report_checks

ACTION_POSITION = 1
BASE_REF_POSITION = 2


def main() -> int:
	"""
	Run the checks of the git action given as first argument, compared in the CI with the commit given as second one.

	Returns
	-------
	int
		1 when a blocking check failed, which stops the git action, else 0.
	"""
	arguments = sys.argv
	action = GitAction(arguments[ACTION_POSITION])
	given_base_ref = ""
	argument_count = len(arguments)
	if argument_count > BASE_REF_POSITION:
		given_base_ref = arguments[BASE_REF_POSITION]

	exit_code = report_checks(action, given_base_ref)

	return exit_code


if __name__ == "__main__":
	exit_code = main()
	sys.exit(exit_code)
