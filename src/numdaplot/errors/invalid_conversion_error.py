"""
Error raised when a setting of a conversion does not apply to it.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_CONVERSION_MESSAGE = (
	"The setting {setting_name} does not apply to a conversion from {source_type_name} to {target_type_name}."
)
DATE_FORMAT_ON_TIME_MESSAGE = (
	"The format {date_format_name} has a date, which TIME cannot hold. Give a CustomDateFormat of a time only, "
	'such as "%H:%M".'
)
TIME_TYPE_NAME = "TIME"
TIME_FORMAT_ON_DATE_MESSAGE = (
	"The format {date_format_name} has a time, which DATE cannot hold. "
	"Convert the column to DATETIME first, then to {target_type_name}."
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
	date_format_name
		The name or the pattern of a format with a time, when dates are read or written with it. When omitted, the
		message names the setting and the types.

	Attributes
	----------
	setting_name
		Name of the setting.
	source_type_name
		Name of the ``ndp.Type`` member of the column.
	target_type_name
		Name of the ``ndp.Type`` member it is converted to.
	date_format_name
		The name or the pattern of a format with a time used on dates, ``None`` for other conversions.

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
	>>> days = ndp.Table.from_arrays({"day": ndp.Array.from_list(["31/12/2026 14:30"])})
	>>> day_and_time = ndp.DateFormat.DAY_MONTH_YEAR_TIME
	>>> try:
	... 	days.convert(ndp.Conversion(column="day", dtype=ndp.Type.DATE, format=day_and_time))
	... except ndp.InvalidConversionError as error:
	... 	print(error)
	The format DAY_MONTH_YEAR_TIME has a time, which DATE cannot hold.
	Convert the column to DATETIME first, then to DATE.
	"""

	def __init__(
		self,
		setting_name: str,
		source_type_name: str,
		target_type_name: str,
		date_format_name: str | None = None,
	) -> None:
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
		date_format_name
			The name or the pattern of a format with a time, when dates are read or written with it, or of a format with
			a date, when times of day are read or written with it. When omitted, the message names the setting and the
			types.
		"""
		message = INVALID_CONVERSION_MESSAGE.format(
			setting_name=setting_name,
			source_type_name=source_type_name,
			target_type_name=target_type_name,
		)
		converts_times = TIME_TYPE_NAME in (source_type_name, target_type_name)
		if date_format_name is not None and converts_times:
			message = DATE_FORMAT_ON_TIME_MESSAGE.format(date_format_name=date_format_name)

		if date_format_name is not None and not converts_times:
			message = TIME_FORMAT_ON_DATE_MESSAGE.format(
				date_format_name=date_format_name,
				target_type_name=target_type_name,
			)

		super().__init__(message)
		self.setting_name = setting_name
		self.source_type_name = source_type_name
		self.target_type_name = target_type_name
		self.date_format_name = date_format_name
