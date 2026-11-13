"""
Unit tests of the charts of a Plot shown under new column names.

.. versionadded:: 0.1.0
"""

import numpy

import numdaplot as ndp
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.data.chart_values import ChartValues, Series
from numdaplot.plots.data.missing_cells import read_missing_counts
from numdaplot.plots.data.point_values import PointValues
from numdaplot.plots.data.renamed_layers import (
	rename_layer,
	rename_layers,
	rename_missing_counts,
	rename_optional,
	rename_points,
	rename_series,
	rename_value_name,
	rename_values,
)
from numdaplot.plots.data.sample_values import SampleValues
from numdaplot.plots.data.table_values import read_table_values
from numdaplot.plots.layers.chart_layer import ChartLayer

DAYS = ndp.Array.from_list([1, 2])
PRICES = ndp.Array.from_list([12.0, None])
COSTS = ndp.Array.from_list([8.0, 9.0])
SALES = ndp.Table.from_arrays({"day": DAYS, "price": PRICES, "cost": COSTS})
LINE_VALUES = read_table_values(SALES, "day", ["price", "cost"], "LineChart")
LINE_LAYER = ChartLayer(ndp.LineChart(), LINE_VALUES)
NEW_NAMES = {"day": "Day", "price": "Price", "zone": "Zone"}
PRICE_RENAMING = ndp.Renaming(changes=[ndp.NameChange(old_name="price", new_name="Price")])
EXPECTED_SERIES_NAMES = ["Price", "cost"]
EXPECTED_VALUE_NAME = "Price, cost"
PRICE_SERIES = Series("price", numpy.array([12.0]))
SAMPLES = SampleValues([PRICE_SERIES], None, "day", "price", ndp.Type.FLOAT64)
EXPECTED_MISSING_POSITIONS = ["Day", "Price", "cost"]
POINTS = PointValues("zone", None, "size", None)
ARRAY_VALUES = read_array_values(ndp.Array.from_list([12.0]), "LineChart")
ARRAY_NAMES = {"0": "Paris"}
SHOWN_DAY = "Day"
SHOWN_PRICE = "Price"
SHOWN_ZONE = "Zone"
KEPT_SIZE = "size"
HOUR = "hour"
DAY = "day"


def test_rename_layers_keeps_the_layers_without_renaming() -> None:
	"""
	Check that no renaming gives back the same list.

	.. versionadded:: 0.1.0
	"""
	layers = [LINE_LAYER]

	renamed_layers = rename_layers(layers, None)

	assert renamed_layers is layers


def test_rename_layers_renames_every_layer() -> None:
	"""
	Check that each layer takes the shown names.

	.. versionadded:: 0.1.0
	"""
	renamed_layers = rename_layers([LINE_LAYER, LINE_LAYER], PRICE_RENAMING)

	first_names = [series.name for series in renamed_layers[0].values.series]
	second_names = [series.name for series in renamed_layers[1].values.series]
	assert first_names == EXPECTED_SERIES_NAMES
	assert second_names == EXPECTED_SERIES_NAMES


def test_rename_layer_renames_the_points() -> None:
	"""
	Check that the color column of a scatter layer is renamed.

	.. versionadded:: 0.1.0
	"""
	layer = ChartLayer(ndp.ScatterChart(), LINE_VALUES, POINTS)

	renamed_layer = rename_layer(layer, NEW_NAMES)

	renamed_points = renamed_layer.points
	assert renamed_points is not None
	assert renamed_points.color_name == SHOWN_ZONE


def test_rename_values_renames_the_x_column_and_the_series() -> None:
	"""
	Check the positions name, the series names and the value label of chart values.

	.. versionadded:: 0.1.0
	"""
	renamed_values = rename_values(LINE_VALUES, NEW_NAMES)

	series_names = [series.name for series in renamed_values.series]
	assert isinstance(renamed_values, ChartValues)
	assert renamed_values.positions.name == SHOWN_DAY
	assert series_names == EXPECTED_SERIES_NAMES
	assert renamed_values.value_name == EXPECTED_VALUE_NAME


def test_rename_values_renames_the_group_of_samples() -> None:
	"""
	Check the group name and the value label of samples.

	.. versionadded:: 0.1.0
	"""
	renamed_samples = rename_values(SAMPLES, NEW_NAMES)

	assert isinstance(renamed_samples, SampleValues)
	assert renamed_samples.group_name == SHOWN_DAY
	assert renamed_samples.value_name == SHOWN_PRICE


def test_rename_missing_counts_renames_the_positions() -> None:
	"""
	Check that the column labels of a missing value chart are renamed.

	.. versionadded:: 0.1.0
	"""
	counts = read_missing_counts(SALES, ndp.Measure.COUNT)

	renamed_counts = rename_missing_counts(counts, NEW_NAMES)

	positions = renamed_counts.positions.values.tolist()
	assert positions == EXPECTED_MISSING_POSITIONS


def test_rename_series_keeps_the_numbers() -> None:
	"""
	Check that a renamed series keeps its numbers.

	.. versionadded:: 0.1.0
	"""
	renamed_series = rename_series([PRICE_SERIES], NEW_NAMES)

	first_series = renamed_series[0]
	assert first_series.name == SHOWN_PRICE
	assert first_series.values is PRICE_SERIES.values


def test_rename_value_name_keeps_a_label_that_names_no_column() -> None:
	"""
	Check that the Value label of an Array stays as it is.

	.. versionadded:: 0.1.0
	"""
	renamed_series = rename_series(ARRAY_VALUES.series, ARRAY_NAMES)

	value_name = rename_value_name(ARRAY_VALUES, renamed_series)

	assert value_name == ARRAY_VALUES.value_name


def test_rename_points_renames_the_color_and_size_columns() -> None:
	"""
	Check that only the renamed column of the points changes.

	.. versionadded:: 0.1.0
	"""
	renamed_points = rename_points(POINTS, NEW_NAMES)

	assert renamed_points.color_name == SHOWN_ZONE
	assert renamed_points.size_name == KEPT_SIZE


def test_rename_optional_keeps_none_and_unrenamed_names() -> None:
	"""
	Check the three cases of an optional name.

	.. versionadded:: 0.1.0
	"""
	renamed_day = rename_optional(DAY, NEW_NAMES)
	kept_hour = rename_optional(HOUR, NEW_NAMES)
	no_name = rename_optional(None, NEW_NAMES)

	assert renamed_day == SHOWN_DAY
	assert kept_hour == HOUR
	assert no_name is None
