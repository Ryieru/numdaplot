"""
Launch the whole numdaplot test suite.

The suite covers the unit tests, the functional tests and every docstring example,
as configured in pyproject.toml.

.. versionadded:: 0.1.0
"""

import sys

import pytest


def main() -> int:
	"""
	Run pytest with the configuration of pyproject.toml.

	The command line arguments given to this script are passed to pytest,
	so ``python run_tests.py -k between`` runs only the matching tests.

	.. versionadded:: 0.1.0

	Returns
	-------
	int
		The pytest exit code, 0 when every test passes.
	"""
	pytest_exit_code = pytest.main()
	exit_code = int(pytest_exit_code)

	return exit_code


if __name__ == "__main__":
	exit_code = main()
	sys.exit(exit_code)
