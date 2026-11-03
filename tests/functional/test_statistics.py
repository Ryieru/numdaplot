"""
Functional tests of the statistics, as a user creates them from ndp.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp

FIRST_QUARTILE = 0.25
REJECTED_FRACTION = -0.5
ALL_STATISTICS = [
	ndp.Sum(),
	ndp.Mean(),
	ndp.Median(),
	ndp.Min(),
	ndp.Max(),
	ndp.Count(),
	ndp.CountDistinct(),
	ndp.StandardDeviation(),
	ndp.Quantile(FIRST_QUARTILE),
	ndp.MostFrequent(),
	ndp.MostFrequentCount(),
]


@pytest.mark.parametrize("statistic", ALL_STATISTICS)
def test_every_statistic_is_a_statistic(statistic: ndp.Statistic) -> None:
	"""
	Check that every statistic exposed by ndp can be created and is a Statistic.

	.. versionadded:: 0.1.0

	Parameters
	----------
	statistic
		A statistic created from ndp.
	"""
	assert isinstance(statistic, ndp.Statistic)


def test_statistics_without_settings_are_equal_when_of_the_same_class() -> None:
	"""
	Check that two Mean() are equal and that Mean() and Median() are not.

	.. versionadded:: 0.1.0
	"""
	first_mean = ndp.Mean()
	second_mean = ndp.Mean()
	median = ndp.Median()

	assert first_mean == second_mean
	assert first_mean != median


def test_a_quantile_outside_zero_to_one_is_rejected() -> None:
	"""
	Check that a user asking for a negative quantile gets InvalidFractionError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidFractionError):
		ndp.Quantile(REJECTED_FRACTION)
