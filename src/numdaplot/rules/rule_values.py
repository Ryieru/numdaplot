"""
Kinds of values that a rule compares against.

.. versionadded:: 0.1.0
"""

from datetime import date, datetime, timedelta

type ScalarValue = bool | int | float | str | date | datetime | timedelta
"""A single value that can be tested for equality.

.. versionadded:: 0.1.0
"""

type OrderedValue = int | float | str | date | datetime | timedelta
"""A single value that can be ordered: numbers, text in alphabetical order, dates and durations.

.. versionadded:: 0.1.0
"""
