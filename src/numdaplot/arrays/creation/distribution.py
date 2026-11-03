"""
Base class of every random distribution.

.. versionadded:: 0.1.0
"""


class Distribution:
	"""
	Base class of every random distribution, the law followed by the values of ``Array.random``.

	A distribution is immutable and checks its settings when it is created.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> isinstance(ndp.Uniform(low=0, high=1), ndp.Distribution)
	True
	"""
