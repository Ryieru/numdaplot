"""
Unit tests of TableSelection, TableColumns, TableCalculation, TableLayout and TableMissing.

Each method hands the columns to a helper, faked here, and wraps the result in a new Table.

.. versionadded:: 0.1.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

from collections.abc import Callable
from dataclasses import dataclass
from types import ModuleType
from typing import Any

import numpy
import pandas
import pytest
from numpy.typing import NDArray

from numdaplot.arrays.array import Array
from numdaplot.conversions.table_conversion import TableConversion
from numdaplot.math_functions.square_root import SquareRoot
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
from numdaplot.tables.columns.name_change import NameChange
from numdaplot.tables.columns.new_column import NewColumn
from numdaplot.tables.columns.renaming import Renaming
from numdaplot.tables.columns.table_application import TableApplication
from numdaplot.tables.description.description import Description
from numdaplot.tables.duplicates.deduplication import Deduplication
from numdaplot.tables.filtering.condition import Condition
from numdaplot.tables.filtering.filter import Filter
from numdaplot.tables.missing.missing_count import MissingCount
from numdaplot.tables.missing.missing_drop import MissingDrop
from numdaplot.tables.pivot.pivot_table import PivotTable
from numdaplot.tables.sorting.sort_key import SortKey
from numdaplot.tables.sorting.table_sorting import TableSorting
from numdaplot.tables.table import Table
from numdaplot.tables.value_counts.value_count import ValueCount
from numdaplot.types.type import Type

FRAME = pandas.DataFrame({"price": [5.0, 12.0, 30.0]})
FAKE_FRAME = pandas.DataFrame({"result": [1.0]})
EXPECTED_FAKE_NAMES = ["result"]
FAKE_MASK = numpy.array([False, True, True])
EXPECTED_FILTERED_PRICES = [12.0, 30.0]
EXPECTED_FILTERED_ROWS = [0, 1]
ROW_FILTER = Filter(conditions=[Condition(rule=Greater(10))])
BUILD_FILTER_MASK_NAME = "build_filter_mask"
PRICE_MEAN = Calculation(column="price", function=Mean())
PRICE_PIVOT = PivotTable(rows=["city"], columns="day", calculation=PRICE_MEAN)
type TableOperation = Callable[[Table], Table]
FRAME_OPERATIONS = list[tuple[ModuleType, str, TableOperation]](
	[
		(table_selection, "take_region", lambda table: table.take(Region(rows=Index(0)))),
		(table_selection, "check_frame", lambda table: table.check(IsMissing())),
		(table_columns, "choose_frame_columns", lambda table: table.choose_columns(ColumnChoice(columns=["price"]))),
		(
			table_columns,
			"rename_frame_columns",
			lambda table: table.rename(Renaming(changes=[NameChange(old_name="price", new_name="cost")])),
		),
		(
			table_columns,
			"convert_frame_columns",
			lambda table: table.convert(TableConversion(columns=["price"], dtype=Type.TEXT)),
		),
		(
			table_columns,
			"apply_frame_columns",
			lambda table: table.apply(TableApplication(function=SquareRoot(), columns=["price"])),
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
		(table_calculation, "pivot_frame", lambda table: table.pivot_table(PRICE_PIVOT)),
		(table_calculation, "count_frame_values", lambda table: table.count_values(ValueCount(column="price"))),
		(table_layout, "sort_frame", lambda table: table.sort(TableSorting(keys=[SortKey(column="price")]))),
		(table_layout, "drop_duplicate_rows", lambda table: table.drop_duplicates(Deduplication())),
		(
			table_missing,
			"count_frame_missing",
			lambda table: table.count_missing(MissingCount(), axis=Axis.EACH_COLUMN),
		),
		(table_missing, "drop_frame_missing", lambda table: table.drop_missing(MissingDrop())),
	]
)


def give_fake_frame(frame: pandas.DataFrame, settings: object, *axis: object) -> pandas.DataFrame:
	"""
	Fake helper returning known columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of the Table, ignored.
	settings
		The settings of the operation, ignored.
	axis
		The axis given by the methods taking one, ignored.

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


@dataclass(frozen=True)
class DefaultSettingsCase:
	"""
	A Table method called without settings, and the settings its helper must receive.

	.. versionadded:: 0.1.0

	Parameters
	----------
	module
		The module of the group of methods.
	helper_name
		The name of the helper the method calls.
	operation
		A function calling the method without settings.
	expected_settings
		The default settings the helper must receive.
	"""

	module: ModuleType
	helper_name: str
	operation: TableOperation
	expected_settings: object


class SettingsRecorder:
	"""
	Fake helper keeping the settings it receives.

	.. versionadded:: 0.1.0
	"""

	def __init__(self) -> None:
		"""
		Start without settings.

		.. versionadded:: 0.1.0
		"""
		self.settings = list[object]()
		self.axes = list[object]()

	def record(self, frame: pandas.DataFrame, settings: object, *axis: object) -> pandas.DataFrame:
		"""
		Keep the settings and the axis, and return the fake columns.

		.. versionadded:: 0.1.0

		Parameters
		----------
		frame
			The columns, ignored.
		settings
			The settings received.
		axis
			The axis received, for the methods taking one.

		Returns
		-------
		pandas.DataFrame
			Always the fake columns.
		"""
		self.settings.append(settings)
		self.axes.extend(axis)

		return FAKE_FRAME


DEFAULT_SETTINGS_CASES = [
	DefaultSettingsCase(table_calculation, "describe_frame", lambda table: table.describe(), Description()),
	DefaultSettingsCase(table_layout, "drop_duplicate_rows", lambda table: table.drop_duplicates(), Deduplication()),
	DefaultSettingsCase(table_missing, "count_frame_missing", lambda table: table.count_missing(), MissingCount()),
	DefaultSettingsCase(table_missing, "drop_frame_missing", lambda table: table.drop_missing(), MissingDrop()),
]


@pytest.mark.parametrize("case", DEFAULT_SETTINGS_CASES)
def test_method_without_settings_uses_the_default_settings(
	monkeypatch: pytest.MonkeyPatch,
	case: DefaultSettingsCase,
) -> None:
	"""
	Check that a method called without settings hands the default settings to its helper.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the helper with a recorder.
	case
		The method, its helper and the expected default settings.
	"""
	recorder = SettingsRecorder()
	monkeypatch.setattr(case.module, case.helper_name, recorder.record)
	table = Table._create(FRAME)

	case.operation(table)

	assert recorder.settings == [case.expected_settings]


AXIS_CASES = list[tuple[str, TableOperation, Axis | None]](
	[
		("count_frame_missing", lambda table: table.count_missing(), None),
		("count_frame_missing", lambda table: table.count_missing(axis=Axis.EACH_ROW), Axis.EACH_ROW),
		("drop_frame_missing", lambda table: table.drop_missing(), Axis.EACH_ROW),
		("drop_frame_missing", lambda table: table.drop_missing(axis=Axis.EACH_COLUMN), Axis.EACH_COLUMN),
	]
)


@pytest.mark.parametrize(("helper_name", "operation", "expected_axis"), AXIS_CASES)
def test_missing_methods_hand_their_axis_to_their_helper(
	monkeypatch: pytest.MonkeyPatch,
	helper_name: str,
	operation: TableOperation,
	expected_axis: Axis | None,
) -> None:
	"""
	Check the axis count_missing and drop_missing give to their helper, by default and when given.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the helper with a recorder.
	helper_name
		The name of the helper.
	operation
		Calls the method.
	expected_axis
		The axis the helper must receive.
	"""
	recorder = SettingsRecorder()
	monkeypatch.setattr(table_missing, helper_name, recorder.record)
	table = Table._create(FRAME)

	operation(table)

	assert recorder.axes == [expected_axis]
