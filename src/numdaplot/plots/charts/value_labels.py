"""
The value written on each bar of a BarChart.

.. versionadded:: 0.2.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.tables.files.decimal_count import require_decimal_count


@dataclass(frozen=True)
class ValueLabels:
	"""
	The value written on each bar of a ``BarChart``, given as its ``value_labels``.

	The value is written past the end of each bar, or in the middle of each part of stacked bars. A missing value
	draws no bar and gets no label. Labels wider than vertical bars are turned upright. A label that does not fit
	its bar, even upright, is not written, with a ``ReadabilityWarning``: a larger ``Size`` gives it room.

	.. versionadded:: 0.2.0

	Parameters
	----------
	decimals
		The number of decimals written, 2 by default, the value being rounded. Whole values of integers are
		written without decimals.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidCountError
		When ``decimals`` is negative.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> clusters = ndp.Array.from_list(["Noise", "Cluster 0", "Cluster 1"])
	>>> diabetic_shares = ndp.Array.from_list([0.523, 0.531, 0.18])
	>>> shares = ndp.Table.from_arrays({"cluster": clusters, "diabetic": diabetic_shares})
	>>> chart = ndp.BarChart(x="cluster", y=["diabetic"], value_labels=ndp.ValueLabels(decimals=2))
	>>> plot = ndp.Plot.bar(shares, chart)
	>>> plot.show()
	"""

	decimals: int = 2

	def __post_init__(self) -> None:
		"""
		Check that the number of decimals is 0 or more.

		.. versionadded:: 0.2.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidCountError
			When ``decimals`` is negative.
		"""
		require_field_types(self)

		require_decimal_count(self.decimals)
