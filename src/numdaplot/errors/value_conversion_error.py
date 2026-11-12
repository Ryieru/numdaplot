"""
Error raised when values cannot be stored in a type without losing information, or texts cannot be read as dates.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.rejected_dates import RejectedDate, RejectedDatePart

VALUE_CONVERSION_MESSAGE = (
	"Cannot store {source_type_name} values{column_text} as {target_type_name} without losing information."
)
REJECTED_VALUE_MESSAGE = (
	"Cannot store the {source_type_name} value {rejected_value!r}{column_text} as {target_type_name} "
	"without losing information."
)
UNREADABLE_DATE_MESSAGE = (
	"Cannot read the {source_type_name} value {rejected_value!r}{column_text} as {target_type_name} with the format "
	"{date_format_name}. Give the format of the values with format=, using DateFormat or CustomDateFormat."
)
NOT_WHOLE_PART_MESSAGE = (
	"Cannot use the {source_type_name} value {rejected_value.value!r} as a {rejected_value.part_name}: "
	"date parts must be whole numbers."
)
IMPOSSIBLE_DATE_MESSAGE = (
	"Cannot build a {target_type_name} from the year {rejected_value.year}, the month {rejected_value.month} and the "
	"day {rejected_value.day}."
)
UNREADABLE_TIME_MESSAGE = (
	"Cannot read the {source_type_name} value {rejected_value!r}{column_text} as {target_type_name} with the format "
	"{date_format_name}. Give the format of the values with format=, using a CustomDateFormat of a time only."
)
TIME_TYPE_NAME = "TIME"
COLUMN_TEXT = " of the column {column_name!r}"
NO_COLUMN_TEXT = ""


class ValueConversionError(NumdaplotError):
	"""
	Raised when values cannot be stored in a type without losing information, or texts cannot be read as dates.

	For example, decimals stored as integers, a text stored as a number, a text that does not follow the date
	format, or date parts that form no date. When the first rejected value is known, the message shows it.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		The advice to give a format speaks of the values, for an Array as for a column.

	Parameters
	----------
	source_type_name
		Name of the ``ndp.Type`` member of the given values.
	target_type_name
		Name of the ``ndp.Type`` member they should be stored as, or ``JSON`` for a value JSON cannot write.
	rejected_value
		The first value that cannot be stored. When omitted, the message names no value. A ``RejectedDatePart`` or
		a ``RejectedDate``, with the year, the month and the day, names the date parts that form no date.
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
	column_name
		Name of the Table column holding the values, or ``None`` for values given to an Array.

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
	... 	days.convert(ndp.TableConversion(columns=["day"], dtype=ndp.Type.DATE))
	... except ndp.ValueConversionError as error:
	... 	print(error)
	Cannot read the TEXT value '31/12/2026' of the column 'day' as DATE with the format YEAR_MONTH_DAY.
	Give the format of the values with format=, using DateFormat or CustomDateFormat.
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
		self.source_type_name = source_type_name
		self.target_type_name = target_type_name
		self.rejected_value = rejected_value
		self.date_format_name = date_format_name
		self.column_name: str | None = None
		message = self.write_message(NO_COLUMN_TEXT)
		super().__init__(message)

	def write_message(self, column_text: str) -> str:
		"""
		Return the message, with the rejected value and the date format when they are known.

		.. versionadded:: 0.1.0

		Parameters
		----------
		column_text
			The words naming the column after the values, or an empty text.

		Returns
		-------
		str
			The message.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.ValueConversionError("FLOAT64", "INT64").write_message("")
		'Cannot store FLOAT64 values as INT64 without losing information.'
		"""
		message_format = self.choose_message_format()
		message = message_format.format(
			source_type_name=self.source_type_name,
			target_type_name=self.target_type_name,
			rejected_value=self.rejected_value,
			date_format_name=self.date_format_name,
			column_text=column_text,
		)

		return message

	def choose_message_format(self) -> str:
		"""
		Return the message format fitting what is known of the rejected value.

		.. versionadded:: 0.1.0

		Returns
		-------
		str
			The format for date parts, a text read with a date format, a known value, or values in general.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> from numdaplot.errors.rejected_dates import RejectedDate
		>>> print(ndp.ValueConversionError("INT64", "DATE", RejectedDate(2025, 2, 31)))
		Cannot build a DATE from the year 2025, the month 2 and the day 31.
		"""
		if isinstance(self.rejected_value, RejectedDatePart):
			return NOT_WHOLE_PART_MESSAGE

		if isinstance(self.rejected_value, RejectedDate):
			return IMPOSSIBLE_DATE_MESSAGE

		if self.rejected_value is None:
			return VALUE_CONVERSION_MESSAGE

		if self.date_format_name is None:
			return REJECTED_VALUE_MESSAGE

		if self.target_type_name == TIME_TYPE_NAME:
			return UNREADABLE_TIME_MESSAGE

		return UNREADABLE_DATE_MESSAGE

	def name_column(self, column_name: str) -> None:
		"""
		Name the Table column holding the values in the message, unless a column is already named.

		.. versionadded:: 0.1.0

		Parameters
		----------
		column_name
			The name of the column.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> error = ndp.ValueConversionError("TEXT", "FLOAT64", "abc")
		>>> error.name_column("payment")
		>>> print(error)
		Cannot store the TEXT value 'abc' of the column 'payment' as FLOAT64 without losing information.
		"""
		if self.column_name is not None:
			return

		self.column_name = column_name
		column_text = COLUMN_TEXT.format(column_name=column_name)
		message = self.write_message(column_text)
		self.args = (message,)
