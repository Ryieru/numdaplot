"""
Unit tests of the names of statistics.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.statistics.count import Count
from numdaplot.statistics.count_distinct import CountDistinct
from numdaplot.statistics.counted_missing import CountedMissing
from numdaplot.statistics.most_frequent_count import MostFrequentCount
from numdaplot.statistics.quantile import Quantile
from numdaplot.statistics.standard_deviation import StandardDeviation
from numdaplot.statistics.statistic import Statistic
from numdaplot.statistics.sum import Sum
from numdaplot.tables.aggregation.statistic_name import name_quantile, name_statistic

QUARTILE = 0.25
LAST_DECILE = 0.9
HIGH_FRACTION = 0.975
TENTH = 0.1


class UnknownStatistic(Statistic):
	"""
	A statistic numdaplot does not know.

	.. versionadded:: 0.1.0
	"""


@pytest.mark.parametrize(
	("statistic", "expected_name"),
	[
		(Sum(), "sum"),
		(Count(), "count_excluded"),
		(Count(missing=CountedMissing.INCLUDED), "count_included"),
		(CountDistinct(), "count_distinct"),
		(StandardDeviation(), "standard_deviation"),
		(MostFrequentCount(), "most_frequent_count"),
		(Quantile(LAST_DECILE), "quantile_90"),
	],
)
def test_name_statistic_uses_lowercase_words_joined_by_underscores(statistic: Statistic, expected_name: str) -> None:
	"""
	Check the name of several statistics.

	.. versionadded:: 0.1.0

	Parameters
	----------
	statistic
		A statistic of numdaplot.
	expected_name
		Its name.
	"""
	statistic_name = name_statistic(statistic)

	assert statistic_name == expected_name


def test_name_statistic_rejects_an_unknown_statistic() -> None:
	"""
	Check that a statistic numdaplot does not know raises RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedOperationError):
		name_statistic(UnknownStatistic())


@pytest.mark.parametrize(
	("fraction", "expected_name"),
	[
		(QUARTILE, "quantile_25"),
		(HIGH_FRACTION, "quantile_97_5"),
		(TENTH, "quantile_10"),
	],
)
def test_name_quantile_writes_the_fraction_as_a_percentage(fraction: float, expected_name: str) -> None:
	"""
	Check that the decimal point becomes an underscore and rounding noise disappears.

	.. versionadded:: 0.1.0

	Parameters
	----------
	fraction
		The fraction of the quantile.
	expected_name
		Its name.
	"""
	quantile_name = name_quantile(Quantile(fraction))

	assert quantile_name == expected_name
