"""
Error raised when a weight is negative.

.. versionadded:: 0.2.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_WEIGHT_MESSAGE = "Expected weights of at least 0 in the column {column_name!r}, got {weight}."


class InvalidWeightError(NumdaplotError):
	"""
	Raised when a column of weights holds a negative weight.

	A weight tells how many units a row stands for, such as the people of a population a survey answer represents.

	.. versionadded:: 0.2.0

	Parameters
	----------
	weight
		The first negative weight.
	column_name
		The name of the column of weights.

	Attributes
	----------
	weight
		The first negative weight.
	column_name
		The name of the column of weights.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> sexes = ndp.Array.from_list([1, 2])
	>>> weights = ndp.Array.from_list([300.0, -2.0])
	>>> answers = ndp.Table.from_arrays({"sex": sexes, "weight": weights})
	>>> try:
	... 	answers.count_values(ndp.ValueCount(column="sex", weights="weight"))
	... except ndp.InvalidWeightError as error:
	... 	print(error)
	Expected weights of at least 0 in the column 'weight', got -2.0.
	"""

	def __init__(self, weight: float, column_name: str) -> None:
		"""
		Build the error message from the weight and its column.

		.. versionadded:: 0.2.0

		Parameters
		----------
		weight
			The first negative weight.
		column_name
			The name of the column of weights.
		"""
		message = INVALID_WEIGHT_MESSAGE.format(column_name=column_name, weight=weight)
		super().__init__(message)
		self.weight = weight
		self.column_name = column_name
