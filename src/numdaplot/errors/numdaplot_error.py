"""
Base class of every numdaplot error.

.. versionadded:: 0.1.0
"""


class NumdaplotError(Exception):
	"""
	Base class of every error raised by numdaplot.

	Catch it to handle any numdaplot error at once, or catch a precise subclass
	to handle only one case.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Quantile(1.5)
	... except ndp.NumdaplotError as error:
	... 	print(error)
	Expected a fraction between 0 and 1, got 1.5.
	"""
