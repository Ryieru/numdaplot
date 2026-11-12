"""
Base class of every statistic.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.refused_operation_error import RefusedOperationError

CONSTRUCTOR_OPERATION = "Creating a Statistic with ndp.Statistic()"
CONSTRUCTOR_ALTERNATIVE = "a statistic such as ndp.Mean"


class Statistic:
	"""
	Base class of every statistic, a single result computed from a set of values.

	A statistic is immutable and checks its settings when it is created.

	Only its subclasses are created: calling ``ndp.Statistic()`` raises ``RefusedOperationError``.

	Every statistic, passed to ``Array.compute``, ``Calculation`` and ``Description``:

	|Statistic|What it computes|Example|
	|---|---|---|
	|``Count``|Number of values, without the missing ones by default|``ndp.Count()``|
	|``CountDistinct``|Number of distinct values that are not missing|``ndp.CountDistinct()``|
	|``Sum``|Sum of the values|``ndp.Sum()``|
	|``Mean``|Arithmetic mean of the values|``ndp.Mean()``|
	|``Median``|Median of the values, the middle value once sorted|``ndp.Median()``|
	|``Min``|Smallest value|``ndp.Min()``|
	|``Max``|Largest value|``ndp.Max()``|
	|``StandardDeviation``|How far the values spread around the mean|``ndp.StandardDeviation()``|
	|``Quantile``|Value below which a given fraction of the values lies|``ndp.Quantile(0.9)``|
	|``MostFrequent``|Value that appears the most often|``ndp.MostFrequent()``|
	|``MostFrequentCount``|Number of times the most frequent value appears|``ndp.MostFrequentCount()``|

	.. versionadded:: 0.1.0

	Raises
	------
	RefusedOperationError
		When the created object is a Statistic and not one of its subclasses.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([10.0, 30.0])
	>>> for statistic in [ndp.Min(), ndp.Mean(), ndp.Max()]:
	... 	print(prices.compute(statistic).to_value())
	10.0
	20.0
	30.0
	"""

	def __init__(self) -> None:
		"""
		Refuse the creation of the base class itself, and let a subclass be created.

		.. versionadded:: 0.1.0

		Raises
		------
		RefusedOperationError
			When the created object is a Statistic and not one of its subclasses.
		"""
		created_class = type(self)
		if created_class is Statistic:
			raise RefusedOperationError(CONSTRUCTOR_OPERATION, CONSTRUCTOR_ALTERNATIVE)
