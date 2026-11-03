"""
Error raised when a random seed is negative.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_SEED_MESSAGE = "Expected a seed of at least 0, got {seed}."


class InvalidSeedError(NumdaplotError):
	"""
	Raised when a random draw is given a negative seed.

	.. versionadded:: 0.1.0

	Parameters
	----------
	seed
		The rejected seed.

	Attributes
	----------
	seed
		The rejected seed.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> dice = ndp.RandomIntegers(low=1, high=6)
	>>> try:
	... 	ndp.Array.random(dice, shape=ndp.Shape((3,)), seed=-1)
	... except ndp.InvalidSeedError as error:
	... 	print(error)
	Expected a seed of at least 0, got -1.
	"""

	def __init__(self, seed: int) -> None:
		"""
		Build the error message from the seed.

		.. versionadded:: 0.1.0

		Parameters
		----------
		seed
			The rejected seed.
		"""
		message = INVALID_SEED_MESSAGE.format(seed=seed)
		super().__init__(message)

		self.seed = seed
