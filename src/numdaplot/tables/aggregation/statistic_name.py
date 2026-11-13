"""
Names of the statistics in the column names of an aggregation and in a description.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.statistics.statistic_values import UNKNOWN_STATISTIC_ALTERNATIVE, UNKNOWN_STATISTIC_OPERATION
from numdaplot.errors.settings.refused_operation_error import RefusedOperationError
from numdaplot.statistics.count import Count
from numdaplot.statistics.count_distinct import CountDistinct
from numdaplot.statistics.counted_missing import CountedMissing
from numdaplot.statistics.maximum import Max
from numdaplot.statistics.mean import Mean
from numdaplot.statistics.median import Median
from numdaplot.statistics.minimum import Min
from numdaplot.statistics.most_frequent import MostFrequent
from numdaplot.statistics.most_frequent_count import MostFrequentCount
from numdaplot.statistics.quantile import Quantile
from numdaplot.statistics.share import Share
from numdaplot.statistics.standard_deviation import StandardDeviation
from numdaplot.statistics.statistic import Statistic
from numdaplot.statistics.sum import Sum

STATISTIC_NAMES = {
	Sum: "sum",
	Mean: "mean",
	Median: "median",
	Min: "min",
	Max: "max",
	CountDistinct: "count_distinct",
	StandardDeviation: "standard_deviation",
	MostFrequent: "most_frequent",
	MostFrequentCount: "most_frequent_count",
	Share: "share",
}
COUNT_NAMES = {
	CountedMissing.EXCLUDED: "count_excluded",
	CountedMissing.INCLUDED: "count_included",
}
QUANTILE_NAME = "quantile_{percent}"
PERCENT_FACTOR = 100
PERCENT_DIGITS = 10
GENERAL_NUMBER_FORMAT = "g"
DECIMAL_POINT = "."
NAME_SEPARATOR = "_"


def name_statistic(statistic: Statistic) -> str:
	"""
	Return the name of a statistic, in lowercase words joined by underscores.

	.. versionadded:: 0.1.0

	.. versionchanged:: 0.2.0
		Names ``Share``.

	Parameters
	----------
	statistic
		Any statistic of numdaplot.

	Returns
	-------
	str
		The name, such as ``standard_deviation``, ``quantile_90`` for ``Quantile(0.9)``, or ``count_excluded`` for
		``Count()``.

	Raises
	------
	RefusedOperationError
		When the statistic is not a statistic of numdaplot.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.aggregation.statistic_name import name_statistic
	>>> name_statistic(ndp.CountDistinct())
	'count_distinct'
	"""
	if isinstance(statistic, Quantile):
		quantile_name = name_quantile(statistic)
		return quantile_name

	if isinstance(statistic, Count):
		count_name = COUNT_NAMES[statistic.missing]
		return count_name

	statistic_class = type(statistic)
	if statistic_class not in STATISTIC_NAMES:
		operation = UNKNOWN_STATISTIC_OPERATION.format(statistic_name=statistic_class.__name__)
		raise RefusedOperationError(operation, UNKNOWN_STATISTIC_ALTERNATIVE)

	statistic_name = STATISTIC_NAMES[statistic_class]

	return statistic_name


def name_quantile(quantile: Quantile) -> str:
	"""
	Return the name of a quantile, holding its fraction as a percentage.

	.. versionadded:: 0.1.0

	Parameters
	----------
	quantile
		The quantile.

	Returns
	-------
	str
		``quantile_90`` for 0.9, and ``quantile_97_5`` for 0.975: an underscore replaces the decimal point.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.aggregation.statistic_name import name_quantile
	>>> name_quantile(ndp.Quantile(0.975))
	'quantile_97_5'
	"""
	percent = quantile.fraction * PERCENT_FACTOR
	rounded_percent = round(percent, PERCENT_DIGITS)
	percent_text = format(rounded_percent, GENERAL_NUMBER_FORMAT)
	percent_name = percent_text.replace(DECIMAL_POINT, NAME_SEPARATOR)
	quantile_name = QUANTILE_NAME.format(percent=percent_name)

	return quantile_name
