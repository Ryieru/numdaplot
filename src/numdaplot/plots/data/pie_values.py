"""
Values a PieChart shares out, read from a Table.

.. versionadded:: 0.1.0
"""

import warnings
from typing import Any

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.errors.empty_total_error import EmptyTotalError
from numdaplot.errors.missing_value_error import MissingValueError
from numdaplot.errors.out_of_domain_error import OutOfDomainError
from numdaplot.errors.readability_warning import ReadabilityWarning
from numdaplot.plots.charts.pie_chart import PieChart
from numdaplot.plots.data.chart_values import ChartValues, Positions, Series
from numdaplot.plots.data.column_reading import read_numbers, read_texts
from numdaplot.plots.data.position_kind import PositionKind
from numdaplot.plots.data.unique_labels import require_unique_labels
from numdaplot.tables.columns.column_names import require_known_columns
from numdaplot.tables.frames.column_values import find_column_type
from numdaplot.tables.table import Table
from numdaplot.tables.table_data import read_stored_frame

CHART_NAME = "PieChart"
MAXIMUM_READABLE_SLICES = 5
READABILITY_START = "A PieChart with {slice_count} slices is hard to read."
READABILITY_ADVICE = "Try ndp.Plot.bar with a BarChart, it may compare them better."
READABILITY_MESSAGE = f"{READABILITY_START} {READABILITY_ADVICE}"
# Number of calls between the warning and the line of the user.
READABILITY_STACK_LEVEL = 5


def read_pie_values(table: Table, chart: PieChart) -> ChartValues:
	"""
	Return the labels and the values of the slices of a PieChart, after checking that they can be shared out.

	.. versionadded:: 0.1.0

	Parameters
	----------
	table
		The Table drawn.
	chart
		The ``labels`` and ``values`` columns.

	Returns
	-------
	ChartValues
		The labels as text positions, and the values as a single series.

	Raises
	------
	ColumnNotFoundError
		When a column does not exist.
	IncompatibleTypesError
		When ``labels`` does not hold texts, or ``values`` does not hold numbers.
	MissingValueError
		When a label or a value is missing.
	OutOfDomainError
		When a value is negative.
	EmptyTotalError
		When the values add up to 0.
	DuplicateLabelError
		When two slices have the same label.

	Warns
	-----
	ReadabilityWarning
		When there are more than 5 slices.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.pie_values import read_pie_values
	>>> cities = ndp.Array.from_list(["Paris", "Lyon"])
	>>> sales = ndp.Array.from_list([120.0, 80.0])
	>>> shares = ndp.Table.from_arrays({"city": cities, "sales": sales})
	>>> read_pie_values(shares, ndp.PieChart(labels="city", values="sales")).series[0].values
	array([120.,  80.])
	"""
	labels_name = chart.labels
	values_name = chart.values
	frame = read_stored_frame(table)
	known_names = frame.columns.tolist()
	require_known_columns([labels_name, values_name], known_names)
	labels = read_texts(frame[labels_name], CHART_NAME)
	numbers = read_numbers(frame[values_name], CHART_NAME)
	require_present_values(labels, labels_name)
	require_present_values(numbers, values_name)
	require_unique_labels(labels)
	require_shares(numbers, values_name)
	slice_count = len(labels)
	warn_slice_count(slice_count)
	rows = numpy.arange(slice_count)
	positions = Positions(PositionKind.TEXTS, labels, labels_name)
	values_series = Series(values_name, numbers)
	values_column = frame[values_name]
	values_type = find_column_type(values_column)
	pie_values = ChartValues(positions, [values_series], rows, values_name, values_type)

	return pie_values


def require_present_values(values: NDArray[Any], column_name: str) -> None:
	"""
	Check that a column drawn by a PieChart has no missing value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The labels, None where missing, or the numbers, NaN where missing.
	column_name
		The column read, shown in the error message.

	Raises
	------
	MissingValueError
		When a value is missing.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.pie_values import require_present_values
	>>> try:
	... 	require_present_values(numpy.array([120.0, numpy.nan]), "sales")
	... except ndp.MissingValueError as error:
	... 	print(error)
	PieChart cannot draw a missing value, found one in 'sales'.
	"""
	missing = pandas.isna(values)
	has_missing = bool(missing.any())
	if has_missing:
		raise MissingValueError(CHART_NAME, column_name)


def require_shares(numbers: NDArray[numpy.float64], column_name: str) -> None:
	"""
	Check that the values of a PieChart can be shared out: none is negative and their total is above 0.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numbers
		The value of each slice, none missing.
	column_name
		The column of the values, shown in the error message.

	Raises
	------
	OutOfDomainError
		At the first negative value.
	EmptyTotalError
		When the values add up to 0.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.pie_values import require_shares
	>>> try:
	... 	require_shares(numpy.array([120.0, -3.0]), "sales")
	... except ndp.OutOfDomainError as error:
	... 	print(error)
	PieChart is not defined for -3.0.
	"""
	negative_numbers = numbers[numbers < 0]
	negative_count = len(negative_numbers)
	if negative_count > 0:
		first_negative = float(negative_numbers[0])
		raise OutOfDomainError(CHART_NAME, first_negative)

	total = numbers.sum()
	if total == 0:
		raise EmptyTotalError(CHART_NAME, column_name)


def warn_slice_count(slice_count: int) -> None:
	"""
	Emit a ReadabilityWarning when a PieChart has more than 5 slices.

	.. versionadded:: 0.1.0

	Parameters
	----------
	slice_count
		The number of slices.

	Warns
	-----
	ReadabilityWarning
		When there are more than 5 slices.

	Examples
	--------
	>>> import warnings
	>>> from numdaplot.plots.data.pie_values import warn_slice_count
	>>> with warnings.catch_warnings(record=True) as caught_warnings:
	... 	warnings.simplefilter("always")
	... 	warn_slice_count(6)
	>>> print(caught_warnings[0].message)
	A PieChart with 6 slices is hard to read. Try ndp.Plot.bar with a BarChart, it may compare them better.
	"""
	if slice_count <= MAXIMUM_READABLE_SLICES:
		return

	message = READABILITY_MESSAGE.format(slice_count=slice_count)
	warnings.warn(message, ReadabilityWarning, stacklevel=READABILITY_STACK_LEVEL)
