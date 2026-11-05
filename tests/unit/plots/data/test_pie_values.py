"""
Unit tests of the values a PieChart shares out.

.. versionadded:: 0.1.0
"""

import warnings
from typing import Any

import numpy
import pandas
import pytest
from numpy.typing import NDArray

import numdaplot as ndp
from numdaplot.errors.empty_total_error import EmptyTotalError
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.missing_value_error import MissingValueError
from numdaplot.errors.out_of_domain_error import OutOfDomainError
from numdaplot.errors.readability_warning import ReadabilityWarning
from numdaplot.plots.data.pie_values import (
	read_pie_values,
	require_present_values,
	require_shares,
	warn_slice_count,
)
from numdaplot.plots.data.position_kind import PositionKind

CITIES = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
SALES = ndp.Array.from_list([120.0, 0.0, 45.0])
SHARES = ndp.Table.from_arrays({"city": CITIES, "sales": SALES})
CHART = ndp.PieChart(labels="city", values="sales")
EXPECTED_LABELS = ["Paris", "Lyon", "Pau"]
EXPECTED_VALUES = [120.0, 0.0, 45.0]
MISSING_LABEL_FRAME = pandas.DataFrame({"city": ["Paris", None], "sales": [120.0, 80.0]})
MISSING_LABEL_SHARES = ndp.Table.from_pandas(MISSING_LABEL_FRAME)
LABELS_WITH_MISSING = numpy.array(["Paris", None], dtype=object)
NUMBERS_WITH_MISSING = numpy.array([120.0, numpy.nan])
PRESENT_NUMBERS = numpy.array([120.0, 80.0])
NEGATIVE_NUMBERS = numpy.array([120.0, -3.0, -5.0])
ZERO_NUMBERS = numpy.array([0.0, 0.0])
READABLE_SLICE_COUNT = 5
UNREADABLE_SLICE_COUNT = 6


def test_read_pie_values_reads_the_labels_and_the_values() -> None:
	"""
	Check that the labels are text positions and the values a single series.

	.. versionadded:: 0.1.0
	"""
	pie_values = read_pie_values(SHARES, CHART)

	assert pie_values.positions.kind == PositionKind.TEXTS
	assert pie_values.positions.values.tolist() == EXPECTED_LABELS
	assert pie_values.series[0].values.tolist() == EXPECTED_VALUES
	assert pie_values.value_name == "sales"


def test_read_pie_values_rejects_labels_that_are_not_texts() -> None:
	"""
	Check that a labels column of numbers raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError):
		read_pie_values(SHARES, ndp.PieChart(labels="sales", values="sales"))


def test_read_pie_values_rejects_a_missing_label() -> None:
	"""
	Check that a missing label raises MissingValueError naming its column.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(MissingValueError, match="'city'"):
		read_pie_values(MISSING_LABEL_SHARES, CHART)


def test_require_present_values_accepts_complete_values() -> None:
	"""
	Check that values without missing one raise nothing.

	.. versionadded:: 0.1.0
	"""
	require_present_values(PRESENT_NUMBERS, "sales")


@pytest.mark.parametrize("values", [LABELS_WITH_MISSING, NUMBERS_WITH_MISSING])
def test_require_present_values_rejects_a_missing_value(values: NDArray[Any]) -> None:
	"""
	Check that a missing text or number raises MissingValueError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		Texts or numbers with a missing value.
	"""
	with pytest.raises(MissingValueError):
		require_present_values(values, "sales")


def test_require_shares_accepts_a_value_of_zero() -> None:
	"""
	Check that a slice of 0 is accepted when the total is positive.

	.. versionadded:: 0.1.0
	"""
	require_shares(numpy.array(EXPECTED_VALUES), "sales")


def test_require_shares_rejects_the_first_negative_value() -> None:
	"""
	Check that a negative value raises OutOfDomainError with the first one.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(OutOfDomainError, match="-3.0"):
		require_shares(NEGATIVE_NUMBERS, "sales")


def test_require_shares_rejects_a_total_of_zero() -> None:
	"""
	Check that values adding up to 0 raise EmptyTotalError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyTotalError):
		require_shares(ZERO_NUMBERS, "sales")


def test_warn_slice_count_is_silent_up_to_five_slices() -> None:
	"""
	Check that 5 slices emit no warning.

	.. versionadded:: 0.1.0
	"""
	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		warn_slice_count(READABLE_SLICE_COUNT)

	assert caught_warnings == []


def test_warn_slice_count_suggests_a_bar_chart_beyond_five_slices() -> None:
	"""
	Check that 6 slices emit a ReadabilityWarning suggesting plot_bar.

	.. versionadded:: 0.1.0
	"""
	with pytest.warns(ReadabilityWarning, match="Try ndp.plot_bar with a BarChart"):
		warn_slice_count(UNREADABLE_SLICE_COUNT)
