"""
Units in which durations are counted.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class DurationUnit(Enum):
	"""
	Units in which durations are counted, used by ``DurationIn`` and ``ToDuration``.

	Months and years have no fixed length, so they are not duration units.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import timedelta
	>>> import numdaplot as ndp
	>>> stays = ndp.Array.from_list([timedelta(days=14)])
	>>> stays.apply(ndp.DurationIn(unit=ndp.DurationUnit.DAY))
	Array([14.], dtype=FLOAT64)
	"""

	WEEK = auto()
	"""
	A week, 7 days.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import timedelta
	>>> import numdaplot as ndp
	>>> stays = ndp.Array.from_list([timedelta(days=14)])
	>>> stays.apply(ndp.DurationIn(unit=ndp.DurationUnit.WEEK))
	Array([2.], dtype=FLOAT64)
	"""

	DAY = auto()
	"""
	A day, 24 hours.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import timedelta
	>>> import numdaplot as ndp
	>>> stays = ndp.Array.from_list([timedelta(days=14)])
	>>> stays.apply(ndp.DurationIn(unit=ndp.DurationUnit.DAY))
	Array([14.], dtype=FLOAT64)
	"""

	HOUR = auto()
	"""
	An hour, 60 minutes.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import timedelta
	>>> import numdaplot as ndp
	>>> stays = ndp.Array.from_list([timedelta(days=14)])
	>>> stays.apply(ndp.DurationIn(unit=ndp.DurationUnit.HOUR))
	Array([336.], dtype=FLOAT64)
	"""

	MINUTE = auto()
	"""
	A minute, 60 seconds.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import timedelta
	>>> import numdaplot as ndp
	>>> stays = ndp.Array.from_list([timedelta(days=14)])
	>>> stays.apply(ndp.DurationIn(unit=ndp.DurationUnit.MINUTE))
	Array([20160.], dtype=FLOAT64)
	"""

	SECOND = auto()
	"""
	A second.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import timedelta
	>>> import numdaplot as ndp
	>>> stays = ndp.Array.from_list([timedelta(days=14)])
	>>> stays.apply(ndp.DurationIn(unit=ndp.DurationUnit.SECOND))
	Array([1209600.], dtype=FLOAT64)
	"""
