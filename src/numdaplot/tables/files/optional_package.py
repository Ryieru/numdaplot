"""
Packages that only some file formats need.

.. versionadded:: 0.1.0
"""

from importlib.util import find_spec

from numdaplot.errors.missing_dependency_error import MissingDependencyError


def require_package(package_name: str, extra_name: str) -> None:
	"""
	Check that an optional package is installed.

	.. versionadded:: 0.1.0

	Parameters
	----------
	package_name
		The name of the package to import, such as ``openpyxl``.
	extra_name
		The numdaplot extra that installs it, such as ``excel``.

	Raises
	------
	MissingDependencyError
		When the package is not installed, with the command that installs it.

	Examples
	--------
	>>> from numdaplot.tables.files.optional_package import require_package
	>>> require_package("pandas", "unused")
	"""
	package_spec = find_spec(package_name)
	if package_spec is None:
		raise MissingDependencyError(package_name, extra_name)
