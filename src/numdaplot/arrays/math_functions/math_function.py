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
	>>> values = ndp.Array.from_list([1.0, 4.0])
	>>> for function in [ndp.SquareRoot(), ndp.Logarithm(base=2)]:
	... 	print(values.apply(function))
	Array([1., 2.], dtype=FLOAT64)
	Array([0., 2.], dtype=FLOAT64)
	"""
