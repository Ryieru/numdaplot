"""
Reading of the Table columns a chart draws.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.data_types.time_of_day import read_times
from numdaplot.data_types.value_family import ValueFamily, find_family
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.plots.data.position_kind import PositionKind
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import find_column_missing, find_column_type
from numdaplot.tables.frames.named_column_errors import NamedColumnErrors
from numdaplot.tables.frames.time_zones import find_column_time_zone

POSITION_KINDS = {
	ValueFamily.NUMBER: PositionKind.NUMBERS,
	ValueFamily.MOMENT: PositionKind.MOMENTS,
	ValueFamily.TEXT: PositionKind.TEXTS,
	ValueFamily.BOOL: PositionKind.TEXTS,
	ValueFamily.TIME: PositionKind.TIMES,
}
NUMBER_FAMILIES = frozenset({ValueFamily.NUMBER})
LABEL_FAMILIES = frozenset({ValueFamily.TEXT, ValueFamily.BOOL, ValueFamily.TIME})
HOUR_LABEL_PATTERN = "%H:%M"
MICROSECONDS_PER_HOUR = 3_600_000_000
TIME_DTYPE = numpy.dtype("timedelta64[us]")
MOMENT_DTYPE = numpy.dtype("datetime64[ns]")
TEXT_DTYPE = "string"
PYTHON_OBJECT_DTYPE = numpy.dtype(object)


def require_column_family(column: Column, accepted_families: frozenset[ValueFamily], chart_name: str) -> ValueFamily:
	"""
	Check that a column holds values a chart draws, and return their family.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column.
	accepted_families
		The families the chart draws in this column.
	chart_name
		Name of the chart class, shown in the error message.

	Returns
	-------
	ValueFamily
		The family of the column.

	Raises
	------
	IncompatibleTypesError
		When the column holds values of another family, such as durations.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.column_reading import NUMBER_FAMILIES, require_column_family
	>>> try:
	... 	require_column_family(pandas.Series([True], dtype="boolean"), NUMBER_FAMILIES, "LineChart")
	... except ndp.IncompatibleTypesError as error:
	... 	print(error)
	Cannot apply LineChart to BOOL.
	"""
	column_type = find_column_type(column)
	family = find_family(column_type)
	if family not in accepted_families:
		with NamedColumnErrors(column):
			raise IncompatibleTypesError(chart_name, [column_type.name])

	return family


def read_numbers(column: Column, chart_name: str) -> NDArray[numpy.float64]:
	"""
	Return a column of numbers as float64 values, NaN where a value is missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column.
	chart_name
		Name of the chart class, shown in the error message.

	Returns
	-------
	NDArray[numpy.float64]
		One number per row.

	Raises
	------
	IncompatibleTypesError
		When the column does not hold numbers.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.plots.data.column_reading import read_numbers
	>>> read_numbers(pandas.Series([3, None], dtype="Int64"), "LineChart")
	array([ 3., nan])
	"""
	require_column_family(column, NUMBER_FAMILIES, chart_name)
	numbers = column.to_numpy(dtype=numpy.float64, na_value=numpy.nan)

	return numbers


def read_texts(column: Column, chart_name: str) -> NDArray[Any]:
	"""
	Return a column of texts, categories, booleans or times of day as Python texts, None where a value is missing.

	A time of day is written ``HH:MM``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column.
	chart_name
		Name of the chart class, shown in the error message.

	Returns
	-------
	NDArray
		One text per row, in a numpy array of Python objects.

	Raises
	------
	IncompatibleTypesError
		When the column does not hold texts.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.plots.data.column_reading import read_texts
	>>> read_texts(pandas.Series(["Paris", None], dtype="string"), "BarChart")
	array(['Paris', None], dtype=object)
	"""
	family = require_column_family(column, LABEL_FAMILIES, chart_name)
	if family == ValueFamily.TIME:
		hour_texts = write_hour_labels(column)
		return hour_texts

	text_column = column.astype(TEXT_DTYPE)
	text_values = text_column.tolist()
	missing = find_column_missing(column)
	value_pairs = zip(text_values, missing, strict=True)
	present_texts = [None if is_missing else text for text, is_missing in value_pairs]
	texts = numpy.array(present_texts, dtype=PYTHON_OBJECT_DTYPE)

	return texts


def read_moments(column: Column) -> NDArray[numpy.datetime64]:
	"""
	Return a column of dates or datetimes as the clock times shown in its time zone, NaT where a value is missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A date or datetime column.

	Returns
	-------
	NDArray[numpy.datetime64]
		One datetime64[ns] value per row, without time zone.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.plots.data.column_reading import read_moments
	>>> utc_times = pandas.Series(pandas.to_datetime(["2026-07-01 10:30"])).dt.tz_localize("UTC")
	>>> read_moments(utc_times.dt.tz_convert("Europe/Paris"))
	array(['2026-07-01T12:30:00.000000000'], dtype='datetime64[ns]')
	"""
	clock_times = column
	time_zone = find_column_time_zone(column)
	if time_zone is not None:
		clock_times = column.dt.tz_localize(None)

	moments = clock_times.to_numpy(dtype=MOMENT_DTYPE)

	return moments


def read_positions(column: Column, chart_name: str) -> tuple[PositionKind, NDArray[Any]]:
	"""
	Return the ``x`` values of a chart read from a column, with their kind.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column of numbers, dates, datetimes or texts.
	chart_name
		Name of the chart class, shown in the error message.

	Returns
	-------
	tuple[PositionKind, NDArray]
		The kind and the values, read by ``read_numbers``, ``read_moments`` or ``read_texts``.

	Raises
	------
	IncompatibleTypesError
		When the column holds durations.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.plots.data.column_reading import read_positions
	>>> read_positions(pandas.Series(["Paris"], dtype="string"), "BarChart")
	(<PositionKind.TEXTS: 3>, array(['Paris'], dtype=object))
	"""
	accepted_families = frozenset(POSITION_KINDS)
	family = require_column_family(column, accepted_families, chart_name)
	kind = POSITION_KINDS[family]
	if kind == PositionKind.NUMBERS:
		numbers = read_numbers(column, chart_name)
		return kind, numbers

	if kind == PositionKind.MOMENTS:
		moments = read_moments(column)
		return kind, moments

	if kind == PositionKind.TIMES:
		hours = read_hours(column)
		return kind, hours

	texts = read_texts(column, chart_name)

	return kind, texts


def read_hours(column: Column) -> NDArray[numpy.float64]:
	"""
	Return a column of times of day as the hours since midnight, NaN where a time is missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column of times of day.

	Returns
	-------
	NDArray[numpy.float64]
		The hours, such as 15.5 for 15:30.

	Examples
	--------
	>>> import numpy
	>>> import pandas
	>>> from numdaplot.plots.data.column_reading import read_hours
	>>> read_hours(pandas.Series(numpy.array([55800000000, "NaT"], dtype="timedelta64[us]")))
	array([15.5,  nan])
	"""
	stored_times = column.to_numpy(dtype=TIME_DTYPE)
	missing = numpy.isnat(stored_times)
	microseconds = stored_times.astype(numpy.float64)
	hours = microseconds / MICROSECONDS_PER_HOUR
	present_hours = numpy.where(missing, numpy.nan, hours)

	return present_hours


def write_hour_labels(column: Column) -> NDArray[Any]:
	"""
	Return a column of times of day as ``HH:MM`` texts, None where a time is missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column of times of day.

	Returns
	-------
	NDArray
		One text per row, in a numpy array of Python objects.

	Examples
	--------
	>>> import numpy
	>>> import pandas
	>>> from numdaplot.plots.data.column_reading import write_hour_labels
	>>> write_hour_labels(pandas.Series(numpy.array([55800000000, "NaT"], dtype="timedelta64[us]")))
	array(['15:30', None], dtype=object)
	"""
	stored_times = column.to_numpy(dtype=TIME_DTYPE)
	times = read_times(stored_times)
	hour_labels = list[str | None]()
	for time_of_day in times:
		hour_label = None
		if time_of_day is not None:
			hour_label = time_of_day.strftime(HOUR_LABEL_PATTERN)

		hour_labels.append(hour_label)

	label_values = numpy.array(hour_labels, dtype=PYTHON_OBJECT_DTYPE)

	return label_values
