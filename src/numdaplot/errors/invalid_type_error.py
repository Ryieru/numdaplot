"""
Error raised when a setting or an argument receives a value of the wrong type.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

TYPE_MESSAGE = "{target_name} expects {expected}, got {given!r}."
CLASS_GIVEN_MESSAGE = "ndp.{class_name} is a class, use ndp.{class_name}() instead."


class InvalidTypeError(NumdaplotError):
	"""
	Raised when a setting or an argument receives a value of the wrong type, such as a number for ``Region`` rows.

	A class given in place of an object, such as ``ndp.Sum`` in place of ``ndp.Sum()``, gets a message naming the
	parentheses.

	.. versionadded:: 0.1.0

	Parameters
	----------
	target_name
		What received the value, such as ``"Region rows"``.
	expected
		What it accepts, such as ``"an Index, a Range or None"``.
	given
		The rejected value.

	Attributes
	----------
	target_name
		What received the value.
	expected
		What it accepts.
	given
		The rejected value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Region(rows=0)
	... except ndp.InvalidTypeError as error:
	... 	print(error)
	Region rows expects an Index, a Range or None, got 0.
	>>> try:
	... 	ndp.Array.from_list([1, 2]).compute(ndp.Sum)
	... except ndp.InvalidTypeError as error:
	... 	print(error)
	ndp.Sum is a class, use ndp.Sum() instead.
	"""

	def __init__(self, target_name: str, expected: str, given: object) -> None:
		"""
		Build the error message from what received the value, what it accepts and the rejected value.

		.. versionadded:: 0.1.0

		Parameters
		----------
		target_name
			What received the value.
		expected
			What it accepts.
		given
			The rejected value.
		"""
		if isinstance(given, type):
			message = CLASS_GIVEN_MESSAGE.format(class_name=given.__name__)
		else:
			message = TYPE_MESSAGE.format(target_name=target_name, expected=expected, given=given)

		super().__init__(message)

		self.target_name = target_name
		self.expected = expected
		self.given = given
