"""
Unit tests of Index.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import pytest

from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.positions.index import Index

LAST_POSITION = -1
DECIMAL_POSITION = 1.5


def test_index_accepts_a_negative_position() -> None:
	"""
	Check that a negative position, counting from the end, is kept.

	.. versionadded:: 0.1.0
	"""
	index = Index(LAST_POSITION)

	assert index.position == LAST_POSITION


def test_index_rejects_a_decimal_position() -> None:
	"""
	Check that a decimal position raises InvalidTypeError when the Index is created.

	.. versionadded:: 0.1.0
	"""
	untyped_index = cast(Any, Index)

	with pytest.raises(InvalidTypeError):
		untyped_index(DECIMAL_POSITION)
