"""
Types of the values stored in an Array or in a Table column.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Type(Enum):
	"""
	Type of the values stored in an Array or in a Table column.

	Integers wrap around silently when a result exceeds their range, as in numpy:
	with ``INT8``, ``127 + 1`` gives ``-128``. Prefer ``INT64`` unless memory matters.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([1, 2], dtype=ndp.Type.FLOAT32)
	Array([1., 2.], dtype=FLOAT32)
	>>> ndp.Array.from_list([1.5, 2.0]).dtype
	<Type.FLOAT64: 10>
	"""

	INT8 = auto()
	"""Signed integer from -128 to 127, 1 byte per value."""

	INT16 = auto()
	"""Signed integer from -32 768 to 32 767, 2 bytes per value."""

	INT32 = auto()
	"""Signed integer of about +/- 2 billion, 4 bytes per value."""

	INT64 = auto()
	"""Signed integer of about +/- 9.2 * 10**18, 8 bytes per value."""

	UINT8 = auto()
	"""Unsigned integer from 0 to 255, 1 byte per value."""

	UINT16 = auto()
	"""Unsigned integer from 0 to 65 535, 2 bytes per value."""

	UINT32 = auto()
	"""Unsigned integer from 0 to about 4 billion, 4 bytes per value."""

	UINT64 = auto()
	"""Unsigned integer from 0 to about 1.8 * 10**19, 8 bytes per value."""

	FLOAT32 = auto()
	"""Decimal number with about 7 significant digits, 4 bytes per value."""

	FLOAT64 = auto()
	"""Decimal number with about 16 significant digits, 8 bytes per value. Default decimal type."""

	BOOL = auto()
	"""True or false."""

	TEXT = auto()
	"""Text of any length."""

	CATEGORY = auto()
	"""Text taking a few repeated values, stored once per distinct value. Table columns only."""

	DATE = auto()
	"""A day, without time."""

	DATETIME = auto()
	"""A day and a time, with or without time zone."""

	DURATION = auto()
	"""A gap between two dates or datetimes."""
