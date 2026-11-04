"""
Kinds of values a chart places along its ``x`` axis.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class PositionKind(Enum):
	"""
	Kinds of values a chart places along its ``x`` axis, each drawn with its own kind of axis.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> read_array_values(prices, "LineChart").positions.kind
	<PositionKind.NUMBERS: 1>
	"""

	NUMBERS = auto()
	"""
	Numbers, placed on a numbered axis.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> read_array_values(prices, "LineChart").positions.kind
	<PositionKind.NUMBERS: 1>
	"""

	MOMENTS = auto()
	"""
	Dates or datetimes, placed on a time axis.

	Examples
	--------
	>>> from datetime import date
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.table_values import read_table_values
	>>> days = ndp.Array.from_list([date(2026, 1, 1), date(2026, 1, 2)])
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices})
	>>> read_table_values(sales, "day", ["price"], "LineChart").positions.kind
	<PositionKind.MOMENTS: 2>
	"""

	TEXTS = auto()
	"""
	Texts, each placed at its own position labeled with it.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.table_values import read_table_values
	>>> cities = ndp.Array.from_list(["Paris", "Lyon"])
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> read_table_values(sales, "city", ["price"], "LineChart").positions.kind
	<PositionKind.TEXTS: 3>
	"""
