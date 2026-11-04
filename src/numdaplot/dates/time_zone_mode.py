"""
How the time zone of a datetime column changes.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class TimeZoneMode(Enum):
	"""
	How the time zone of a datetime column changes, used by ``TimeZoneChange``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Table.from_arrays({"time": ndp.Array.from_list([datetime(2026, 7, 1, 10, 30)])})
	>>> paris = ndp.TimeZoneChange(mode=ndp.TimeZoneMode.ATTRIBUTE, zone=ndp.TimeZone("Europe/Paris"))
	>>> times.convert(ndp.Conversion(column="time", dtype=ndp.Type.DATETIME, timezone=paris))
	time
	DATETIME Europe/Paris
	0 2026-07-01 10:30:00+02:00
	"""

	ATTRIBUTE = auto()
	"""
	Gives a zone to datetimes without one: the clock time stays the same.

	A time that does not exist in the zone, or exists twice when the clocks change, raises
	``ValueConversionError``.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Table.from_arrays({"time": ndp.Array.from_list([datetime(2026, 7, 1, 10, 30)])})
	>>> paris = ndp.TimeZoneChange(mode=ndp.TimeZoneMode.ATTRIBUTE, zone=ndp.TimeZone("Europe/Paris"))
	>>> times.convert(ndp.Conversion(column="time", dtype=ndp.Type.DATETIME, timezone=paris))
	time
	DATETIME Europe/Paris
	0 2026-07-01 10:30:00+02:00
	"""

	SHIFT = auto()
	"""
	Moves datetimes with a zone to another zone: the instant stays the same, the clock time changes.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Table.from_arrays({"time": ndp.Array.from_list([datetime(2026, 7, 1, 10, 30)])})
	>>> utc = ndp.TimeZoneChange(mode=ndp.TimeZoneMode.ATTRIBUTE, zone=ndp.TimeZone("UTC"))
	>>> utc_times = times.convert(ndp.Conversion(column="time", dtype=ndp.Type.DATETIME, timezone=utc))
	>>> paris = ndp.TimeZoneChange(mode=ndp.TimeZoneMode.SHIFT, zone=ndp.TimeZone("Europe/Paris"))
	>>> utc_times.convert(ndp.Conversion(column="time", dtype=ndp.Type.DATETIME, timezone=paris))
	time
	DATETIME Europe/Paris
	0 2026-07-01 12:30:00+02:00
	"""

	REMOVE = auto()
	"""
	Removes the zone of datetimes: the clock time stays the same.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Table.from_arrays({"time": ndp.Array.from_list([datetime(2026, 7, 1, 10, 30)])})
	>>> paris = ndp.TimeZoneChange(mode=ndp.TimeZoneMode.ATTRIBUTE, zone=ndp.TimeZone("Europe/Paris"))
	>>> paris_times = times.convert(ndp.Conversion(column="time", dtype=ndp.Type.DATETIME, timezone=paris))
	>>> no_zone = ndp.TimeZoneChange(mode=ndp.TimeZoneMode.REMOVE)
	>>> paris_times.convert(ndp.Conversion(column="time", dtype=ndp.Type.DATETIME, timezone=no_zone))
	time
	DATETIME
	0 2026-07-01 10:30:00
	"""
