"""
Error raised when a setting receives a value of the wrong kind.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

SETTING_TYPE_MESSAGE = "{setting_name} expects {expected}, got {given!r}."
CLASS_GIVEN_MESSAGE = "ndp.{class_name} is a class, use ndp.{class_name}() instead."


class InvalidSettingTypeError(NumdaplotError):
	"""
	Raised when a setting receives a value of the wrong kind, such as a number for the rows of a ``Region``.

	A class given in place of an object, such as ``ndp.Sum`` in place of ``ndp.Sum()``, gets a message naming the
	parentheses.

	.. versionadded:: 0.1.0

	Parameters
	----------
	setting_name
		The setting and what owns it, such as ``"Region rows"``.
	expected
		What the setting accepts, such as ``"an Index, a Range or None"``.
	given
		The rejected value.

	Attributes
	----------
	setting_name
		The setting and what owns it.
	expected
		What the setting accepts.
	given
		The rejected value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Region(rows=0)
	... except ndp.InvalidSettingTypeError as error:
	... 	print(error)
	Region rows expects an Index, a Range or None, got 0.
	>>> try:
	... 	ndp.Array.from_list([1, 2]).compute(ndp.Sum)
	... except ndp.InvalidSettingTypeError as error:
	... 	print(error)
	ndp.Sum is a class, use ndp.Sum() instead.
	"""

	def __init__(self, setting_name: str, expected: str, given: object) -> None:
		"""
		Build the error message from the setting, what it accepts and the rejected value.

		.. versionadded:: 0.1.0

		Parameters
		----------
		setting_name
			The setting and what owns it.
		expected
			What the setting accepts.
		given
			The rejected value.
		"""
		if isinstance(given, type):
			message = CLASS_GIVEN_MESSAGE.format(class_name=given.__name__)
		else:
			message = SETTING_TYPE_MESSAGE.format(setting_name=setting_name, expected=expected, given=given)

		super().__init__(message)

		self.setting_name = setting_name
		self.expected = expected
		self.given = given
