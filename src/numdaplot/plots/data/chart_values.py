"""
Values a chart draws, read from a Table or an Array.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass
from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.plots.data.position_kind import PositionKind
from numdaplot.types.type import Type


@dataclass(frozen=True, eq=False)
class Positions:
	"""
	The ``x`` values of a chart.

	.. versionadded:: 0.1.0

	Parameters
	----------
	kind
		Numbers, moments, texts or times of day.
	values
		One value per row: float64 numbers with NaN, datetime64[ns] clock times with NaT, texts, or float64 hours
		since midnight with NaN.
	name
		The name of the ``x`` column, or None for row numbers.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.data.chart_values import Positions
	>>> from numdaplot.plots.data.position_kind import PositionKind
	>>> Positions(PositionKind.NUMBERS, numpy.array([0.0, 1.0]), None).values
	array([0., 1.])
	"""

	kind: PositionKind
	values: NDArray[Any]
	name: str | None


@dataclass(frozen=True, eq=False)
class Series:
	"""
	One series of values drawn by a chart, as numbers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		The name shown in the legend: the column name, or the column number of an Array.
	values
		One float64 number per row, NaN where the value is missing or not drawn. A time of day is its hours since
		midnight, such as 15.5 for 15:30.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.data.chart_values import Series
	>>> Series("price", numpy.array([12.0, numpy.nan])).name
	'price'
	"""

	name: str
	values: NDArray[numpy.float64]


@dataclass(frozen=True, eq=False)
class ChartValues:
	"""
	The positions and the series a chart draws.

	.. versionadded:: 0.1.0

	Parameters
	----------
	positions
		The ``x`` values.
	series
		The series of numbers, each with one value per position.
	rows
		The row numbers of the source kept for drawing, to read other columns of the same rows.
	value_name
		The name of the series: the names of the ``y`` columns of a Table as ``name_columns`` writes them, or
		``Value`` for an Array. It labels the axis of a single series, and names the series in the default title.
	value_type
		The type of the first series, of the family of every series: numbers or times of day.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> grid = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
	>>> [series.name for series in read_array_values(grid, "LineChart").series]
	['0', '1']
	"""

	positions: Positions
	series: list[Series]
	rows: NDArray[numpy.intp]
	value_name: str | None
	value_type: Type
