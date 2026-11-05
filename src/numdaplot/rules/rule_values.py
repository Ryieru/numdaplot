"""
Kinds of values that a rule compares against.

.. versionadded:: 0.1.0
"""

from datetime import date, datetime, timedelta

type ScalarValue = bool | int | float | str | date | datetime | timedelta
"""
A single value: a boolean, a number, a text, a date, a datetime or a duration.

It is a name used by the documentation and the annotations, not an object to create: pass the value itself,
such as ``True``, ``10``, ``2.5``, ``"Paris"``, ``date(2026, 1, 31)``, ``datetime(2026, 1, 31, 14, 30)`` or
``timedelta(days=1)``.

.. versionadded:: 0.1.0

Examples
--------
>>> import numdaplot as ndp
>>> countries = ndp.Array.from_list(["FR", "DE", "FR"])
>>> countries.check(ndp.Equal("FR"))
Array([ True, False,  True], dtype=BOOL)
"""

type OrderedValue = int | float | str | date | datetime | timedelta
"""
A single value that can be ordered: a number, a text in alphabetical order, a date, a datetime or a duration.

It is a name used by the documentation and the annotations, not an object to create: pass the value itself,
such as ``10``, ``2.5``, ``"Paris"``, ``date(2026, 1, 31)``, ``datetime(2026, 1, 31, 14, 30)`` or
``timedelta(days=1)``.

.. versionadded:: 0.1.0

Examples
--------
>>> import numdaplot as ndp
>>> prices = ndp.Array.from_list([80, 120])
>>> prices.select(ndp.Greater(100))
Array([120], dtype=INT64)
"""
