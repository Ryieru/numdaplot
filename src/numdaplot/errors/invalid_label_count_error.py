"""
Error raised when Brackets are not given exactly one label per bracket.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_LABEL_COUNT_MESSAGE = "Expected {bracket_count} labels, one per bracket, got {label_count}."


class InvalidLabelCountError(NumdaplotError):
	"""
	Raised when the labels of ``Brackets`` are not exactly one per bracket.

	There is one bracket between two limits, plus one for each open end.

	.. versionadded:: 0.1.0

	Parameters
	----------
	bracket_count
		The number of brackets.
	label_count
		The number of labels given.

	Attributes
	----------
	bracket_count
		The number of brackets.
	label_count
		The number of labels given.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Brackets(limits=[0, 18, 65], labels=["child", "adult", "senior"])
	... except ndp.InvalidLabelCountError as error:
	... 	print(error)
	Expected 2 labels, one per bracket, got 3.
	"""

	def __init__(self, bracket_count: int, label_count: int) -> None:
		"""
		Build the error message from the two counts.

		.. versionadded:: 0.1.0

		Parameters
		----------
		bracket_count
			The number of brackets.
		label_count
			The number of labels given.
		"""
		message = INVALID_LABEL_COUNT_MESSAGE.format(bracket_count=bracket_count, label_count=label_count)
		super().__init__(message)

		self.bracket_count = bracket_count
		self.label_count = label_count
