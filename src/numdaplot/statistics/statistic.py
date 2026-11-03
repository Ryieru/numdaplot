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
	>>> prices = ndp.Array.from_list([10.0, 30.0])
	>>> for statistic in [ndp.Min(), ndp.Mean(), ndp.Max()]:
	... 	print(prices.compute(statistic).to_value())
	10.0
	20.0
	30.0
	"""
