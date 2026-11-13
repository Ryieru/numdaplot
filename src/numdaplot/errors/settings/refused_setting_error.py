"""
Error raised when a setting is given to an object that does not accept it.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

REFUSED_SETTING_MESSAGE = "{owner_name} does not accept {setting_name}."


class RefusedSettingError(NumdaplotError):
	"""
	Raised when a setting is given to an object that does not accept it.

	For example, a ``ScatterChart`` always draws a marker, and only PNG images have a resolution.

	.. versionadded:: 0.1.0

	Parameters
	----------
	setting_name
		The refused setting, such as ``MarkerShape.NONE``.
	owner_name
		What refuses it, such as ``ScatterChart``.

	Attributes
	----------
	setting_name
		The refused setting, such as ``MarkerShape.NONE``.
	owner_name
		What refuses it, such as ``ScatterChart``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.ScatterChart(x="surface", y="price", marker=ndp.MarkerShape.NONE)
	... except ndp.RefusedSettingError as error:
	... 	print(error)
	ScatterChart does not accept MarkerShape.NONE.
	"""

	def __init__(self, setting_name: str, owner_name: str) -> None:
		"""
		Build the error message from the setting and what refuses it.

		.. versionadded:: 0.1.0

		Parameters
		----------
		setting_name
			The refused setting, such as ``MarkerShape.NONE``.
		owner_name
			What refuses it, such as ``ScatterChart``.
		"""
		message = REFUSED_SETTING_MESSAGE.format(setting_name=setting_name, owner_name=owner_name)
		super().__init__(message)
		self.setting_name = setting_name
		self.owner_name = owner_name
