"""Entry point of the checks: ``python tools/checks/run_checks.py commit|push|ci <family> [base commit]``."""

import sys

from check_plan import report_checks
from check_request import read_request


def main() -> int:
	"""
	Run the checks written on the command line.

	Returns
	-------
	int
		1 when a blocking check failed, which stops the git action, else 0.
	"""
	request = read_request(sys.argv)
	exit_code = report_checks(request)

	return exit_code


if __name__ == "__main__":
	exit_code = main()
	sys.exit(exit_code)
