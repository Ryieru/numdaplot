"""
A change of the time zone of a datetime column.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.dates.time_zone import TimeZone
from numdaplot.dates.time_zone_mode import TimeZoneMode
from numdaplot.errors.dates.invalid_time_zone_change_error import InvalidTimeZoneChangeError


@dataclass(frozen=True)
class TimeZoneChange:
	"""
	A change of the time zone of a datetime column, used by ``TableConversion``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	mode
		Whether a zone is given to datetimes without one, datetimes are moved to another zone, or their zone
		is removed.
	zone
		The new zone, needed by ``TimeZoneMode.ATTRIBUTE`` and ``SHIFT``. ``REMOVE`` refuses it, so it is the only mode
		used when omitted.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidTimeZoneChangeError
		When ``ATTRIBUTE`` or ``SHIFT`` has no zone, or ``REMOVE`` has one.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Table.from_arrays({"time": ndp.Array.from_list([datetime(2026, 7, 1, 10, 30)])})
	>>> paris = ndp.TimeZoneChange(mode=ndp.TimeZoneMode.ATTRIBUTE, zone=ndp.TimeZone("Europe/Paris"))
	>>> times.convert(ndp.TableConversion(columns=["time"], dtype=ndp.Type.DATETIME, timezone=paris))
	                       time
	      DATETIME Europe/Paris
	0 2026-07-01 10:30:00+02:00
	"""

	mode: TimeZoneMode
	zone: TimeZone | None = None

	def __post_init__(self) -> None:
		"""
		Check that the zone is given exactly when the mode needs it.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidTimeZoneChangeError
			When ``ATTRIBUTE`` or ``SHIFT`` has no zone, or ``REMOVE`` has one.
		"""
		require_field_types(self)

		needs_zone = self.mode != TimeZoneMode.REMOVE
		has_zone = self.zone is not None
		if needs_zone != has_zone:
			raise InvalidTimeZoneChangeError(self.mode.name, needs_zone)
