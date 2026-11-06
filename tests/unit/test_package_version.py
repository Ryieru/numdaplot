"""
Unit tests of the version of the installed package.

.. versionadded:: 0.1.0
"""

from importlib.metadata import PackageNotFoundError

import pytest

from numdaplot import package_version
from numdaplot.package_version import UNKNOWN_VERSION, find_package_version

INSTALLED_VERSION = "1.2.3"
VERSION_FUNCTION_NAME = "version"


def give_installed_version(_package_name: str) -> str:
	"""
	Fake reading of the information of an installed package.

	.. versionadded:: 0.1.0

	Parameters
	----------
	_package_name
		The name of the package, not used.

	Returns
	-------
	str
		A version.
	"""
	return INSTALLED_VERSION


def refuse_package(package_name: str) -> str:
	"""
	Fake reading of the information of a package that is not installed.

	.. versionadded:: 0.1.0

	Parameters
	----------
	package_name
		The name of the package.

	Raises
	------
	PackageNotFoundError
		Always.
	"""
	raise PackageNotFoundError(package_name)


def test_find_package_version_reads_the_installed_package(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the version comes from the information of the package.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the reading.
	"""
	monkeypatch.setattr(package_version, VERSION_FUNCTION_NAME, give_installed_version)

	found_version = find_package_version()

	assert found_version == INSTALLED_VERSION


def test_find_package_version_stays_usable_without_installation(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check the version of a code that runs without being installed.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the reading.
	"""
	monkeypatch.setattr(package_version, VERSION_FUNCTION_NAME, refuse_package)

	found_version = find_package_version()

	assert found_version == UNKNOWN_VERSION
