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
	"""
	Signed integer from -128 to 127, 1 byte per value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([1, -2], dtype=ndp.Type.INT8)
	Array([ 1, -2], dtype=INT8)
	"""

	INT16 = auto()
	"""
	Signed integer from -32 768 to 32 767, 2 bytes per value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([1, -2], dtype=ndp.Type.INT16)
	Array([ 1, -2], dtype=INT16)
	"""

	INT32 = auto()
	"""
	Signed integer of about +/- 2 billion, 4 bytes per value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([1, -2], dtype=ndp.Type.INT32)
	Array([ 1, -2], dtype=INT32)
	"""

	INT64 = auto()
	"""
	Signed integer of about +/- 9.2 * 10**18, 8 bytes per value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([1, -2], dtype=ndp.Type.INT64)
	Array([ 1, -2], dtype=INT64)
	"""

	UINT8 = auto()
	"""
	Unsigned integer from 0 to 255, 1 byte per value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([1, 2], dtype=ndp.Type.UINT8)
	Array([1, 2], dtype=UINT8)
	"""

	UINT16 = auto()
	"""
	Unsigned integer from 0 to 65 535, 2 bytes per value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([1, 2], dtype=ndp.Type.UINT16)
	Array([1, 2], dtype=UINT16)
	"""

	UINT32 = auto()
	"""
	Unsigned integer from 0 to about 4 billion, 4 bytes per value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([1, 2], dtype=ndp.Type.UINT32)
	Array([1, 2], dtype=UINT32)
	"""

	UINT64 = auto()
	"""
	Unsigned integer from 0 to about 1.8 * 10**19, 8 bytes per value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([1, 2], dtype=ndp.Type.UINT64)
	Array([1, 2], dtype=UINT64)
	"""

	FLOAT32 = auto()
	"""
	Decimal number with about 7 significant digits, 4 bytes per value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([1.5, 2.0], dtype=ndp.Type.FLOAT32)
	Array([1.5, 2. ], dtype=FLOAT32)
	"""

	FLOAT64 = auto()
	"""
	Decimal number with about 16 significant digits, 8 bytes per value. Default decimal type.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([1.5, None], dtype=ndp.Type.FLOAT64)
	Array([1.5, nan], dtype=FLOAT64)
	"""

	BOOL = auto()
	"""
	True or false.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([True, False], dtype=ndp.Type.BOOL)
	Array([ True, False], dtype=BOOL)
	"""

	TEXT = auto()
	"""
	Text of any length.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list(["Paris", "Lyon"], dtype=ndp.Type.TEXT)
	Array(['Paris', 'Lyon'], dtype=TEXT)
	"""

	CATEGORY = auto()
	"""
	Text taking a few repeated values, stored once per distinct value. Table columns only.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> categories = sales.convert(ndp.Conversion(column="city", dtype=ndp.Type.CATEGORY))
	>>> categories.column_types["city"]
	<Type.CATEGORY: 13>
	"""

	DATE = auto()
	"""
	A day, without time. Stored in days, but a calculation on it stays within 1677 to 2262, as ``DATETIME``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import date
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([date(2026, 1, 31)]).dtype
	<Type.DATE: 14>
	"""

	DATETIME = auto()
	"""
	A day and a time, with or without time zone, from 1677 to 2262.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([datetime(2026, 1, 31, 8, 30)]).dtype
	<Type.DATETIME: 15>
	"""

	DURATION = auto()
	"""
	A gap between two dates or datetimes, of about 292 years at most, before or after zero.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import timedelta
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([timedelta(hours=2)]).dtype
	<Type.DURATION: 16>
	"""

	TIME = auto()
	"""
	A time of day, from 00:00 to 23:59:59.999999, without date nor time zone. Stored as the time since midnight.

	.. versionadded:: 0.1.0

	Two times give a ``DURATION`` when subtracted, a duration moves a time within its day, and a time added to a
	``DATE`` gives a ``DATETIME``. Its hour, minute and second are read with ``DatePart``.

	Examples
	--------
	>>> from datetime import time
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([time(15, 35)]).dtype
	<Type.TIME: 17>
	"""
