"""
Error raised when a statistic appears twice in a list of statistics.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

DUPLICATE_STATISTIC_MESSAGE = "The statistic {statistic!r} appears more than once."


class DuplicateStatisticError(NumdaplotError):
	"""
	Raised when the same statistic appears twice in the functions of a ``Description``, which would give two equal rows.

	Two statistics are the same when they have the same class and the same settings, so ``Quantile(0.25)`` and
	``Quantile(0.75)`` are different.

	.. versionadded:: 0.1.0

	Parameters
	----------
	statistic
		The statistic given twice.

	Attributes
	----------
	statistic
		The statistic given twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Description(functions=[ndp.Sum(), ndp.Sum()])
	... except ndp.DuplicateStatisticError as error:
	... 	print(error)
	The statistic Sum() appears more than once.
	"""

	def __init__(self, statistic: object) -> None:
		"""
		Build the error message from the statistic given twice.

		.. versionadded:: 0.1.0

		Parameters
		----------
		statistic
			The statistic given twice.
		"""
		message = DUPLICATE_STATISTIC_MESSAGE.format(statistic=statistic)
		super().__init__(message)

		self.statistic = statistic
