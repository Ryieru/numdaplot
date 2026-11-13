"""
Error raised when a statistic appears twice in a list of statistics.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

DUPLICATE_STATISTIC_MESSAGE = "The statistic {statistic!r} appears more than once."
SAME_NAME_MESSAGE = (
	"The statistics {statistic!r} and {other_statistic!r} give rows of the same name. "
	"Use aggregate with a result_name for each, or one description per statistic."
)


class DuplicateStatisticError(NumdaplotError):
	"""
	Raised when two statistics of a ``Description`` would give rows of the same name.

	Two statistics have the same name when they have the same class and the same settings, so ``Quantile(0.25)`` and
	``Quantile(0.75)`` are different. Two ``Share`` have the same name whatever their rules.

	.. versionadded:: 0.1.0

	.. versionchanged:: 0.2.0
		Also raised for two different statistics of the same name, such as two ``Share``.

	Parameters
	----------
	statistic
		The statistic given twice, or the first of two statistics of the same name.
	other_statistic
		The second statistic of the same name. When omitted, ``statistic`` itself appears twice.

	Attributes
	----------
	statistic
		The statistic given twice, or the first of two statistics of the same name.
	other_statistic
		The second statistic of the same name, ``None`` when ``statistic`` itself appears twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Description(functions=[ndp.Sum(), ndp.Sum()])
	... except ndp.DuplicateStatisticError as error:
	... 	print(error)
	The statistic Sum() appears more than once.
	>>> try:
	... 	ndp.Description(functions=[ndp.Share(ndp.Greater(65)), ndp.Share(ndp.Less(18))])
	... except ndp.DuplicateStatisticError as error:
	... 	print(error)
	The statistics Share(rule=Greater(value=65), missing=<CountedMissing.EXCLUDED: 1>)
	and Share(rule=Less(value=18), missing=<CountedMissing.EXCLUDED: 1>) give rows of the same name.
	Use aggregate with a result_name for each, or one description per statistic.
	"""

	def __init__(self, statistic: object, other_statistic: object | None = None) -> None:
		"""
		Build the error message from the statistic given twice, or from the two statistics of the same name.

		.. versionadded:: 0.1.0

		.. versionchanged:: 0.2.0
			Takes the second statistic of the same name.

		Parameters
		----------
		statistic
			The statistic given twice, or the first of two statistics of the same name.
		other_statistic
			The second statistic of the same name, ``statistic`` itself appearing twice when omitted.
		"""
		message = DUPLICATE_STATISTIC_MESSAGE.format(statistic=statistic)
		if other_statistic is not None:
			message = SAME_NAME_MESSAGE.format(statistic=statistic, other_statistic=other_statistic)

		super().__init__(message)

		self.statistic = statistic
		self.other_statistic = other_statistic
