"""
Unit tests of ArrayExchange.

.. versionadded:: 0.1.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

from datetime import time
from typing import Any

import numpy
import pytest
from numpy.typing import NDArray

from numdaplot.arrays import array_exchange
from numdaplot.arrays.array import Array
from numdaplot.arrays.array_exchange import ArrayExchange
from numdaplot.arrays.equality.equality import Equality
from numdaplot.arrays.equality.type_match import TypeMatch
from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.errors.not_single_value_error import NotSingleValueError
from numdaplot.tables.table import Table

ARE_EQUAL_NAME = "are_equal"
GRID = [[1, 2], [3, 4]]
SINGLE_GRID = [[7]]
SINGLE_VALUE = 7
DECIMALS = [1.0, 2.0]
FIRST_POSITION = (0, 0)
CHANGED_VALUE = 99
TIME_ARRAY = Array.from_list([time(0, 1), None])
EXPECTED_TIME_OBJECTS = [time(0, 1), None]


class EqualityRecorder:
	"""
	Fake comparison recording the type setting it receives.

	.. versionadded:: 0.1.0
	"""

	def __init__(self) -> None:
		"""
		Start without recorded setting.

		.. versionadded:: 0.1.0
		"""
		self.type_matches = list[TypeMatch]()

	def compare(self, left: NDArray[Any], right: NDArray[Any], types: TypeMatch) -> bool:
		"""
		Record the type setting and answer True.

		.. versionadded:: 0.1.0

		Parameters
		----------
		left
			The first values, ignored.
		right
			The second values, ignored.
		types
			The recorded type setting.

		Returns
		-------
		bool
			Always True.
		"""
		self.type_matches.append(types)

		return True


def test_to_list_nests_one_list_per_row() -> None:
	"""
	Check that a grid gives a list of rows.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)
	array = ArrayExchange._create(values)

	python_values = array.to_list()

	assert python_values == GRID


def test_to_value_reads_the_single_value_whatever_the_dimensions() -> None:
	"""
	Check that a one-by-one grid gives its single value.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(SINGLE_GRID)
	array = ArrayExchange._create(values)

	single_value = array.to_value()

	assert single_value == SINGLE_VALUE


def test_to_value_rejects_several_values() -> None:
	"""
	Check that four values raise NotSingleValueError.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)
	array = ArrayExchange._create(values)

	with pytest.raises(NotSingleValueError):
		array.to_value()


def test_is_equal_gives_the_type_setting_to_the_comparison(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the type setting of the Equality reaches the comparison.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the comparison with a fake recording the type setting.
	"""
	recorder = EqualityRecorder()
	monkeypatch.setattr(array_exchange, ARE_EQUAL_NAME, recorder.compare)
	values = numpy.array(GRID)
	other_values = numpy.array(DECIMALS)
	array = ArrayExchange._create(values)
	other = Array._create(other_values)
	equality = Equality(other=other, types=TypeMatch.STRICT)

	is_equal = array.is_equal(equality)

	assert is_equal
	assert recorder.type_matches == [TypeMatch.STRICT]


def test_is_equal_rejects_a_value_that_is_not_an_array() -> None:
	"""
	Check that comparing with a list raises InvalidTypeError.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)
	array = ArrayExchange._create(values)
	not_an_array = Table.from_arrays({"count": Array.from_list([1, 2])})
	equality = Equality(other=not_an_array)

	with pytest.raises(InvalidTypeError):
		array.is_equal(equality)


def test_to_numpy_gives_an_independent_copy() -> None:
	"""
	Check that changing the result of to_numpy never changes the stored values.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)
	array = ArrayExchange._create(values)
	numpy_copy = array.to_numpy()

	numpy_copy[FIRST_POSITION] = CHANGED_VALUE

	stored_rows = values.tolist()
	assert stored_rows == GRID


def test_to_numpy_gives_python_times_of_day() -> None:
	"""
	Check that an Array of times gives an object array of datetime.time.

	.. versionadded:: 0.1.0
	"""
	values = TIME_ARRAY.to_numpy()

	value_list = values.tolist()
	assert value_list == EXPECTED_TIME_OBJECTS
