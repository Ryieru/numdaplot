"""
Base class of every statistic.

.. versionadded:: 0.1.0
"""


class Statistic:
	"""
	Base class of every statistic, a single result computed from a set of values.

	A statistic is immutable and checks its settings when it is created.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> isinstance(ndp.Mean(), ndp.Statistic)
	True
	"""
