"""
Base class of every function reading or building dates and durations.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.refused_operation_error import RefusedOperationError

CONSTRUCTOR_OPERATION = "Creating a TimeFunction with ndp.TimeFunction()"
CONSTRUCTOR_ALTERNATIVE = "a time function such as ndp.DatePart"


class TimeFunction:
	"""
	Base class of every function reading or building dates and durations, applied by ``Array.apply``.

	A time function is immutable. Missing values stay missing.

	Only its subclasses are created: calling ``ndp.TimeFunction()`` raises ``RefusedOperationError``.

	Every time function, passed to ``Array.apply``:

	|Time function|What it gives for each value|Example|
	|---|---|---|
	|``DatePart``|A part of a date or datetime, as a number|``ndp.DatePart(unit=ndp.DatePartUnit.MONTH)``|
	|``DatePeriod``|The first day of the period holding it|``ndp.DatePeriod(unit=ndp.PeriodUnit.MONTH)``|
	|``ToDuration``|A number read as a duration in a unit|``ndp.ToDuration(unit=ndp.DurationUnit.DAY)``|
	|``DurationIn``|A duration counted in a unit, as a decimal|``ndp.DurationIn(unit=ndp.DurationUnit.DAY)``|

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

	def __init__(self) -> None:
		"""
		Refuse the creation of the base class itself, and let a subclass be created.

		.. versionadded:: 0.1.0

		Raises
		------
		RefusedOperationError
			When the created object is a TimeFunction and not one of its subclasses.
		"""
		created_class = type(self)
		if created_class is TimeFunction:
			raise RefusedOperationError(CONSTRUCTOR_OPERATION, CONSTRUCTOR_ALTERNATIVE)
