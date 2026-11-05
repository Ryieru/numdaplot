"""
Error raised when values cannot be stored in a type without losing information, or texts cannot be read as dates.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

VALUE_CONVERSION_MESSAGE = "Cannot store {source_type_name} values as {target_type_name} without losing information."
REJECTED_VALUE_MESSAGE = (
	"Cannot store the {source_type_name} value {rejected_value!r} as {target_type_name} without losing information."
)
UNREADABLE_DATE_MESSAGE = (
	"Cannot read the {source_type_name} value {rejected_value!r} as {target_type_name} with the format "
	"{date_format_name}. Give the format of the column with format=, using DateFormat or CustomDateFormat."
)


class ValueConversionError(NumdaplotError):
	"""
	Raised when values cannot be stored in a type without losing information, or texts cannot be read as dates.

	For example, decimals stored as integers, a text stored as a number, or a text that does not follow the
	date format. When the first rejected value is known, the message shows it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	source_type_name
		Name of the ``ndp.Type`` member of the given values.
	target_type_name
		Name of the ``ndp.Type`` member they should be stored as.
	rejected_value
		The first value that cannot be stored. When omitted, the message names no value.
	date_format_name
		The name or the pattern of the date format a rejected text was read with. When omitted, or without
		``rejected_value``, the message names no format.

	Attributes
	----------
	source_type_name
		Name of the ``ndp.Type`` member of the given values.
	target_type_name
		Name of the ``ndp.Type`` member they should be stored as.
	rejected_value
		The first value that cannot be stored, or ``None`` when it is not known.
	date_format_name
		The name or the pattern of the date format a rejected text was read with, ``None`` for other values.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Array.from_list([1.5, 2.5], dtype=ndp.Type.INT64)
	... except ndp.ValueConversionError as error:
	... 	print(error)
	Cannot store FLOAT64 values as INT64 without losing information.
	>>> days = ndp.Table.from_arrays({"day": ndp.Array.from_list(["31/12/2026"])})
	>>> try:
	... 	days.convert(ndp.Conversion(column="day", dtype=ndp.Type.DATE))
	... except ndp.ValueConversionError as error:
	... 	print(error)
	Cannot read the TEXT value '31/12/2026' as DATE with the format YEAR_MONTH_DAY.
	Give the format of the column with format=, using DateFormat or CustomDateFormat.
	"""

	def __init__(
		self,
		source_type_name: str,
		target_type_name: str,
		rejected_value: object = None,
		date_format_name: str | None = None,
	) -> None:
		"""
		Build the error message from the type names, and the rejected value and the date format when they are known.

		.. versionadded:: 0.1.0

		Parameters
		----------
		source_type_name
			Name of the ``ndp.Type`` member of the given values.
		target_type_name
			Name of the ``ndp.Type`` member they should be stored as.
		rejected_value
			The first value that cannot be stored. When omitted, the message names no value.
		date_format_name
			The name or the pattern of the date format a rejected text was read with. When omitted, or without
			``rejected_value``, the message names no format.
		"""
		message = VALUE_CONVERSION_MESSAGE.format(source_type_name=source_type_name, target_type_name=target_type_name)
		if rejected_value is not None:
			message = REJECTED_VALUE_MESSAGE.format(
				source_type_name=source_type_name,
				target_type_name=target_type_name,
				rejected_value=rejected_value,
			)

		if rejected_value is not None and date_format_name is not None:
			message = UNREADABLE_DATE_MESSAGE.format(
				source_type_name=source_type_name,
				target_type_name=target_type_name,
				rejected_value=rejected_value,
				date_format_name=date_format_name,
			)

		super().__init__(message)

		self.source_type_name = source_type_name
		self.target_type_name = target_type_name
		self.rejected_value = rejected_value
		self.date_format_name = date_format_name
