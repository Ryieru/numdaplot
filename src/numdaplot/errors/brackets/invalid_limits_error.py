"""
Error raised when the limits of Brackets do not form valid brackets.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

TOO_FEW_LIMITS_MESSAGE = "Expected at least 2 limits, or 1 with an open first or last bracket, got {limit_count}."
UNORDERED_LIMITS_MESSAGE = "Expected limits in strictly increasing order, got {later_limit} after {earlier_limit}."
EMPTY_BRACKET_MESSAGE = "The bracket from {low} to {high} holds no integer."


class InvalidLimitsError(NumdaplotError):
	"""
	Raised when the limits of ``Brackets`` do not form valid brackets.

	The limits must strictly increase, and form at least one bracket. On a column of integers, each bracket between two
	limits must hold an integer.

	.. versionadded:: 0.1.0

	Parameters
	----------
	limits
		The limits of the brackets.
	empty_bracket
		The low and the high limit of a bracket holding no integer, when the limits are valid but that bracket is not.
		When omitted, the limits themselves are wrong.

	Attributes
	----------
	limits
		The limits of the brackets.
	empty_bracket
		The limits of the bracket holding no integer, ``None`` when the limits themselves are wrong.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Brackets(limits=[0, 10, 10])
	... except ndp.InvalidLimitsError as error:
	... 	print(error)
	Expected limits in strictly increasing order, got 10 after 10.
	>>> try:
	... 	ndp.Brackets(limits=[0])
	... except ndp.InvalidLimitsError as error:
	... 	print(error)
	Expected at least 2 limits, or 1 with an open first or last bracket, got 1.
	"""

	def __init__(self, limits: list[int | float], empty_bracket: list[int | float] | None = None) -> None:
		"""
		Build the error message from the first problem of the limits.

		.. versionadded:: 0.1.0

		Parameters
		----------
		limits
			The limits of the brackets.
		empty_bracket
			The low and the high limit of a bracket holding no integer. When omitted, the limits themselves are wrong.
		"""
		message = write_limits_message(limits, empty_bracket)
		super().__init__(message)

		self.limits = limits
		self.empty_bracket = empty_bracket


def write_limits_message(limits: list[int | float], empty_bracket: list[int | float] | None) -> str:
	"""
	Return the message naming the first problem of the limits of brackets.

	.. versionadded:: 0.1.0

	Parameters
	----------
	limits
		The limits of the brackets.
	empty_bracket
		The low and the high limit of a bracket holding no integer, or None.

	Returns
	-------
	str
		The empty bracket, else the first limit not greater than the previous one, else the number of limits.

	Examples
	--------
	>>> from numdaplot.errors.brackets.invalid_limits_error import write_limits_message
	>>> write_limits_message([5.2, 5.8], [5.2, 5.8])
	'The bracket from 5.2 to 5.8 holds no integer.'
	"""
	if empty_bracket is not None:
		low, high = empty_bracket
		empty_message = EMPTY_BRACKET_MESSAGE.format(low=low, high=high)
		return empty_message

	for earlier_limit, later_limit in zip(limits, limits[1:], strict=False):
		is_greater = later_limit > earlier_limit
		if not is_greater:
			unordered_message = UNORDERED_LIMITS_MESSAGE.format(earlier_limit=earlier_limit, later_limit=later_limit)
			return unordered_message

	limit_count = len(limits)
	too_few_message = TOO_FEW_LIMITS_MESSAGE.format(limit_count=limit_count)

	return too_few_message
