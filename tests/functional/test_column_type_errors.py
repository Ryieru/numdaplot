"""
Functional tests of the name of the column in the type errors of a Table and of its charts.

.. versionadded:: 0.1.0
"""

from collections.abc import Callable
from datetime import datetime
from typing import Any

import pytest

import numdaplot as ndp

TRIPS = ndp.Table.from_arrays(
	{
		"day": ndp.Array.from_list([datetime(2019, 3, 1), datetime(2019, 3, 2)]),
		"paid": ndp.Array.from_list([True, False]),
		"zone": ndp.Array.from_list(["a", "b"]),
		"fare": ndp.Array.from_list([1.0, 2.0]),
	}
)
FARE_AND_ZONE = ["fare", "zone"]
MEAN_ZONE = ndp.Calculation(column="zone", function=ndp.Mean())


@pytest.mark.parametrize(
	("calculate", "expected_message"),
	[
		(
			lambda: ndp.Plot.bar(TRIPS, ndp.BarChart(x="zone", y=["day"])),
			"Cannot apply BarChart to the DATETIME column 'day'.",
		),
		(
			lambda: ndp.Plot.bar(TRIPS, ndp.BarChart(x="fare", y=["paid"])),
			"Cannot apply BarChart to the BOOL column 'paid'.",
		),
		(
			lambda: ndp.Plot.line(TRIPS, ndp.LineChart(x="fare", y=["zone"])),
			"Cannot apply LineChart to the TEXT column 'zone'.",
		),
		(
			lambda: ndp.Plot.scatter(TRIPS, ndp.ScatterChart(x="fare", y="paid")),
			"Cannot apply ScatterChart to the BOOL column 'paid'.",
		),
		(
			lambda: ndp.Plot.scatter(TRIPS, ndp.ScatterChart(x="fare", y="fare", size_by="zone")),
			"Cannot apply ScatterChart to the TEXT column 'zone'.",
		),
		(
			lambda: ndp.Plot.box(TRIPS, ndp.BoxChart(columns=["paid"])),
			"Cannot apply BoxChart to the BOOL column 'paid'.",
		),
		(
			lambda: ndp.Plot.histogram(TRIPS, ndp.HistogramChart(columns=["zone"])),
			"Cannot apply HistogramChart to the TEXT column 'zone'.",
		),
		(
			lambda: ndp.Plot.pie(TRIPS, ndp.PieChart(labels="fare", values="fare")),
			"Cannot apply PieChart to the FLOAT64 column 'fare'.",
		),
		(
			lambda: ndp.Plot.heatmap(TRIPS, ndp.HeatmapChart(columns=["zone"])),
			"Cannot apply HeatmapChart to the TEXT column 'zone'.",
		),
	],
)
def test_a_chart_names_the_column_it_refuses(calculate: Callable[[], Any], expected_message: str) -> None:
	"""
	Check the message of each kind of chart.

	.. versionadded:: 0.1.0

	Parameters
	----------
	calculate
		The drawing.
	expected_message
		The message of the error.
	"""
	with pytest.raises(ndp.IncompatibleTypesError) as error_info:
		calculate()

	error_text = str(error_info.value)
	assert error_text == expected_message


@pytest.mark.parametrize(
	("calculate", "expected_message"),
	[
		(
			lambda: TRIPS.filter(ndp.Filter(conditions=[ndp.Condition(rule=ndp.Greater(1), columns=["day"])])),
			"Cannot apply Greater to the DATETIME column 'day' and INT64.",
		),
		(
			lambda: TRIPS.filter(ndp.Filter(conditions=[ndp.Condition(rule=ndp.Contains("a"), columns=["fare"])])),
			"Cannot apply Contains to the FLOAT64 column 'fare'.",
		),
		(
			lambda: TRIPS.filter(
				ndp.Filter(conditions=[ndp.Condition(rule=ndp.Greater(0.5), columns=["fare", "zone"])])
			),
			"Cannot apply Greater to the TEXT column 'zone' and FLOAT64.",
		),
		(lambda: TRIPS.check(ndp.Contains("a")), "Cannot apply Contains to the DATETIME column 'day'."),
		(
			lambda: TRIPS.aggregate(ndp.Aggregation(calculations=[MEAN_ZONE])),
			"Cannot apply Mean to the TEXT column 'zone'.",
		),
		(
			lambda: TRIPS.aggregate(ndp.Aggregation(calculations=[MEAN_ZONE], group_by=["paid"])),
			"Cannot apply Mean to the TEXT column 'zone'.",
		),
		(
			lambda: TRIPS.pivot_table(ndp.PivotTable(rows=["paid"], columns="fare", calculation=MEAN_ZONE)),
			"Cannot apply Mean to the TEXT column 'zone'.",
		),
		(
			lambda: TRIPS.convert(ndp.Conversion(column="paid", dtype=ndp.Type.DATE)),
			"Cannot apply convert to the BOOL column 'paid' and DATE.",
		),
	],
)
def test_a_table_names_the_column_it_refuses(calculate: Callable[[], Any], expected_message: str) -> None:
	"""
	Check the message of each operation of a Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	calculate
		The operation.
	expected_message
		The message of the error.
	"""
	with pytest.raises(ndp.IncompatibleTypesError) as error_info:
		calculate()

	error_text = str(error_info.value)
	assert error_text == expected_message


def test_a_conversion_names_the_column_of_a_rejected_value() -> None:
	"""
	Check the message of a text that cannot become a number.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.ValueConversionError) as error_info:
		TRIPS.convert(ndp.Conversion(column="zone", dtype=ndp.Type.FLOAT64))

	error_text = str(error_info.value)
	assert error_text == "Cannot store the TEXT value 'a' of the column 'zone' as FLOAT64 without losing information."
	assert error_info.value.column_name == "zone"


def test_a_conversion_names_the_column_of_an_unreadable_date() -> None:
	"""
	Check the message of a text that cannot become a date.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.ValueConversionError) as error_info:
		TRIPS.convert(ndp.Conversion(column="zone", dtype=ndp.Type.DATE))

	error_text = str(error_info.value)
	assert "value 'a' of the column 'zone' as DATE" in error_text


def test_the_error_keeps_the_column_name_as_an_attribute() -> None:
	"""
	Check that the code catching the error can read the column.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.IncompatibleTypesError) as error_info:
		TRIPS.aggregate(ndp.Aggregation(calculations=[MEAN_ZONE]))

	assert error_info.value.column_name == "zone"
	assert error_info.value.type_names == ["TEXT"]


@pytest.mark.parametrize(
	("calculate", "expected_message"),
	[
		(lambda: ndp.Array.from_list([1, 2]) + "euros", "Cannot apply + to INT64 and TEXT."),
		(lambda: TRIPS.column("zone").compute(ndp.Mean()), "Cannot apply Mean to TEXT."),
	],
)
def test_an_array_names_no_column(calculate: Callable[[], Any], expected_message: str) -> None:
	"""
	Check that an Array, which has no column, keeps the short message.

	.. versionadded:: 0.1.0

	Parameters
	----------
	calculate
		The operation.
	expected_message
		The message of the error.
	"""
	with pytest.raises(ndp.IncompatibleTypesError) as error_info:
		calculate()

	error_text = str(error_info.value)
	assert error_text == expected_message
