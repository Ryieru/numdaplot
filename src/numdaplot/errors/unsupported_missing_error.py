"""
Error raised when a missing value is given for a type that cannot hold one.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

UNSUPPORTED_MISSING_MESSAGE = "{type_name} values cannot be missing, use a decimal, date or duration type."


class UnsupportedMissingError(NumdaplotError):
	"""
	Raised when a missing value (``None``) is given for a type that cannot hold one in an Array.

	Only decimals (NaN), dates, datetimes and durations (NaT) can be missing in an Array.

	.. versionadded:: 0.1.0

	Parameters
	----------
	type_name
		Name of the ``ndp.Type`` member that cannot hold a missing value.

	Attributes
	----------
	type_name
		Name of the ``ndp.Type`` member that cannot hold a missing value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Array.from_list([1, None])
	... except ndp.UnsupportedMissingError as error:
	... 	print(error)
	INT64 values cannot be missing, use a decimal, date or duration type.
	"""

	def __init__(self, type_name: str) -> None:
		"""
		Build the error message from the type name.

		.. versionadded:: 0.1.0

		Parameters
		----------
		type_name
			Name of the ``ndp.Type`` member that cannot hold a missing value.
		"""
		message = UNSUPPORTED_MISSING_MESSAGE.format(type_name=type_name)
		super().__init__(message)

		self.type_name = type_name
