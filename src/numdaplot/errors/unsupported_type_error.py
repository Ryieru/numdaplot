"""
Error raised when a type has no equivalent between numdaplot and an underlying library.

.. versionadded:: 0.1.0
"""

from numdaplot.data_types.library import Library
from numdaplot.errors.numdaplot_error import NumdaplotError

UNSUPPORTED_TYPE_MESSAGE = "The type {type_name} has no equivalent between numdaplot and {library_name}."


class UnsupportedTypeError(NumdaplotError):
	"""
	Raised when a type cannot be converted between numdaplot and numpy or pandas.

	For example, numpy has no ``CATEGORY`` type, and numdaplot has no complex number type.

	.. versionadded:: 0.1.0

	Parameters
	----------
	type_name
		Name of the type that cannot be converted.
	library
		Library on the other side of the conversion, ``Library.NUMPY`` or ``Library.PANDAS``.

	Attributes
	----------
	type_name
		Name of the type that cannot be converted.
	library
		Library on the other side of the conversion, ``Library.NUMPY`` or ``Library.PANDAS``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> import numpy
	>>> try:
	... 	ndp.Array.from_numpy(numpy.array([1 + 2j]))
	... except ndp.UnsupportedTypeError as error:
	... 	print(error)
	The type complex128 has no equivalent between numdaplot and numpy.
	"""

	def __init__(self, type_name: str, library: Library) -> None:
		"""
		Build the error message from the type and the library.

		.. versionadded:: 0.1.0

		Parameters
		----------
		type_name
			Name of the type that cannot be converted.
		library
			Library on the other side of the conversion, ``Library.NUMPY`` or ``Library.PANDAS``.
		"""
		message = UNSUPPORTED_TYPE_MESSAGE.format(type_name=type_name, library_name=library.value)
		super().__init__(message)
		self.type_name = type_name
		self.library = library
