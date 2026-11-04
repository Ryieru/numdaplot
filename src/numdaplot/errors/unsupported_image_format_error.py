"""
Error raised when an image is saved with an extension numdaplot does not write.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

UNSUPPORTED_IMAGE_FORMAT_MESSAGE = "Cannot save an image as {extension!r}: use .png, .svg or .pdf."


class UnsupportedImageFormatError(NumdaplotError):
	"""
	Raised when the path of an image does not end with ``.png``, ``.svg`` or ``.pdf``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	extension
		The rejected extension, such as ``.jpg``, or an empty text when the path has none.

	Attributes
	----------
	extension
		The rejected extension, such as ``.jpg``, or an empty text when the path has none.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> path = Path(tempfile.mkdtemp()) / "prices.jpg"
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> plot = ndp.plot_line(prices, ndp.LineChart())
	>>> try:
	... 	plot.save(path)
	... except ndp.UnsupportedImageFormatError as error:
	... 	print(error)
	Cannot save an image as '.jpg': use .png, .svg or .pdf.
	"""

	def __init__(self, extension: str) -> None:
		"""
		Build the error message from the rejected extension.

		.. versionadded:: 0.1.0

		Parameters
		----------
		extension
			The rejected extension, such as ``.jpg``, or an empty text when the path has none.
		"""
		message = UNSUPPORTED_IMAGE_FORMAT_MESSAGE.format(extension=extension)
		super().__init__(message)
		self.extension = extension
