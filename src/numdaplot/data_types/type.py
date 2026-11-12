"""
Types of the values stored in an Array or in a Table column.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Type(Enum):
	"""
	Type of the values stored in an Array or in a Table column.

	A result outside the range of its type raises an error, never a wrong number. Prefer ``INT64`` unless memory
	matters. Each member below gives the rules of its type.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> small_counts = ndp.Array.from_list([1, 2], dtype=ndp.Type.INT8)
	>>> large_counts = ndp.Array.from_list([1000, 2000])
	>>> (small_counts + large_counts).dtype
	<Type.INT64: 4>
	>>> small_counts.convert(ndp.ArrayConversion(dtype=ndp.Type.FLOAT32)).dtype
	<Type.FLOAT32: 9>
	>>> try:
	... 	small_counts + 300
	... except ndp.IntegerOverflowError as error:
	... 	print(error)
	The operation + gives values outside the range of INT8, from -128 to 127. Convert the values to INT64 first.
	"""

	INT8 = auto()
	"""
	Signed integer from -128 to 127, 1 byte per value. It follows the rules of ``INT64``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> counts = ndp.Array.from_list([1, 2], dtype=ndp.Type.INT8)
	>>> (counts + 1).dtype, counts.compute(ndp.Sum()).dtype
	(<Type.INT8: 1>, <Type.INT64: 4>)
	>>> try:
	... 	counts + 300
	... except ndp.IntegerOverflowError as error:
	... 	print(error)
	The operation + gives values outside the range of INT8, from -128 to 127. Convert the values to INT64 first.
	"""

	INT16 = auto()
	"""
	Signed integer from -32 768 to 32 767, 2 bytes per value. It follows the rules of ``INT64``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> counts = ndp.Array.from_list([1, 2], dtype=ndp.Type.INT16)
	>>> (counts + 1).dtype, counts.compute(ndp.Sum()).dtype
	(<Type.INT16: 2>, <Type.INT64: 4>)
	>>> try:
	... 	counts + 40000
	... except ndp.IntegerOverflowError as error:
	... 	print(error)
	The operation + gives values outside the range of INT16, from -32768 to 32767. Convert the values to INT64 first.
	"""

	INT32 = auto()
	"""
	Signed integer of about +/- 2 billion, 4 bytes per value. It follows the rules of ``INT64``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> counts = ndp.Array.from_list([1, 2], dtype=ndp.Type.INT32)
	>>> (counts + 1).dtype, counts.compute(ndp.Sum()).dtype
	(<Type.INT32: 3>, <Type.INT64: 4>)
	>>> try:
	... 	counts + 3000000000
	... except ndp.IntegerOverflowError as error:
	... 	print(error)
	The operation + gives values outside the range of INT32, from -2147483648 to 2147483647.
	Convert the values to INT64 first.
	"""

	INT64 = auto()
	"""
	Signed integer of about +/- 9.2 * 10**18, 8 bytes per value. Default integer type: Python integers become
	``INT64``.

	A Python integer keeps the type of the values, a Python decimal gives ``FLOAT64``. Division, the statistics and the
	math functions giving decimals give ``FLOAT64``, ``Sum`` gives ``INT64``, and ``Min``, ``Max``, ``Absolute`` and
	``Round`` keep the type. An Array of integers cannot hold missing values: a Table column can.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> counts = ndp.Array.from_list([1, 2])
	>>> counts.dtype
	<Type.INT64: 4>
	>>> (counts + 1).dtype, (counts + 1.5).dtype, (counts / 2).dtype
	(<Type.INT64: 4>, <Type.FLOAT64: 10>, <Type.FLOAT64: 10>)
	>>> counts.compute(ndp.Sum()).dtype, counts.compute(ndp.Mean()).dtype, counts.apply(ndp.SquareRoot()).dtype
	(<Type.INT64: 4>, <Type.FLOAT64: 10>, <Type.FLOAT64: 10>)
	>>> counts.compute(ndp.Max()).dtype
	<Type.INT64: 4>
	>>> try:
	... 	ndp.Array.from_list([1, None], dtype=ndp.Type.INT64)
	... except ndp.UnsupportedMissingError as error:
	... 	print(error)
	INT64 values cannot be missing in an Array. Remove them, or give dtype=ndp.Type.FLOAT64.
	"""

	UINT8 = auto()
	"""
	Unsigned integer from 0 to 255, 1 byte per value. It follows the rules of ``INT64``, and ``Sum`` gives ``UINT64``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> counts = ndp.Array.from_list([1, 2], dtype=ndp.Type.UINT8)
	>>> (counts + 1).dtype, counts.compute(ndp.Sum()).dtype
	(<Type.UINT8: 5>, <Type.UINT64: 8>)
	>>> try:
	... 	counts - 5
	... except ndp.IntegerOverflowError as error:
	... 	print(error)
	The operation - gives values outside the range of UINT8, from 0 to 255. Convert the values to INT64 first.
	"""

	UINT16 = auto()
	"""
	Unsigned integer from 0 to 65 535, 2 bytes per value. It follows the rules of ``INT64``, and ``Sum`` gives
	``UINT64``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> counts = ndp.Array.from_list([1, 2], dtype=ndp.Type.UINT16)
	>>> (counts + 1).dtype, counts.compute(ndp.Sum()).dtype
	(<Type.UINT16: 6>, <Type.UINT64: 8>)
	>>> try:
	... 	counts - 5
	... except ndp.IntegerOverflowError as error:
	... 	print(error)
	The operation - gives values outside the range of UINT16, from 0 to 65535. Convert the values to INT64 first.
	"""

	UINT32 = auto()
	"""
	Unsigned integer from 0 to about 4 billion, 4 bytes per value. It follows the rules of ``INT64``, and ``Sum`` gives
	``UINT64``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> counts = ndp.Array.from_list([1, 2], dtype=ndp.Type.UINT32)
	>>> (counts + 1).dtype, counts.compute(ndp.Sum()).dtype
	(<Type.UINT32: 7>, <Type.UINT64: 8>)
	>>> try:
	... 	counts - 5
	... except ndp.IntegerOverflowError as error:
	... 	print(error)
	The operation - gives values outside the range of UINT32, from 0 to 4294967295. Convert the values to INT64 first.
	"""

	UINT64 = auto()
	"""
	Unsigned integer from 0 to about 1.8 * 10**19, 8 bytes per value. It follows the rules of ``INT64``, and ``Sum``
	gives ``UINT64``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> counts = ndp.Array.from_list([1, 2], dtype=ndp.Type.UINT64)
	>>> (counts + 1).dtype, counts.compute(ndp.Sum()).dtype
	(<Type.UINT64: 8>, <Type.UINT64: 8>)
	>>> try:
	... 	counts - 5
	... except ndp.IntegerOverflowError as error:
	... 	print(error)
	The operation - gives values outside the range of UINT64, from 0 to 18446744073709551615.
	Convert the values to FLOAT64 first, which keeps about 16 digits.
	"""

	FLOAT32 = auto()
	"""
	Decimal number with about 7 significant digits, 4 bytes per value. It stays ``FLOAT32`` in every calculation.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([1.5, 2.0], dtype=ndp.Type.FLOAT32)
	>>> (prices * 2.5).dtype, prices.compute(ndp.Mean()).dtype, prices.apply(ndp.SquareRoot()).dtype
	(<Type.FLOAT32: 9>, <Type.FLOAT32: 9>, <Type.FLOAT32: 9>)
	"""

	FLOAT64 = auto()
	"""
	Decimal number with about 16 significant digits, 8 bytes per value. Default decimal type: Python decimals become
	``FLOAT64``.

	Decimals combined with integers, division, and the statistics and math functions of integers giving decimals give
	``FLOAT64``. A missing value is ``nan``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([1.5, None])
	Array([1.5, nan], dtype=FLOAT64)
	>>> counts = ndp.Array.from_list([1, 3])
	>>> (counts * 0.5).dtype, counts.compute(ndp.Mean()).to_value()
	(<Type.FLOAT64: 10>, 2.0)
	"""

	BOOL = auto()
	"""
	True or false. ``Sum`` counts the true values and ``Mean`` gives their share. An Array of booleans cannot hold
	missing values: a Table column can.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> answers = ndp.Array.from_list([True, False, True, True])
	>>> answers.compute(ndp.Sum()).to_value(), answers.compute(ndp.Mean()).to_value()
	(3, 0.75)
	>>> try:
	... 	ndp.Array.from_list([True, None])
	... except ndp.UnsupportedMissingError as error:
	... 	print(error)
	BOOL values cannot be missing in an Array. Remove them.
	"""

	TEXT = auto()
	"""
	Text of any length. Python texts become ``TEXT``. A missing text is shown as ``nan``, and given as None by
	``to_list``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", None])
	>>> cities
	Array(['Paris', nan], dtype=TEXT)
	>>> cities.to_list()
	['Paris', None]
	"""

	CATEGORY = auto()
	"""
	Text taking a few repeated values, stored once per distinct value. Table columns only: ``Table.column`` gives
	their values as ``TEXT``, and ``ArrayConversion`` refuses it.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> categories = sales.convert(ndp.TableConversion(column="city", dtype=ndp.Type.CATEGORY))
	>>> categories.column_types["city"], categories.column("city").dtype
	(<Type.CATEGORY: 13>, <Type.TEXT: 12>)
	"""

	DATE = auto()
	"""
	A day, without time. Python dates become ``DATE``. Stored in days, but a calculation on it stays within 1677 to
	2262, as ``DATETIME``. A missing date is ``NaT``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import date
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([date(2026, 1, 31), None])
	Array(['2026-01-31',        'NaT'], dtype=DATE)
	"""

	DATETIME = auto()
	"""
	A day and a time, with or without time zone, from 1677 to 2262. Python datetimes become ``DATETIME``. A missing
	datetime is ``NaT``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([datetime(2026, 1, 31, 8, 30), None]).dtype
	<Type.DATETIME: 15>
	"""

	DURATION = auto()
	"""
	A gap between two dates or datetimes, of about 292 years at most, before or after zero. Python durations
	(``timedelta``) become ``DURATION``. A missing duration is ``NaT``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import timedelta
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([timedelta(hours=2), None]).dtype
	<Type.DURATION: 16>
	"""

	TIME = auto()
	"""
	A time of day, from 00:00 to 23:59:59.999999, without date nor time zone. Stored as the time since midnight.
	Python times of day become ``TIME``, and a missing one is given as None by ``to_list``.

	Two times give a ``DURATION`` when subtracted, a duration moves a time within its day, and a time added to a
	``DATE`` gives a ``DATETIME``. Its hour, minute and second are read with ``DatePart``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import time
	>>> import numdaplot as ndp
	>>> ndp.Array.from_list([time(15, 35), None]).to_list()
	[datetime.time(15, 35), None]
	"""
