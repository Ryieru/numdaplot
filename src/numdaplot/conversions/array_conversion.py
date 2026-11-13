"""
A new type for the values of an Array.

.. versionadded:: 0.2.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.conversions.boolean_rule import BooleanRule
from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.dates.date_format import DateFormat
from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.types.type import Type

ARRAY_CONVERSION_NAME = "ArrayConversion"
CATEGORY_SETTING_NAME = "Type.CATEGORY"


@dataclass(frozen=True)
class ArrayConversion:
	"""
	A new type for the values of an Array, used by ``Array.convert``.

	Accepted conversions: between number types, between numbers and booleans, from numbers, booleans, dates,
	datetimes, durations and times of day to texts, from texts to numbers, booleans, dates, datetimes or times of day,
	between dates and datetimes, and from datetimes to times of day. ``CATEGORY`` is refused: an Array holds the
	values of a category column as texts.

	.. versionadded:: 0.2.0

	Parameters
	----------
	dtype
		The new type of the values, any type but ``CATEGORY``.
	format
		How dates are written as texts, when texts are read as dates or datetimes, or dates or datetimes are
		written as texts. When omitted, texts are read as year, month and day. For ``DATETIME``, each text may
		also have a time after a space or a ``"T"``, and a text without time counts as midnight. A format that is
		given applies to every text: ``DateFormat.YEAR_MONTH_DAY_TIME`` refuses a text without time. When omitted,
		dates are written as year, month and day separated by ``"-"``, with the time for datetimes. Times of day
		take a ``CustomDateFormat`` of a time only, such as ``"%H%M"``: when omitted, texts are read as ``HH:MM``,
		``HH:MM:SS`` or ``HH:MM:SS.ffffff``, and times are written as ``15:35:00``.
	booleans
		How numbers are read as booleans, only when numbers are converted to ``BOOL``. When omitted, ``ZERO_ONE``:
		0 gives ``False``, 1 gives ``True``, and any other number raises ``ValueConversionError``.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names, such as ``Brackets`` as format.
	RefusedSettingError
		When ``dtype`` is ``CATEGORY``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> zip_codes = ndp.Array.from_list(["06000", "75001"])
	>>> zip_codes.convert(ndp.ArrayConversion(dtype=ndp.Type.INT32))
	Array([ 6000, 75001], dtype=INT32)
	>>> days = ndp.Array.from_list(["31/12/2026"])
	>>> days.convert(ndp.ArrayConversion(dtype=ndp.Type.DATE, format=ndp.DateFormat.DAY_MONTH_YEAR))
	Array(['2026-12-31'], dtype=DATE)
	"""

	dtype: Type
	format: DateFormat | CustomDateFormat | None = None
	booleans: BooleanRule | None = None

	def __post_init__(self) -> None:
		"""
		Check the type of every setting, and refuse the type ``CATEGORY``.

		.. versionadded:: 0.2.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		RefusedSettingError
			When ``dtype`` is ``CATEGORY``.
		"""
		require_field_types(self)
		if self.dtype == Type.CATEGORY:
			raise RefusedSettingError(CATEGORY_SETTING_NAME, ARRAY_CONVERSION_NAME)
