"""
A pattern describing how dates are written as texts.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.invalid_date_format_error import InvalidDateFormatError
from numdaplot.settings.field_types import require_field_types

DATE_CODES = ("%d", "%m", "%Y", "%y", "%b", "%B", "%j")
TIME_ZONE_CODES = ("%z", "%Z")
TIME_CODES = ("%H", "%I", "%M", "%S", "%f", "%p")


@dataclass(frozen=True)
class CustomDateFormat:
	"""
	A pattern describing how dates are written as texts, used by ``Conversion`` when no ``DateFormat`` fits.

	The pattern uses the codes of Python ``datetime.strptime``: ``%d`` day, ``%m`` month, ``%Y`` year,
	``%b`` short month name, ``%B`` full month name, ``%H`` hour, ``%M`` minute, ``%S`` second.
	Month names are in English.

	.. versionadded:: 0.1.0

	Parameters
	----------
	pattern
		The pattern, such as ``"%d %b %Y"`` for ``"31 Dec 2026"``.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidDateFormatError
		When the pattern has no day, month or year code, or has a time zone code (``%z``, ``%Z``).

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Table.from_arrays({"day": ndp.Array.from_list(["31 Dec 2026", "1 Feb 2026"])})
	>>> days.convert(ndp.Conversion(column="day", dtype=ndp.Type.DATE, format=ndp.CustomDateFormat("%d %b %Y")))
	         day
	        DATE
	0 2026-12-31
	1 2026-02-01
	"""

	pattern: str

	def __post_init__(self) -> None:
		"""
		Check that the pattern reads a date and no time zone.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidDateFormatError
			When the pattern has no day, month or year code, or has a time zone code.
		"""
		require_field_types(self)

		has_date_code = any(date_code in self.pattern for date_code in DATE_CODES)
		has_time_zone_code = any(zone_code in self.pattern for zone_code in TIME_ZONE_CODES)
		is_rejected = has_time_zone_code or not has_date_code
		if is_rejected:
			raise InvalidDateFormatError(self.pattern)
