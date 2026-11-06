"""
Version of the installed package.

.. versionadded:: 0.1.0
"""

from importlib.metadata import PackageNotFoundError, version

PACKAGE_NAME = "numdaplot"
UNKNOWN_VERSION = "0+unknown"


def find_package_version() -> str:
	"""
	Return the version of numdaplot, as written in the information of the installed package.

	.. versionadded:: 0.1.0

	Returns
	-------
	str
		The version, or ``0+unknown`` for a code that runs without being installed.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.package_version import find_package_version
	>>> find_package_version() == ndp.__version__
	True
	"""
	try:
		package_version = version(PACKAGE_NAME)
	except PackageNotFoundError:
		return UNKNOWN_VERSION

	return package_version
