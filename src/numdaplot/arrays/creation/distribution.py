"""
Base class of every random distribution.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.refused_operation_error import RefusedOperationError

CONSTRUCTOR_OPERATION = "Creating a Distribution with ndp.Distribution()"
CONSTRUCTOR_ALTERNATIVE = "a distribution such as ndp.Uniform"


class Distribution:
	"""
	Base class of every random distribution, the law followed by the values of ``Array.random``.

	A distribution is immutable and checks its settings when it is created.

	Only its subclasses are created: calling ``ndp.Distribution()`` raises ``RefusedOperationError``.

	Every distribution, passed to ``Array.random``:

	|Distribution|What it draws|Example|
	|---|---|---|
	|``Uniform``|Equally likely decimals from ``low`` to ``high``|``ndp.Uniform(low=0, high=10)``|
	|``Normal``|Decimals around a mean, following a bell curve|``ndp.Normal(mean=0, deviation=1)``|
	|``RandomIntegers``|Equally likely integers from ``low`` to ``high``|``ndp.RandomIntegers(low=1, high=6)``|

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> shape = ndp.Shape([3])
	>>> for distribution in [ndp.Uniform(low=0, high=10), ndp.RandomIntegers(low=0, high=10)]:
	... 	print(ndp.Array.random(distribution, shape=shape, seed=1))
	Array([5.11821625, 9.50463696, 1.44159613], dtype=FLOAT64)
	Array([5, 5, 8], dtype=INT64)
	"""

	def __init__(self) -> None:
		"""
		Refuse the creation of the base class itself, and let a subclass be created.

		.. versionadded:: 0.1.0

		Raises
		------
		RefusedOperationError
			When the created object is a Distribution and not one of its subclasses.
		"""
		created_class = type(self)
		if created_class is Distribution:
			raise RefusedOperationError(CONSTRUCTOR_OPERATION, CONSTRUCTOR_ALTERNATIVE)
