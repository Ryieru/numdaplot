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
	>>> shape = ndp.Shape((3,))
	>>> for distribution in [ndp.Uniform(low=0, high=10), ndp.RandomIntegers(low=0, high=10)]:
	... 	print(ndp.Array.random(distribution, shape=shape, seed=1))
	Array([5.11821625, 9.50463696, 1.44159613], dtype=FLOAT64)
	Array([5, 5, 8], dtype=INT64)
	"""
