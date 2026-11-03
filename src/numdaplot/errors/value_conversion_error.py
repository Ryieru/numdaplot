"""
Error raised when values cannot be stored in a type without losing information.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

VALUE_CONVERSION_MESSAGE = "Cannot store {source_type_name} values as {target_type_name} without losing information."


class ValueConversionError(NumdaplotError):
	"""
	Raised when values cannot be stored in a type without losing information.

	For example, decimals stored as integers, or a text stored as a number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	source_type_name
		Name of the ``ndp.Type`` member of the given values.
	target_type_name
		Name of the ``ndp.Type`` member they should be stored as.

	Attributes
	----------
	source_type_name
		Name of the ``ndp.Type`` member of the given values.
	target_type_name
		Name of the ``ndp.Type`` member they should be stored as.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Array.from_list([1.5, 2.5], dtype=ndp.Type.INT64)
	... except ndp.ValueConversionError as error:
	... 	print(error)
	Cannot store FLOAT64 values as INT64 without losing information.
	"""

	def __init__(self, source_type_name: str, target_type_name: str) -> None:
		"""
		Build the error message from the source type name and the target type name.

		.. versionadded:: 0.1.0

		Parameters
		----------
		source_type_name
			Name of the ``ndp.Type`` member of the given values.
		target_type_name
			Name of the ``ndp.Type`` member they should be stored as.
		"""
		message = VALUE_CONVERSION_MESSAGE.format(source_type_name=source_type_name, target_type_name=target_type_name)
		super().__init__(message)

		self.source_type_name = source_type_name
		self.target_type_name = target_type_name
