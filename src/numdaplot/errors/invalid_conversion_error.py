"""
Error raised when a setting of a conversion does not apply to it.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_CONVERSION_MESSAGE = (
	"The setting {setting_name} does not apply to a conversion from {source_type_name} to {target_type_name}."
)


class InvalidConversionError(NumdaplotError):
	"""
	Raised when a setting of a ``Conversion`` does not apply to the types it converts.

	For example, a date format given to a conversion between numbers, a format with a time given to
	a ``DATE`` column, or a time zone change given to a conversion from texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	setting_name
		Name of the setting, such as ``"format"``.
	source_type_name
		Name of the ``ndp.Type`` member of the column.
	target_type_name
		Name of the ``ndp.Type`` member it is converted to.

	Attributes
	----------
	setting_name
		Name of the setting.
	source_type_name
		Name of the ``ndp.Type`` member of the column.
	target_type_name
		Name of the ``ndp.Type`` member it is converted to.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Table.from_arrays({"price": ndp.Array.from_list([12.5])})
	>>> day_first = ndp.DateFormat.DAY_MONTH_YEAR
	>>> try:
	... 	prices.convert(ndp.Conversion(column="price", dtype=ndp.Type.TEXT, format=day_first))
	... except ndp.InvalidConversionError as error:
	... 	print(error)
	The setting format does not apply to a conversion from FLOAT64 to TEXT.
	"""

	def __init__(self, setting_name: str, source_type_name: str, target_type_name: str) -> None:
		"""
		Build the error message from the setting and the types of the conversion.

		.. versionadded:: 0.1.0

		Parameters
		----------
		setting_name
			Name of the setting.
		source_type_name
			Name of the ``ndp.Type`` member of the column.
		target_type_name
			Name of the ``ndp.Type`` member it is converted to.
		"""
		message = INVALID_CONVERSION_MESSAGE.format(
			setting_name=setting_name,
			source_type_name=source_type_name,
			target_type_name=target_type_name,
		)
		super().__init__(message)
		self.setting_name = setting_name
		self.source_type_name = source_type_name
		self.target_type_name = target_type_name
