"""
Error raised when two settings that exclude each other are both given.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

CONFLICTING_SETTINGS_MESSAGE = "{first_name} and {second_name} cannot be given together."


class ConflictingSettingsError(NumdaplotError):
	"""
	Raised when two settings that exclude each other are both given.

	For example, a ``ScatterChart`` colors its points with one ``color`` or by the values of ``color_by``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	first_name
		Name of the first setting.
	second_name
		Name of the second setting.

	Attributes
	----------
	first_name
		Name of the first setting.
	second_name
		Name of the second setting.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.ScatterChart(x="surface", y="price", color=ndp.Color.RED, color_by="city")
	... except ndp.ConflictingSettingsError as error:
	... 	print(error)
	color and color_by cannot be given together.
	"""

	def __init__(self, first_name: str, second_name: str) -> None:
		"""
		Build the error message from the two setting names.

		.. versionadded:: 0.1.0

		Parameters
		----------
		first_name
			Name of the first setting.
		second_name
			Name of the second setting.
		"""
		message = CONFLICTING_SETTINGS_MESSAGE.format(first_name=first_name, second_name=second_name)
		super().__init__(message)
		self.first_name = first_name
		self.second_name = second_name
