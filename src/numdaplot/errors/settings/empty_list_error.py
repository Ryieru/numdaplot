"""
Error raised when a setting receives an empty list.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

EMPTY_LIST_MESSAGE = "Expected at least one {item_name}, got an empty list."


class EmptyListError(NumdaplotError):
	"""
	Raised when a setting needs at least one element, such as the conditions of a ``Filter``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	item_name
		What the list holds, such as ``condition``.

	Attributes
	----------
	item_name
		What the list holds, such as ``condition``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Filter(conditions=[])
	... except ndp.EmptyListError as error:
	... 	print(error)
	Expected at least one condition, got an empty list.
	"""

	def __init__(self, item_name: str) -> None:
		"""
		Build the error message from the item name.

		.. versionadded:: 0.1.0

		Parameters
		----------
		item_name
			What the list holds, such as ``condition``.
		"""
		message = EMPTY_LIST_MESSAGE.format(item_name=item_name)
		super().__init__(message)

		self.item_name = item_name
