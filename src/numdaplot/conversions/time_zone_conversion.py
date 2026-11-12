"""
Change of the time zone of a datetime column of a Table.

.. versionadded:: 0.1.0
"""

import numpy

from numdaplot.data_types.type import Type
from numdaplot.dates.time_zone_change import TimeZoneChange
from numdaplot.dates.time_zone_mode import TimeZoneMode
from numdaplot.errors.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import find_column_missing
from numdaplot.tables.frames.time_zones import find_column_time_zone

MODE_OPERATIONS = {
	TimeZoneMode.ATTRIBUTE: "Attributing a time zone",
	TimeZoneMode.SHIFT: "Shifting to another time zone",
	TimeZoneMode.REMOVE: "Removing the time zone",
}
# pandas marks with NaT the clock times that do not exist, or exist twice, in the zone.
UNREADABLE_CLOCK_TIME = "NaT"


def change_time_zone(column: Column, change: TimeZoneChange) -> Column:
	"""
	Return a datetime column with its time zone given, changed or removed.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A datetime column.
	change
		The mode of the change, and the new zone for ``ATTRIBUTE`` and ``SHIFT``.

	Returns
	-------
	Column
		The changed column, missing values staying missing.

	Raises
	------
	TimeZoneMismatchError
		When ``ATTRIBUTE`` is asked for datetimes with a zone, or ``SHIFT`` and ``REMOVE`` for datetimes without.
	ValueConversionError
		With ``ATTRIBUTE``, at the first clock time that does not exist in the zone, or exists twice.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.time_zone_conversion import change_time_zone
	>>> times = pandas.Series(pandas.to_datetime(["2026-07-01 10:30"]))
	>>> paris = ndp.TimeZoneChange(mode=ndp.TimeZoneMode.ATTRIBUTE, zone=ndp.TimeZone("Europe/Paris"))
	>>> change_time_zone(times, paris).tolist()
	[Timestamp('2026-07-01 10:30:00+0200', tz='Europe/Paris')]
	"""
	time_zone = find_column_time_zone(column)
	has_zone = time_zone is not None
	expects_zone = change.mode != TimeZoneMode.ATTRIBUTE
	if has_zone != expects_zone:
		operation = MODE_OPERATIONS[change.mode]
		raise TimeZoneMismatchError(operation, expects_zone)

	if change.zone is None:
		naive_column = column.dt.tz_localize(None)
		return naive_column

	if change.mode == TimeZoneMode.SHIFT:
		shifted_column = column.dt.tz_convert(change.zone.name)
		return shifted_column

	attributed_column = attribute_time_zone(column, change.zone.name)

	return attributed_column


def attribute_time_zone(column: Column, zone_name: str) -> Column:
	"""
	Return datetimes without zone given a time zone, their clock time staying the same.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A datetime column without time zone.
	zone_name
		The IANA name of the zone.

	Returns
	-------
	Column
		The datetimes in the zone.

	Raises
	------
	ValueConversionError
		At the first clock time that does not exist in the zone, or exists twice, when the clocks change.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.time_zone_conversion import attribute_time_zone
	>>> try:
	... 	attribute_time_zone(pandas.Series(pandas.to_datetime(["2026-03-29 02:30"])), "Europe/Paris")
	... except ndp.ValueConversionError as error:
	... 	print(error)
	Cannot store the DATETIME value '2026-03-29 02:30:00' as DATETIME without losing information.
	"""
	zone_column = column.dt.tz_localize(zone_name, ambiguous=UNREADABLE_CLOCK_TIME, nonexistent=UNREADABLE_CLOCK_TIME)
	missing = find_column_missing(column)
	unreadable_times = zone_column.isna()
	unreadable = unreadable_times.to_numpy(dtype=numpy.bool_)
	rejected = unreadable & ~missing
	has_rejected = bool(rejected.any())
	if has_rejected:
		rejected_times = column[rejected]
		first_rejected_time = rejected_times.iloc[0]
		rejected_text = str(first_rejected_time)
		raise ValueConversionError(Type.DATETIME.name, Type.DATETIME.name, rejected_text)

	return zone_column
