"""
A new type for columns of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.conversions.boolean_rule import BooleanRule
from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.dates.date_format import DateFormat
from numdaplot.dates.time_zone_change import TimeZoneChange
from numdaplot.tables.columns.brackets import Brackets
from numdaplot.tables.columns.column_names import copy_column_names
from numdaplot.types.type import Type


@dataclass(frozen=True)
class TableConversion:
	"""
	A new type for columns of a Table, used by ``Table.convert``.

	Every listed column takes the same type and settings.

	Accepted conversions: between number types, between numbers and booleans, from numbers, booleans,
	categories, dates, datetimes, durations and times of day to texts, from texts and categories to numbers,
	booleans, dates, datetimes or times of day, from any type but categories to categories, between dates and
	datetimes, and from datetimes to times of day, the local time for a datetime with a time zone. A time zone change
	keeps the type ``DATETIME``: give it alone, in a conversion of a datetime column to ``DATETIME``.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Renamed from ``Conversion``. Takes ``columns``, a list, in place of ``column``.

	Parameters
	----------
	columns
		The names of the columns, at least one, each once. The conversion keeps its own copy of the list.
	dtype
		Its new type.
	format
		How dates are written as texts, when texts are read as dates or datetimes, or dates or datetimes are
		written as texts. When omitted, texts are read as year, month and day. For ``DATETIME``, each text may
		also have a time after a space or a ``"T"``, and a text without time counts as midnight. A format that is
		given applies to every text: ``DateFormat.YEAR_MONTH_DAY_TIME`` refuses a text without time. When omitted,
		dates are written as year, month and day separated by ``"-"``, with the time for datetimes. Times of day
		take a ``CustomDateFormat`` of a time only, such as ``"%H%M"``: when omitted, texts are read as ``HH:MM``,
		``HH:MM:SS`` or ``HH:MM:SS.ffffff``, and times are written as ``15:35:00``. For a conversion of numbers to
		``CATEGORY``, ``Brackets`` cut the numbers into ordered categories, such as ages into ``0 to 9``.
	timezone
		A change of the time zone of a datetime column, the time zone unchanged when omitted.
	booleans
		How numbers are read as booleans, only when numbers are converted to ``BOOL``. When omitted, ``ZERO_ONE``:
		0 gives ``False``, 1 gives ``True``, and any other number raises ``ValueConversionError``.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	EmptyListError
		When ``columns`` is an empty list.
	InvalidColumnNameError
		When a column name is an empty text.
	DuplicateColumnError
		When a column name appears twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> codes = ndp.Table.from_arrays({"zip_code": ndp.Array.from_list(["06000", "75001"])})
	>>> codes.convert(ndp.TableConversion(columns=["zip_code"], dtype=ndp.Type.INT32))
	  zip_code
	     INT32
	0     6000
	1    75001
	>>> days = ndp.Table.from_arrays({"day": ndp.Array.from_list(["31/12/2026"])})
	>>> days.convert(ndp.TableConversion(columns=["day"], dtype=ndp.Type.DATE, format=ndp.DateFormat.DAY_MONTH_YEAR))
	         day
	        DATE
	0 2026-12-31
	>>> pickups = ndp.Table.from_arrays({"pickup": ndp.Array.from_list(["2026-12-31 20:21:09", "2026-12-31"])})
	>>> pickups.convert(ndp.TableConversion(columns=["pickup"], dtype=ndp.Type.DATETIME))
	               pickup
	             DATETIME
	0 2026-12-31 20:21:09
	1 2026-12-31 00:00:00
	"""

	columns: list[str]
	dtype: Type
	format: DateFormat | CustomDateFormat | Brackets | None = None
	timezone: TimeZoneChange | None = None
	booleans: BooleanRule | None = None

	def __post_init__(self) -> None:
		"""
		Check the columns and replace them with a copy that only the conversion holds.

		.. versionadded:: 0.1.0
		.. versionchanged:: 0.2.0
			Checks ``columns``, a list, in place of ``column``.

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		EmptyListError
			When ``columns`` is an empty list.
		InvalidColumnNameError
			When a column name is an empty text.
		DuplicateColumnError
			When a column name appears twice.
		"""
		require_field_types(self)

		columns_copy = copy_column_names(self.columns)
		object.__setattr__(self, "columns", columns_copy)
