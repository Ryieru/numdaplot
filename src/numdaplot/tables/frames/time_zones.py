"""
Time zones of the datetime columns of a Table.

.. versionadded:: 0.1.0
"""

from typing import cast

import pandas

from numdaplot.dates.time_zone import TimeZone
from numdaplot.errors.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.errors.unknown_time_zone_error import UnknownTimeZoneError
from numdaplot.errors.unsupported_type_error import UnsupportedTypeError
from numdaplot.tables.frames.column import Column
from numdaplot.types.library import Library
from numdaplot.types.type import Type

UTC_ZONE_NAME = "UTC"
NANOSECOND_UNIT = "ns"
TYPE_AND_ZONE = "{type_name} {zone_name}"
DATETIME_KIND = "M"


def find_column_time_zone(column: Column) -> TimeZone | None:
	"""
	Return the time zone of a Table column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column.

	Returns
	-------
	TimeZone or None
		The zone of a datetime column with a time zone, ``None`` for any other column.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.time_zones import find_column_time_zone
	>>> find_column_time_zone(pandas.Series(pandas.to_datetime(["2026-07-01 10:30"])).dt.tz_localize("Europe/Paris"))
	TimeZone(name='Europe/Paris')
	"""
	column_dtype = column.dtype
	if not isinstance(column_dtype, pandas.DatetimeTZDtype):
		return None

	zone_name = str(column_dtype.tz)
	time_zone = TimeZone(zone_name)

	return time_zone


def name_column_type(column: Column, column_type: Type) -> str:
	"""
	Return the type shown under the name of a Table column, followed by its time zone when it has one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column.
	column_type
		The numdaplot type of the column.

	Returns
	-------
	str
		The name of the type, such as ``"FLOAT64"`` or ``"DATETIME Europe/Paris"``.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.frames.time_zones import name_column_type
	>>> name_column_type(pandas.Series([1.5]), ndp.Type.FLOAT64)
	'FLOAT64'
	"""
	time_zone = find_column_time_zone(column)
	if time_zone is None:
		return column_type.name

	type_and_zone = TYPE_AND_ZONE.format(type_name=column_type.name, zone_name=time_zone.name)

	return type_and_zone


def normalize_time_zone_column(column: Column) -> Column:
	"""
	Return a datetime column with a time zone, counted in nanoseconds, its zone named by its IANA name.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A pandas column of datetimes with a time zone.

	Returns
	-------
	pandas.Series
		The same instants in the same zone.

	Raises
	------
	UnsupportedTypeError
		When the zone is not an IANA time zone, such as a fixed offset of one hour.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.time_zones import normalize_time_zone_column
	>>> times = pandas.Series(pandas.to_datetime(["2026-07-01 10:30"])).dt.tz_localize("UTC").dt.as_unit("s")
	>>> str(normalize_time_zone_column(times).dtype)
	'datetime64[ns, UTC]'
	"""
	column_dtype = cast(pandas.DatetimeTZDtype, column.dtype)
	zone_name = str(column_dtype.tz)
	try:
		TimeZone(zone_name)
	except UnknownTimeZoneError as error:
		dtype_name = str(column_dtype)
		raise UnsupportedTypeError(dtype_name, Library.PANDAS) from error

	nanosecond_column = column.dt.as_unit(NANOSECOND_UNIT)
	named_column = nanosecond_column.dt.tz_convert(zone_name)

	return named_column


def remove_utc_zone(column: Column) -> Column:
	"""
	Return the instants of a datetime column with a time zone as datetimes without zone, in UTC.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column of datetimes with a time zone.

	Returns
	-------
	pandas.Series
		The UTC clock time of each instant, without time zone.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.time_zones import remove_utc_zone
	>>> times = pandas.Series(pandas.to_datetime(["2026-07-01 10:30"])).dt.tz_localize("Europe/Paris")
	>>> remove_utc_zone(times).tolist()
	[Timestamp('2026-07-01 08:30:00')]
	"""
	utc_column = column.dt.tz_convert(UTC_ZONE_NAME)
	naive_column = utc_column.dt.tz_localize(None)

	return naive_column


def attribute_utc_results(column: Column, time_zone: TimeZone) -> Column:
	"""
	Return datetimes computed in UTC without zone as the same instants in a time zone.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column of datetimes without time zone, holding UTC clock times.
	time_zone
		The zone to show the instants in.

	Returns
	-------
	pandas.Series
		The instants in the zone.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.frames.time_zones import attribute_utc_results
	>>> times = pandas.Series(pandas.to_datetime(["2026-07-01 08:30"]))
	>>> attribute_utc_results(times, ndp.TimeZone("Europe/Paris")).tolist()
	[Timestamp('2026-07-01 10:30:00+0200', tz='Europe/Paris')]
	"""
	utc_column = column.dt.tz_localize(UTC_ZONE_NAME)
	zone_column = utc_column.dt.tz_convert(time_zone.name)

	return zone_column


def attribute_source_time_zone(results: Column, source: Column) -> Column:
	"""
	Return statistics of a column in the time zone of that column, when they are datetimes and it has one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	results
		Statistics computed on the UTC clock times of ``source``.
	source
		The column the statistics are computed on.

	Returns
	-------
	pandas.Series
		The datetime results in the zone of the source column, or the results themselves otherwise.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.time_zones import attribute_source_time_zone
	>>> source = pandas.Series(pandas.to_datetime(["2026-07-01 10:30"])).dt.tz_localize("Europe/Paris")
	>>> attribute_source_time_zone(pandas.Series(pandas.to_datetime(["2026-07-01 08:30"])), source).tolist()
	[Timestamp('2026-07-01 10:30:00+0200', tz='Europe/Paris')]
	"""
	time_zone = find_column_time_zone(source)
	if time_zone is None:
		return results

	is_datetime_result = results.dtype.kind == DATETIME_KIND
	if not is_datetime_result:
		return results

	zone_results = attribute_utc_results(results, time_zone)

	return zone_results


def require_no_time_zone(frame: pandas.DataFrame, operation: str) -> None:
	"""
	Check that no column of a Table holds datetimes with a time zone.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	operation
		What needs datetimes without zone, shown in the error message, such as ``"An Excel file"``.

	Raises
	------
	TimeZoneMismatchError
		When a column holds datetimes with a time zone.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.frames.time_zones import require_no_time_zone
	>>> times = pandas.Series(pandas.to_datetime(["2026-07-01 10:30"])).dt.tz_localize("UTC")
	>>> try:
	... 	require_no_time_zone(pandas.DataFrame({"time": times}), "An Excel file")
	... except ndp.TimeZoneMismatchError as error:
	... 	print(error)
	An Excel file needs datetimes without a time zone.
	"""
	for _, column in frame.items():
		time_zone = find_column_time_zone(column)
		if time_zone is not None:
			raise TimeZoneMismatchError(operation, False)
