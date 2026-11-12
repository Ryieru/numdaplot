"""
Unit tests of ArrayDisplay.

.. versionadded:: 0.2.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

from typing import Any

import numpy
import pytest
from numpy.typing import NDArray

from numdaplot.arrays import array_display
from numdaplot.arrays.array_display import ArrayDisplay

FORMAT_ARRAY_NAME = "format_array"
GRID = [[1, 2], [3, 4]]
FAKE_TEXT = "fake text"


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


def test_repr_shows_the_formatted_text(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the text of an Array is the formatted text of its values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the formatting with a fake.
	"""
	monkeypatch.setattr(array_display, FORMAT_ARRAY_NAME, format_fake_text)
	values = numpy.array(GRID)
	array = ArrayDisplay._create(values)

	array_text = repr(array)

	assert array_text == FAKE_TEXT
