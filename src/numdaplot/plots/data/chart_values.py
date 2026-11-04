"""
Values a chart draws, read from a Table or an Array.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass
from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.plots.data.position_kind import PositionKind


@dataclass(frozen=True, eq=False)
class Positions:
	"""
	The ``x`` values of a chart.

	.. versionadded:: 0.1.0

	Parameters
	----------
	kind
		Numbers, moments or texts.
	values
		One value per row: float64 numbers with NaN, datetime64[ns] clock times with NaT, or texts.
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
	One series of numbers drawn by a chart.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		The name shown in the legend: the column name, or the column number of an Array.
	values
		One float64 number per row, NaN where the value is missing or not drawn.

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
		The default label of the axis of the series: the name of the single ``y`` column of a Table, None
		otherwise.

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
