"""
Place of a Plot in the grid of a Figure.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.invalid_count_error import InvalidCountError

MINIMUM_SPAN = 1


@dataclass(frozen=True)
class Cell:
	"""
	Place of a Plot in the grid of a ``Figure``: its first cell, and how many cells it spans.

	Rows and columns are numbered from 0, row 0 at the top and column 0 on the left.

	.. versionadded:: 0.1.0

	Parameters
	----------
	row
		The row of the top cell, from 0.
	column
		The column of the left cell, from 0.
	row_span
		The number of rows covered, 1 by default.
	column_span
		The number of columns covered, 1 by default.

	Raises
	------
	InvalidCountError
		When ``row_span`` or ``column_span`` is lower than 1.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> months = ndp.Array.from_list([1, 2, 3, 4, 5, 6])
	>>> sales = ndp.Array.from_list([120.0, 150.0, 90.0, 170.0, 160.0, 185.0])
	>>> costs = ndp.Array.from_list([80.0, 95.0, 70.0, 110.0, 100.0, 120.0])
	>>> shop = ndp.Table.from_arrays({"month": months, "sales": sales, "cost": costs})
	>>> trend = ndp.plot_line(shop, ndp.LineChart(x="month", y=["sales", "cost"]))
	>>> sales_spread = ndp.plot_box(shop, ndp.BoxChart(columns=["sales"]))
	>>> cost_spread = ndp.plot_box(shop, ndp.BoxChart(columns=["cost"]))
	>>> figure = ndp.Figure(ndp.Layout(rows=2, columns=2))
	>>> figure = figure.place(trend, ndp.Cell(row=0, column=0, column_span=2))
	>>> figure = figure.place(sales_spread, ndp.Cell(row=1, column=0))
	>>> figure = figure.place(cost_spread, ndp.Cell(row=1, column=1))
	>>> figure.show()
	"""

	row: int
	column: int
	row_span: int = MINIMUM_SPAN
	column_span: int = MINIMUM_SPAN

	def __post_init__(self) -> None:
		"""
		Check the number of rows and of columns covered.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidCountError
			When ``row_span`` or ``column_span`` is lower than 1.
		"""
		if self.row_span < MINIMUM_SPAN:
			raise InvalidCountError(self.row_span, MINIMUM_SPAN)

		if self.column_span < MINIMUM_SPAN:
			raise InvalidCountError(self.column_span, MINIMUM_SPAN)
