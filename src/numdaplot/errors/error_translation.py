"""
Base class of the blocks that replace or complete the errors raised inside them.

.. versionadded:: 0.2.0
"""

from types import TracebackType

MISSING_TRANSLATION = "Each block translating errors says how it translates them."


class ErrorTranslation:
	"""
	Base class of the blocks that replace or complete the errors raised inside them, used with ``with``.

	Nothing happens when the block starts. When it ends with an error, ``translate_error`` raises the error of
	numdaplot standing for it, or returns to let the error go on, completed or unchanged.

	.. versionadded:: 0.2.0

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.frames.named_column_errors import NamedColumnErrors
	>>> try:
	... 	with NamedColumnErrors(pandas.Series([1.0], name="price")):
	... 		raise ndp.IncompatibleTypesError("Contains", ["FLOAT64"])
	... except ndp.IncompatibleTypesError as error:
	... 	print(error)
	Cannot apply Contains to the FLOAT64 column 'price'.
	"""

	def __enter__(self) -> None:
		"""
		Start the block.

		.. versionadded:: 0.2.0
		"""

	def __exit__(
		self,
		error_type: type[BaseException] | None,
		error: BaseException | None,
		traceback: TracebackType | None,
	) -> None:
		"""
		Hand the error of the block to ``translate_error``, a block without error ending as it is.

		.. versionadded:: 0.2.0

		Parameters
		----------
		error_type
			The type of the error raised by the block, or None.
		error
			The error raised by the block, or None.
		traceback
			Its traceback, or None.
		"""
		if error is None:
			return

		self.translate_error(error)

	def translate_error(self, error: BaseException) -> None:
		"""
		Raise the error of numdaplot standing for an error of the block, or return to let it go on.

		.. versionadded:: 0.2.0

		Parameters
		----------
		error
			The error raised by the block.

		Raises
		------
		NotImplementedError
			Always, for this base class, which translates no error.
		"""
		raise NotImplementedError(MISSING_TRANSLATION)
