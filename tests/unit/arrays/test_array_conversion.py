"""
Unit tests of ArrayConversion.

.. versionadded:: 0.1.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

from typing import Any, cast

import numpy
import pytest
from numpy.typing import NDArray

from numdaplot.arrays import array_conversion
from numdaplot.arrays.array import Array
from numdaplot.arrays.array_conversion import ArrayConversion
from numdaplot.arrays.equality import Equality
from numdaplot.arrays.type_match import TypeMatch
from numdaplot.errors.not_single_value_error import NotSingleValueError
from numdaplot.errors.unsupported_operand_error import UnsupportedOperandError

ARE_EQUAL_NAME = "are_equal"
FORMAT_ARRAY_NAME = "format_array"
GRID = [[1, 2], [3, 4]]
SINGLE_GRID = [[7]]
SINGLE_VALUE = 7
DECIMALS = [1.0, 2.0]
FAKE_TEXT = "fake text"
NOT_AN_ARRAY = [1, 2]


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


def format_fake_text(values: NDArray[Any]) -> str:
	"""
	Fake text formatting returning a known text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values, ignored.

	Returns
	-------
	str
		Always the fake text.
	"""
	return FAKE_TEXT


def test_to_list_nests_one_list_per_row() -> None:
	"""
	Check that a grid gives a list of rows.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)
	array = ArrayConversion._create(values)

	python_values = array.to_list()

	assert python_values == GRID


def test_to_value_reads_the_single_value_whatever_the_dimensions() -> None:
	"""
	Check that a one-by-one grid gives its single value.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(SINGLE_GRID)
	array = ArrayConversion._create(values)

	single_value = array.to_value()

	assert single_value == SINGLE_VALUE


def test_to_value_rejects_several_values() -> None:
	"""
	Check that four values raise NotSingleValueError.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)
	array = ArrayConversion._create(values)

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
	monkeypatch.setattr(array_conversion, ARE_EQUAL_NAME, recorder.compare)
	values = numpy.array(GRID)
	other_values = numpy.array(DECIMALS)
	array = ArrayConversion._create(values)
	other = Array._create(other_values)
	equality = Equality(other=other, types=TypeMatch.STRICT)

	is_equal = array.is_equal(equality)

	assert is_equal
	assert recorder.type_matches == [TypeMatch.STRICT]


def test_is_equal_rejects_a_value_that_is_not_an_array() -> None:
	"""
	Check that comparing with a list raises UnsupportedOperandError.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)
	array = ArrayConversion._create(values)
	not_an_array = cast(Array, NOT_AN_ARRAY)
	equality = Equality(other=not_an_array)

	with pytest.raises(UnsupportedOperandError):
		array.is_equal(equality)


def test_repr_shows_the_formatted_text(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the text of an Array is the formatted text of its values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the formatting with a fake.
	"""
	monkeypatch.setattr(array_conversion, FORMAT_ARRAY_NAME, format_fake_text)
	values = numpy.array(GRID)
	array = ArrayConversion._create(values)

	array_text = repr(array)

	assert array_text == FAKE_TEXT
