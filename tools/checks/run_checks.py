"""Entry point of the checks, called by the git hooks: ``python tools/checks/run_checks.py commit|push``."""

import sys

from changed_files import GitAction
from check_plan import report_checks


def main() -> int:
	"""
	Run the checks of the git action given as argument.

	Returns
	-------
	int
		1 when a blocking check failed, which stops the git action, else 0.
	"""
	action = GitAction(sys.argv[1])
	exit_code = report_checks(action)

	return exit_code


if __name__ == "__main__":
	exit_code = main()
	sys.exit(exit_code)
