"""
Unit tests of the check of optional packages.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.files.missing_dependency_error import MissingDependencyError
from numdaplot.tables.files.optional_package import require_package

INSTALLED_PACKAGE = "numpy"
MISSING_PACKAGE = "numdaplot_package_that_does_not_exist"
EXTRA_NAME = "excel"


def test_require_package_accepts_an_installed_package() -> None:
	"""
	Check that an installed package passes.

	.. versionadded:: 0.1.0
	"""
	require_package(INSTALLED_PACKAGE, EXTRA_NAME)


def test_require_package_names_the_extra_of_a_missing_package() -> None:
	"""
	Check that a missing package raises MissingDependencyError naming the extra.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(MissingDependencyError) as error_info:
		require_package(MISSING_PACKAGE, EXTRA_NAME)

	error = error_info.value
	assert error.package_name == MISSING_PACKAGE
	assert error.extra_name == EXTRA_NAME
