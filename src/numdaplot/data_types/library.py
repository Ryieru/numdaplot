"""
Libraries that numdaplot types are converted to and from.

.. versionadded:: 0.1.0
"""

from enum import Enum


class Library(Enum):
	"""
	Underlying library on the other side of a type conversion, read on ``UnsupportedTypeError.library``.

	The value of each member is the name of the library, as shown in error messages.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> import numpy
	>>> try:
	... 	ndp.Array.from_numpy(numpy.array([1 + 2j]))
	... except ndp.UnsupportedTypeError as error:
	... 	print(error.library.value)
	numpy
	"""

	NUMPY = "numpy"
	"""numpy, used by Array."""

	PANDAS = "pandas"
	"""pandas, used by Table."""
