"""
Error raised when the suffixes of a join are empty or the same.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_SUFFIXES_MESSAGE = "Expected two different non-empty suffixes, got {left!r} and {right!r}."


class InvalidSuffixesError(NumdaplotError):
	"""
	Raised when a ``JoinSuffixes`` has an empty suffix, or the same suffix on both sides.

	Either would leave two columns of a join with the same name.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The suffix of the columns of the joined Table.
	right
		The suffix of the columns of the other Table.

	Attributes
	----------
	left
		The suffix of the columns of the joined Table.
	right
		The suffix of the columns of the other Table.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.JoinSuffixes(left="_2025", right="_2025")
	... except ndp.InvalidSuffixesError as error:
	... 	print(error)
	Expected two different non-empty suffixes, got '_2025' and '_2025'.
	"""

	def __init__(self, left: str, right: str) -> None:
		"""
		Build the error message from the two suffixes.

		.. versionadded:: 0.1.0

		Parameters
		----------
		left
			The suffix of the columns of the joined Table.
		right
			The suffix of the columns of the other Table.
		"""
		message = INVALID_SUFFIXES_MESSAGE.format(left=left, right=right)
		super().__init__(message)

		self.left = left
		self.right = right
