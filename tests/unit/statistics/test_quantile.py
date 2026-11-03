"""
Unit tests of Quantile.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.statistics import quantile
from numdaplot.statistics.quantile import Quantile

NINTH_DECILE = 0.9
REQUIRE_FRACTION_NAME = "require_fraction"


def test_quantile_keeps_its_fraction(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the fraction is available as an attribute.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the fraction check with a fake that accepts everything.
	"""
	monkeypatch.setattr(quantile, REQUIRE_FRACTION_NAME, accept_any_value)

	statistic = Quantile(NINTH_DECILE)

	assert statistic.fraction == NINTH_DECILE


def test_quantile_checks_its_fraction(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the fraction is given to the fraction check.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the fraction check with a fake that records what it receives.
	"""
	checked_values = list[float]()
	monkeypatch.setattr(quantile, REQUIRE_FRACTION_NAME, checked_values.append)

	Quantile(NINTH_DECILE)

	assert checked_values == [NINTH_DECILE]


def accept_any_value(value: float) -> None:
	"""
	Fake fraction check that accepts every value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The value to check, ignored.
	"""
