"""
Kinds of values that a rule compares against.

.. versionadded:: 0.1.0
"""

from datetime import date, datetime, timedelta

import numpy

from numdaplot.settings.setting_types import require_setting_type

SINGLE_VALUE_EXPECTED = 'a single value such as 10 or "Paris"'
SINGLE_VALUE_TYPES = (bool, int, float, str, date, datetime, timedelta, numpy.bool_, numpy.integer, numpy.floating)

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


def require_single_value(setting_name: str, value: object) -> None:
	"""
	Check that a rule receives a single value: a boolean, a number, a text, a date, a datetime or a duration.

	.. versionadded:: 0.1.0

	Parameters
	----------
	setting_name
		The setting and the rule owning it, such as ``"Greater value"``.
	value
		The received value.

	Raises
	------
	InvalidSettingTypeError
		When the value is not a single value, such as an Array, a list or None.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.rules.rule_values import require_single_value
	>>> try:
	... 	require_single_value("Greater value", [10, 20])
	... except ndp.InvalidSettingTypeError as error:
	... 	print(error)
	Greater value expects a single value such as 10 or "Paris", got [10, 20].
	"""
	require_setting_type(setting_name, SINGLE_VALUE_EXPECTED, value, SINGLE_VALUE_TYPES)
