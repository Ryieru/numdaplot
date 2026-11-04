"""
Base class of every function reading or building dates and durations.

.. versionadded:: 0.1.0
"""


class TimeFunction:
	"""
	Base class of every function reading or building dates and durations, applied by ``Array.apply``.

	A time function is immutable. Missing values stay missing.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import date
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([date(2026, 12, 31)])
	>>> for function in [ndp.DatePart(unit=ndp.DatePartUnit.MONTH), ndp.DatePeriod(unit=ndp.PeriodUnit.YEAR)]:
	... 	print(days.apply(function))
	Array([12.], dtype=FLOAT64)
	Array(['2026-01-01'], dtype=DATE)
	"""
