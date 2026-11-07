"""
Error raised when a value has no new value in a ValueMapping.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

UNMATCHED_VALUE_MESSAGE = (
	"The value {value!r} has no ValueChange. Add one, or give others=Unmatched.MISSING to make it missing."
)


class UnmatchedValueError(NumdaplotError):
	"""
	Raised when a value of an Array has no new value in a ``ValueMapping`` whose ``others`` is ``Unmatched.ERROR``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The first value without new value.

	Attributes
	----------
	value
		The first value without new value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> sexes = ndp.Array.from_list([1, 2, 3])
	>>> try:
	... 	sexes.apply(ndp.ValueMapping(changes=[ndp.ValueChange(1, "Homme"), ndp.ValueChange(2, "Femme")]))
	... except ndp.UnmatchedValueError as error:
	... 	print(error)
	The value 3 has no ValueChange. Add one, or give others=Unmatched.MISSING to make it missing.
	"""

	def __init__(self, value: object) -> None:
		"""
		Build the error message from the value without new value.

		.. versionadded:: 0.1.0

		Parameters
		----------
		value
			The first value without new value.
		"""
		message = UNMATCHED_VALUE_MESSAGE.format(value=value)
		super().__init__(message)

		self.value = value
