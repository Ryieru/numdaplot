"""
Base class of every math function.

.. versionadded:: 0.1.0
"""


class MathFunction:
	"""
	Base class of every math function, applied to each value of a number Array by ``Array.apply``.

	A math function is immutable and checks its settings when it is created.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> isinstance(ndp.SquareRoot(), ndp.MathFunction)
	True
	"""
