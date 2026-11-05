"""
Error raised when an operation does not apply to the types of its values.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

TYPE_NAME_SEPARATOR = " and "
INCOMPATIBLE_TYPES_MESSAGE = "Cannot apply {operation} to {type_names}."
COLUMN_TYPE_NAME = "the {type_name} column {column_name!r}"


class IncompatibleTypesError(NumdaplotError):
	"""
	Raised when an operation, a rule, a statistic or a math function does not apply to the types it receives.

	For example, a number cannot be added to a text, and ``Contains`` only applies to text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operation
		Name of the operation: an operator such as ``"+"``, or a rule, statistic or function name.
	type_names
		Names of the ``ndp.Type`` members the operation received, in order.

	Attributes
	----------
	operation
		Name of the operation: an operator such as ``"+"``, or a rule, statistic or function name.
	type_names
		Names of the ``ndp.Type`` members the operation received, in order.
	column_name
		Name of the Table column holding the first type, or ``None`` for an Array or a type alone.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> array = ndp.Array.from_list([1, 2])
	>>> try:
	... 	array + "euros"
	... except ndp.IncompatibleTypesError as error:
	... 	print(error)
	Cannot apply + to INT64 and TEXT.
	>>> sales = ndp.Table.from_arrays({"city": ndp.Array.from_list(["Paris"])})
	>>> mean_city = ndp.Calculation(column="city", function=ndp.Mean())
	>>> try:
	... 	sales.aggregate(ndp.Aggregation(calculations=[mean_city]))
	... except ndp.IncompatibleTypesError as error:
	... 	print(error)
	Cannot apply Mean to the TEXT column 'city'.
	"""

	def __init__(self, operation: str, type_names: list[str]) -> None:
		"""
		Build the error message from the operation and the type names.

		.. versionadded:: 0.1.0

		Parameters
		----------
		operation
			Name of the operation: an operator such as ``"+"``, or a rule, statistic or function name.
		type_names
			Names of the ``ndp.Type`` members the operation received, in order.
		"""
		joined_type_names = TYPE_NAME_SEPARATOR.join(type_names)
		message = INCOMPATIBLE_TYPES_MESSAGE.format(operation=operation, type_names=joined_type_names)
		super().__init__(message)

		self.operation = operation
		self.type_names = list(type_names)
		self.column_name: str | None = None

	def name_column(self, column_name: str) -> None:
		"""
		Name the Table column holding the first type in the message, unless a column is already named.

		.. versionadded:: 0.1.0

		Parameters
		----------
		column_name
			The name of the column.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> error = ndp.IncompatibleTypesError("Greater", ["DATETIME", "INT64"])
		>>> error.name_column("day")
		>>> print(error)
		Cannot apply Greater to the DATETIME column 'day' and INT64.
		"""
		if self.column_name is not None:
			return

		self.column_name = column_name
		first_type_name, *other_type_names = self.type_names
		named_type = COLUMN_TYPE_NAME.format(type_name=first_type_name, column_name=column_name)
		joined_type_names = TYPE_NAME_SEPARATOR.join([named_type, *other_type_names])
		message = INCOMPATIBLE_TYPES_MESSAGE.format(operation=self.operation, type_names=joined_type_names)
		self.args = (message,)
