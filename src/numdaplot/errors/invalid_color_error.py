"""
Error raised when a custom color is not written as ``#rrggbb``.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_COLOR_MESSAGE = "Expected a color written as #rrggbb, got {text!r}."


class InvalidColorError(NumdaplotError):
	"""
	Raised when the text of a ``CustomColor`` is not ``#`` followed by six hexadecimal digits.

	.. versionadded:: 0.1.0

	Parameters
	----------
	text
		The rejected text.

	Attributes
	----------
	text
		The rejected text.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.CustomColor("#ff88")
	... except ndp.InvalidColorError as error:
	... 	print(error)
	Expected a color written as #rrggbb, got '#ff88'.
	"""

	def __init__(self, text: str) -> None:
		"""
		Build the error message from the rejected text.

		.. versionadded:: 0.1.0

		Parameters
		----------
		text
			The rejected text.
		"""
		message = INVALID_COLOR_MESSAGE.format(text=text)
		super().__init__(message)
		self.text = text
