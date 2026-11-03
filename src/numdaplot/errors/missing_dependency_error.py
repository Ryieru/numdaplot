"""
Error raised when a file format needs an optional package that is not installed.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

MISSING_DEPENDENCY_MESSAGE = (
	"This file format needs the {package_name} package, install it with: pip install numdaplot[{extra_name}]"
)


class MissingDependencyError(NumdaplotError):
	"""
	Raised when reading or writing Excel or Parquet files without the matching optional package.

	.. versionadded:: 0.1.0

	Parameters
	----------
	package_name
		Name of the missing package, such as ``openpyxl``.
	extra_name
		Name of the numdaplot extra that installs it, such as ``excel``.

	Attributes
	----------
	package_name
		Name of the missing package, such as ``openpyxl``.
	extra_name
		Name of the numdaplot extra that installs it, such as ``excel``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> print(ndp.MissingDependencyError("openpyxl", "excel"))
	This file format needs the openpyxl package, install it with: pip install numdaplot[excel]
	"""

	def __init__(self, package_name: str, extra_name: str) -> None:
		"""
		Build the error message from the package name and the extra name.

		.. versionadded:: 0.1.0

		Parameters
		----------
		package_name
			Name of the missing package, such as ``openpyxl``.
		extra_name
			Name of the numdaplot extra that installs it, such as ``excel``.
		"""
		message = MISSING_DEPENDENCY_MESSAGE.format(package_name=package_name, extra_name=extra_name)
		super().__init__(message)

		self.package_name = package_name
		self.extra_name = extra_name
