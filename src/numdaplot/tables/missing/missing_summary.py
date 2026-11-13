"""
Summary of the missing values of each column of a Table.

.. versionadded:: 0.1.0
"""

import numpy
import pandas

from numdaplot.measures.count_division import divide_counts
from numdaplot.tables.frames.column_values import find_column_type
from numdaplot.tables.frames.time_zones import name_column_type
from numdaplot.tables.missing.missing_counts import COLUMN_SUM_AXIS, find_frame_missing

COLUMN_NAMES_COLUMN = "column"
TYPE_NAMES_COLUMN = "type"
COUNTS_COLUMN = "missing_count"
RATIOS_COLUMN = "missing_ratio"
TOTAL_LABEL = "(all columns)"
TOTAL_TYPE_NAME = ""
SUMMARY_TEXT_DTYPE = "string"
PERCENT_FORMAT = "{percent:.1f} %"
PERCENT_FACTOR = 100


def summarize_missing(frame: pandas.DataFrame) -> pandas.DataFrame:
	"""
	Return the number and the percentage of missing values of each column of a Table, then of the whole Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.

	Returns
	-------
	pandas.DataFrame
		One row per column, in order, then an ``(all columns)`` row, with the columns ``column``, ``type``,
		``missing_count`` and ``missing_ratio``. The ratios are texts such as ``"12.5 %"``,
		missing when there is no value.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.missing.missing_summary import summarize_missing
	>>> summarize_missing(pandas.DataFrame({"price": [1.5, None, 3.0], "stock": [2.0, 4.0, 1.0]}))
	          column     type  missing_count missing_ratio
	0          price  FLOAT64              1        33.3 %
	1          stock  FLOAT64              0         0.0 %
	2  (all columns)                       1        16.7 %
	"""
	missing_grid = find_frame_missing(frame)
	row_count = len(frame)
	column_counts = missing_grid.sum(axis=COLUMN_SUM_AXIS, dtype=numpy.int64)
	column_ratios = divide_counts(column_counts, row_count)
	missing_total = column_counts.sum(dtype=numpy.int64)
	total_counts = numpy.array([missing_total], dtype=numpy.int64)
	total_ratios = divide_counts(total_counts, missing_grid.size)
	counts = numpy.concatenate([column_counts, total_counts])
	ratios = numpy.concatenate([column_ratios, total_ratios])
	ratio_texts = [format_ratio(ratio) for ratio in ratios]
	summary_names = list_summary_names(frame)
	type_names = list_summary_types(frame)
	summary_columns = {
		COLUMN_NAMES_COLUMN: summary_names,
		TYPE_NAMES_COLUMN: type_names,
		COUNTS_COLUMN: counts,
		RATIOS_COLUMN: ratio_texts,
	}
	raw_summary = pandas.DataFrame(summary_columns)
	summary_dtypes = dict.fromkeys([COLUMN_NAMES_COLUMN, TYPE_NAMES_COLUMN, RATIOS_COLUMN], SUMMARY_TEXT_DTYPE)
	summary = raw_summary.astype(summary_dtypes)

	return summary


def list_summary_names(frame: pandas.DataFrame) -> list[str]:
	"""
	Return the labels of the rows of a summary: the names of the columns, then ``(all columns)``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.

	Returns
	-------
	list[str]
		One label per column, in order, then the label of the total row.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.missing.missing_summary import list_summary_names
	>>> list_summary_names(pandas.DataFrame({"price": [1.5]}))
	['price', '(all columns)']
	"""
	column_names = [str(column_name) for column_name in frame.columns]
	summary_names = [*column_names, TOTAL_LABEL]

	return summary_names


def list_summary_types(frame: pandas.DataFrame) -> list[str]:
	"""
	Return the type names of the rows of a summary: the type of each column, then an empty text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.

	Returns
	-------
	list[str]
		The ``ndp.Type`` name of each column, with its time zone when it has one, in order, then an empty
		text for the total row.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.missing.missing_summary import list_summary_types
	>>> list_summary_types(pandas.DataFrame({"price": [1.5]}))
	['FLOAT64', '']
	"""
	type_names = list[str]()

	for column_name in frame.columns:
		column = frame[column_name]
		column_type = find_column_type(column)
		type_name = name_column_type(column, column_type)
		type_names.append(type_name)

	type_names.append(TOTAL_TYPE_NAME)

	return type_names


def format_ratio(ratio: numpy.float64) -> str | None:
	"""
	Return a fraction written as a percentage with one decimal.

	.. versionadded:: 0.1.0

	Parameters
	----------
	ratio
		A fraction between 0 and 1, or NaN when there is no value.

	Returns
	-------
	str or None
		The percentage, such as ``"12.5 %"``, or ``None`` for NaN.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.missing.missing_summary import format_ratio
	>>> format_ratio(numpy.float64(0.125))
	'12.5 %'
	"""
	is_missing = bool(numpy.isnan(ratio))
	if is_missing:
		return None

	percent = ratio * PERCENT_FACTOR
	ratio_text = PERCENT_FORMAT.format(percent=percent)

	return ratio_text
