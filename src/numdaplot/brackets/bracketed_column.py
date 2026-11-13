"""
Conversion of a number column to the categories of its brackets.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.brackets.bracket_end import BracketEnd
from numdaplot.brackets.bracket_names import write_bracket_names
from numdaplot.brackets.brackets import Brackets
from numdaplot.brackets.unmatched import Unmatched
from numdaplot.column_storage.column import Column
from numdaplot.column_storage.column_values import find_column_missing, find_column_type
from numdaplot.column_storage.frame_normalization import convert_to_type
from numdaplot.errors.unmatched_value_error import BRACKETS_NAME, UnmatchedValueError
from numdaplot.rules.bounds import Bounds
from numdaplot.types.number_types import INTEGER_TYPES
from numdaplot.types.pandas_mapping import to_pandas_dtype
from numdaplot.types.type import Type

NO_CATEGORY = -1
DECIMAL_DTYPE = numpy.float64
LOW_SIDE = "right"
HIGH_SIDE = "left"


def cut_column(column: Column, brackets: Brackets) -> Column:
	"""
	Return a number column as the categories of its brackets, in the order of the brackets.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column of numbers.
	brackets
		The limits, the bounds, the open ends, the labels and what happens to a value in no bracket.

	Returns
	-------
	Column
		A ``CATEGORY`` column whose categories are the names of the brackets, missing values staying missing.

	Raises
	------
	InvalidLimitsError
		When a bracket between two limits holds no integer of a column of integers.
	UnmatchedValueError
		At the first value in no bracket, when ``others`` is ``Unmatched.ERROR``.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.brackets.bracketed_column import cut_column
	>>> ages = pandas.Series([4, None, 30], dtype="Int64")
	>>> cut_column(ages, ndp.Brackets(limits=[0, 18, 65])).tolist()
	['0 to 17', <NA>, '18 to 64']
	"""
	column_type = find_column_type(column)
	holds_integers = column_type in INTEGER_TYPES
	names = write_bracket_names(brackets, holds_integers)
	missing = find_column_missing(column)
	numbers = column.to_numpy(dtype=DECIMAL_DTYPE, na_value=numpy.nan)
	positions = find_bracket_positions(numbers, brackets)
	has_no_bracket = positions == NO_CATEGORY
	unmatched = has_no_bracket & ~missing
	require_matched_values(column, unmatched, brackets.others)
	text_dtype = to_pandas_dtype(Type.TEXT)
	categories = pandas.Index(names, dtype=text_dtype)
	# Some versions of the pandas stubs only accept a sequence of integers as codes.
	categorical_class = cast(Any, pandas.Categorical)
	raw_categorical = categorical_class.from_codes(positions, categories=categories)
	categorical = cast(pandas.Categorical, raw_categorical)
	category_column = pandas.Series(categorical, index=column.index)
	stored_column = convert_to_type(category_column, Type.CATEGORY)

	return stored_column


def find_bracket_positions(numbers: NDArray[numpy.float64], brackets: Brackets) -> NDArray[numpy.intp]:
	"""
	Return the position of the bracket of each number, -1 for a missing number or a number in no bracket.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numbers
		The numbers, NaN where missing.
	brackets
		The limits, the bounds and the open ends.

	Returns
	-------
	NDArray[numpy.intp]
		The position of each bracket, counted from the first one, open or not.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.brackets.bracketed_column import find_bracket_positions
	>>> brackets = ndp.Brackets(limits=[0, 10, 20], first=ndp.BracketEnd.OPEN)
	>>> find_bracket_positions(numpy.array([-5.0, 0.0, 10.0, 25.0, numpy.nan]), brackets)
	array([ 0,  1,  2, -1, -1])
	"""
	limits = numpy.array(brackets.limits, dtype=DECIMAL_DTYPE)
	side = LOW_SIDE if brackets.bounds == Bounds.LOW_ONLY else HIGH_SIDE
	limit_counts = numpy.searchsorted(limits, numbers, side=side)
	first_offset = 1 if brackets.first == BracketEnd.OPEN else 0
	positions = limit_counts - 1 + first_offset
	is_matched = ~numpy.isnan(numbers)
	if brackets.first == BracketEnd.CLOSED:
		is_above_first = limit_counts > 0
		is_matched = is_matched & is_above_first

	if brackets.last == BracketEnd.CLOSED:
		limit_count = limits.size
		is_below_last = limit_counts < limit_count
		is_matched = is_matched & is_below_last

	matched_positions = numpy.where(is_matched, positions, NO_CATEGORY)

	return matched_positions


def require_matched_values(column: Column, unmatched: NDArray[numpy.bool_], others: Unmatched) -> None:
	"""
	Check that every present number is in a bracket, unless the numbers in no bracket become missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The Table column of numbers.
	unmatched
		True at each present number in no bracket.
	others
		``Unmatched.ERROR`` to refuse such a number, ``Unmatched.MISSING`` to make it missing.

	Raises
	------
	UnmatchedValueError
		At the first number in no bracket, with ``Unmatched.ERROR``.

	Examples
	--------
	>>> import numpy
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.brackets.bracketed_column import require_matched_values
	>>> try:
	... 	require_matched_values(pandas.Series([5, 105]), numpy.array([False, True]), ndp.Unmatched.ERROR)
	... except ndp.UnmatchedValueError as error:
	... 	print(error.value)
	105
	"""
	if others == Unmatched.MISSING:
		return

	has_unmatched = bool(unmatched.any())
	if not has_unmatched:
		return

	unmatched_positions = numpy.flatnonzero(unmatched)
	first_position = int(unmatched_positions[0])
	python_values = column.tolist()
	first_value = python_values[first_position]
	raise UnmatchedValueError(first_value, BRACKETS_NAME)
