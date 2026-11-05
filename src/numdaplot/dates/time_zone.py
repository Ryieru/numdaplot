"""
A time zone of the IANA database.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from numdaplot.errors.unknown_time_zone_error import UnknownTimeZoneError


@dataclass(frozen=True)
class TimeZone:
	"""
	A time zone of the IANA database, such as ``"Europe/Paris"`` or ``"UTC"``, used by ``TimeZoneChange``.

	A zone follows the summer and winter time changes of its place. Fixed offsets such as ``"+01:00"``
	are not time zones.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		The IANA name of the zone.

	Raises
	------
	UnknownTimeZoneError
		When the name is not a known IANA name.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Table.from_arrays({"time": ndp.Array.from_list([datetime(2026, 7, 1, 10, 30)])})
	>>> paris = ndp.TimeZone("Europe/Paris")
	>>> in_paris = ndp.TimeZoneChange(mode=ndp.TimeZoneMode.ATTRIBUTE, zone=paris)
	>>> paris_times = times.convert(ndp.Conversion(column="time", dtype=ndp.Type.DATETIME, timezone=in_paris))
	>>> paris_times.column_time_zones
	{'time': TimeZone(name='Europe/Paris')}
	"""

	name: str

	def __post_init__(self) -> None:
		"""
		Check that the name is a known IANA name.

		.. versionadded:: 0.1.0

		Raises
		------
		UnknownTimeZoneError
			When the name is not a known IANA name.
		"""
		try:
			ZoneInfo(self.name)
		except (ZoneInfoNotFoundError, ValueError) as error:
			raise UnknownTimeZoneError(self.name) from error
