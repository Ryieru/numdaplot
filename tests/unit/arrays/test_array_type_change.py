"""
Unit tests of ArrayTypeChange.

.. versionadded:: 0.2.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

from typing import Any, cast

import numpy
import pytest
from numpy.typing import NDArray

from numdaplot.arrays import array_type_change
from numdaplot.arrays.array_type_change import ArrayTypeChange
from numdaplot.conversions.array_conversion import ArrayConversion
from numdaplot.conversions.table_conversion import TableConversion
from numdaplot.data_types.type import Type
from numdaplot.errors.invalid_type_error import InvalidTypeError

CONVERT_VALUES_NAME = "convert_array_values"
COUNTS = numpy.array([1, 2])
FAKE_RESULT = numpy.array(["converted"], dtype=object)
TEXT_CONVERSION = ArrayConversion(dtype=Type.TEXT)
TABLE_TEXT_CONVERSION = TableConversion(columns=["count"], dtype=Type.TEXT)


class ConversionRecorder:
	"""
	Fake conversion of values recording the conversion it receives.

	.. versionadded:: 0.2.0
	"""

	def __init__(self) -> None:
		"""
		Start without recorded conversion.

		.. versionadded:: 0.2.0
		"""
		self.conversions = list[ArrayConversion]()

	def convert(self, values: NDArray[Any], conversion: ArrayConversion) -> NDArray[Any]:
		"""
		Record the conversion and give a fixed result.

		.. versionadded:: 0.2.0

		Parameters
		----------
		values
			The values of the Array, ignored.
		conversion
			The conversion asked.

		Returns
		-------
		NDArray
			The fixed result.
		"""
		self.conversions.append(conversion)

		return FAKE_RESULT


def test_convert_gives_the_conversion_to_the_conversion_of_values(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that convert passes its conversion on and wraps the converted values in a new object.

	.. versionadded:: 0.2.0

	Parameters
	----------
	monkeypatch
		Replaces the conversion of values with a recorder.
	"""
	recorder = ConversionRecorder()
	monkeypatch.setattr(array_type_change, CONVERT_VALUES_NAME, recorder.convert)
	array = ArrayTypeChange._create(COUNTS)

	converted_array = array.convert(TEXT_CONVERSION)

	assert recorder.conversions == [TEXT_CONVERSION]
	assert converted_array._values is FAKE_RESULT
	assert converted_array is not array


def test_convert_refuses_a_table_conversion() -> None:
	"""
	Check that a TableConversion raises InvalidTypeError.

	.. versionadded:: 0.2.0
	"""
	array = ArrayTypeChange._create(COUNTS)
	table_conversion = cast(Any, TABLE_TEXT_CONVERSION)

	with pytest.raises(InvalidTypeError):
		array.convert(table_conversion)
