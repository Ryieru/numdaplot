"""
Libraries that numdaplot types are converted to and from.

.. versionadded:: 0.1.0
"""

from enum import Enum


class Library(Enum):
	"""
	Underlying library on the other side of a type conversion.

	The value of each member is the name of the library, as shown in error messages.

	.. versionadded:: 0.1.0
	"""

	NUMPY = "numpy"
	"""numpy, used by Array."""

	PANDAS = "pandas"
	"""pandas, used by Table."""
