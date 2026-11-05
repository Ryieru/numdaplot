"""
Unit tests of TableSelection, TableColumns, TableCalculation, TableLayout and TableMissing.

Each method hands the columns to a helper, faked here, and wraps the result in a new Table.

.. versionadded:: 0.1.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

from collections.abc import Callable
from types import ModuleType
from typing import Any

import numpy
import pandas
import pytest
from numpy.typing import NDArray

from numdaplot.arrays.array import Array
from numdaplot.data_types.type import Type
from numdaplot.positions.axis import Axis
from numdaplot.positions.index import Index
from numdaplot.positions.region import Region
from numdaplot.rules.greater import Greater
from numdaplot.rules.is_missing import IsMissing
from numdaplot.statistics.mean import Mean
from numdaplot.tables import table_calculation, table_columns, table_layout, table_missing, table_selection
from numdaplot.tables.aggregation.aggregation import Aggregation
from numdaplot.tables.aggregation.calculation import Calculation
from numdaplot.tables.columns.column_choice import ColumnChoice
from numdaplot.tables.columns.conversion import Conversion
from numdaplot.tables.columns.new_column import NewColumn
from numdaplot.tables.columns.renaming import Renaming
from numdaplot.tables.description.description import Description
from numdaplot.tables.duplicates.deduplication import Deduplication
from numdaplot.tables.filtering.condition import Condition
from numdaplot.tables.filtering.filter import Filter
from numdaplot.tables.frames.column import Column
from numdaplot.tables.missing.missing_count import MissingCount
from numdaplot.tables.missing.missing_drop import MissingDrop
from numdaplot.tables.sorting.sort_key import SortKey
from numdaplot.tables.sorting.sorting import Sorting
from numdaplot.tables.table import Table

FRAME = pandas.DataFrame({"price": [5.0, 12.0, 30.0]})
FAKE_FRAME = pandas.DataFrame({"result": [1.0]})
EXPECTED_FAKE_NAMES = ["result"]
FAKE_MASK = numpy.array([False, True, True])
EXPECTED_FILTERED_PRICES = [12.0, 30.0]
EXPECTED_FILTERED_ROWS = [0, 1]
FAKE_COLUMN = pandas.Series(["5", "12", "30"], dtype="string")
EXPECTED_CONVERTED_TYPES = {"price": Type.TEXT}
ROW_FILTER = Filter(conditions=[Condition(rule=Greater(10))])
BUILD_FILTER_MASK_NAME = "build_filter_mask"
CONVERT_COLUMN_NAME = "convert_column"
PRICE_MEAN = Calculation(column="price", function=Mean())
type TableOperation = Callable[[Table], Table]
FRAME_OPERATIONS = list[tuple[ModuleType, str, TableOperation]](
	[
		(table_selection, "take_region", lambda table: table.take(Region(rows=Index(0)))),
		(table_selection, "check_frame", lambda table: table.check(IsMissing())),
		(table_columns, "choose_frame_columns", lambda table: table.choose_columns(ColumnChoice(columns=["price"]))),
		(
			table_columns,
			"rename_frame_columns",
			lambda table: table.rename([Renaming(old_name="price", new_name="cost")]),
		),
		(
			table_columns,
			"add_frame_column",
			lambda table: table.add_column(NewColumn(name="count", values=Array.from_list([1, 2, 3]))),
		),
		(
			table_calculation,
			"aggregate_frame",
			lambda table: table.aggregate(Aggregation(calculations=[PRICE_MEAN])),
		),
		(table_calculation, "describe_frame", lambda table: table.describe(Description())),
		(table_layout, "sort_frame", lambda table: table.sort(Sorting(keys=[SortKey(column="price")]))),
		(table_layout, "drop_duplicate_rows", lambda table: table.drop_duplicates(Deduplication())),
		(
			table_missing,
			"count_frame_missing",
			lambda table: table.count_missing(MissingCount(axis=Axis.EACH_COLUMN)),
		),
		(table_missing, "drop_frame_missing", lambda table: table.drop_missing(MissingDrop())),
	]
)


def give_fake_frame(frame: pandas.DataFrame, settings: object) -> pandas.DataFrame:
	"""
	Fake helper returning known columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of the Table, ignored.
	settings
		The settings of the operation, ignored.

	Returns
	-------
	pandas.DataFrame
		Always the fake columns.
	"""
	return FAKE_FRAME


def give_fake_mask(frame: pandas.DataFrame, row_filter: Filter) -> NDArray[Any]:
	"""
	Fake filter mask keeping the last two rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns, ignored.
	row_filter
		The filter, ignored.

	Returns
	-------
	NDArray[numpy.bool_]
		Always the fake mask.
	"""
	return FAKE_MASK


def give_fake_column(column: Column, conversion: Conversion) -> Column:
	"""
	Fake conversion returning known texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The converted column, ignored.
	conversion
		The conversion, ignored.

	Returns
	-------
	Column
		Always the fake texts.
	"""
	return FAKE_COLUMN


@pytest.mark.parametrize(("module", "helper_name", "operation"), FRAME_OPERATIONS)
def test_table_operations_wrap_the_columns_of_their_helper(
	monkeypatch: pytest.MonkeyPatch,
	module: ModuleType,
	helper_name: str,
	operation: TableOperation,
) -> None:
	"""
	Check that each operation returns a new Table holding what its helper returns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the helper with a fake.
	module
		The module of the group of methods.
	helper_name
		The name of the helper the method calls.
	operation
		A function calling the method.
	"""
	monkeypatch.setattr(module, helper_name, give_fake_frame)
	table = Table._create(FRAME)

	new_table = operation(table)

	assert new_table is not table
	assert new_table.column_names == EXPECTED_FAKE_NAMES


def test_filter_keeps_the_rows_of_the_mask_and_numbers_them_from_zero(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check the kept prices and their row numbers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the mask builder with a fake.
	"""
	monkeypatch.setattr(table_selection, BUILD_FILTER_MASK_NAME, give_fake_mask)
	table = Table._create(FRAME)

	filtered_table = table.filter(ROW_FILTER)

	filtered_frame = filtered_table.to_pandas()
	price_column = filtered_frame["price"]
	prices = price_column.tolist()
	row_numbers = filtered_frame.index.tolist()
	assert prices == EXPECTED_FILTERED_PRICES
	assert row_numbers == EXPECTED_FILTERED_ROWS


def test_convert_replaces_the_column_with_its_conversion(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the converted column takes the place of the original one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the conversion with a fake.
	"""
	monkeypatch.setattr(table_columns, CONVERT_COLUMN_NAME, give_fake_column)
	table = Table._create(FRAME)

	converted_table = table.convert(Conversion(column="price", dtype=Type.TEXT))

	original_types = table.column_types
	assert converted_table.column_types == EXPECTED_CONVERTED_TYPES
	assert original_types == {"price": Type.FLOAT64}
