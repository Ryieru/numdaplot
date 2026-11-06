"""
numdaplot: a simpler, explicit API over numpy, pandas and matplotlib.

Import it as ``ndp``; every public name is available directly under it.

.. versionadded:: 0.1.0

Examples
--------
>>> import numdaplot as ndp
>>> prices = ndp.Array.from_list([12.5, None, 30.0])
>>> prices.select(ndp.Greater(20))
Array([30.], dtype=FLOAT64)
>>> prices.compute(ndp.Mean()).to_value()
21.25
"""

from numdaplot.arrays.array import Array
from numdaplot.arrays.array_sorting import ArraySorting
from numdaplot.arrays.creation.distribution import Distribution
from numdaplot.arrays.creation.normal import Normal
from numdaplot.arrays.creation.random_integers import RandomIntegers
from numdaplot.arrays.creation.spacing import Spacing
from numdaplot.arrays.creation.uniform import Uniform
from numdaplot.arrays.equality import Equality
from numdaplot.arrays.math_functions.absolute import Absolute
from numdaplot.arrays.math_functions.cosine import Cosine
from numdaplot.arrays.math_functions.exponential import Exponential
from numdaplot.arrays.math_functions.logarithm import Logarithm
from numdaplot.arrays.math_functions.math_function import MathFunction
from numdaplot.arrays.math_functions.round import Round
from numdaplot.arrays.math_functions.sine import Sine
from numdaplot.arrays.math_functions.square_root import SquareRoot
from numdaplot.arrays.replacement import Replacement
from numdaplot.arrays.shape import Shape
from numdaplot.arrays.type_match import TypeMatch
from numdaplot.data_types.library import Library
from numdaplot.data_types.type import Type
from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.dates.date_format import DateFormat
from numdaplot.dates.date_part import DatePart
from numdaplot.dates.date_part_unit import DatePartUnit
from numdaplot.dates.date_period import DatePeriod
from numdaplot.dates.duration_in import DurationIn
from numdaplot.dates.duration_unit import DurationUnit
from numdaplot.dates.period_unit import PeriodUnit
from numdaplot.dates.time_function import TimeFunction
from numdaplot.dates.time_zone import TimeZone
from numdaplot.dates.time_zone_change import TimeZoneChange
from numdaplot.dates.time_zone_mode import TimeZoneMode
from numdaplot.dates.to_duration import ToDuration
from numdaplot.errors.broadcast_warning import BroadcastWarning
from numdaplot.errors.calculation_warning import CalculationWarning
from numdaplot.errors.cell_out_of_range_error import CellOutOfRangeError
from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.conflicting_settings_error import ConflictingSettingsError
from numdaplot.errors.dimension_error import DimensionError
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.duplicate_label_error import DuplicateLabelError
from numdaplot.errors.duplicate_statistic_error import DuplicateStatisticError
from numdaplot.errors.empty_array_error import EmptyArrayError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.errors.empty_region_error import EmptyRegionError
from numdaplot.errors.empty_text_error import EmptyTextError
from numdaplot.errors.empty_total_error import EmptyTotalError
from numdaplot.errors.empty_values_error import EmptyValuesError
from numdaplot.errors.file_access_error import FileAccessError
from numdaplot.errors.file_exists_error import FileExistsError
from numdaplot.errors.file_not_found_error import FileNotFoundError
from numdaplot.errors.incompatible_charts_error import IncompatibleChartsError
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.integer_overflow_error import IntegerOverflowError
from numdaplot.errors.invalid_base_error import InvalidBaseError
from numdaplot.errors.invalid_bin_width_error import InvalidBinWidthError
from numdaplot.errors.invalid_bounds_error import InvalidBoundsError
from numdaplot.errors.invalid_chart_data_error import InvalidChartDataError
from numdaplot.errors.invalid_color_count_error import InvalidColorCountError
from numdaplot.errors.invalid_color_error import InvalidColorError
from numdaplot.errors.invalid_column_name_error import InvalidColumnNameError
from numdaplot.errors.invalid_conversion_error import InvalidConversionError
from numdaplot.errors.invalid_count_error import InvalidCountError
from numdaplot.errors.invalid_date_format_error import InvalidDateFormatError
from numdaplot.errors.invalid_deviation_error import InvalidDeviationError
from numdaplot.errors.invalid_fraction_error import InvalidFractionError
from numdaplot.errors.invalid_opacity_error import InvalidOpacityError
from numdaplot.errors.invalid_point_size_error import InvalidPointSizeError
from numdaplot.errors.invalid_position_error import InvalidPositionError
from numdaplot.errors.invalid_resolution_error import InvalidResolutionError
from numdaplot.errors.invalid_rotation_error import InvalidRotationError
from numdaplot.errors.invalid_seed_error import InvalidSeedError
from numdaplot.errors.invalid_separator_error import InvalidSeparatorError
from numdaplot.errors.invalid_shape_error import InvalidShapeError
from numdaplot.errors.invalid_sheet_name_error import InvalidSheetNameError
from numdaplot.errors.invalid_size_error import InvalidSizeError
from numdaplot.errors.invalid_step_error import InvalidStepError
from numdaplot.errors.invalid_time_zone_change_error import InvalidTimeZoneChangeError
from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.errors.irregular_list_error import IrregularListError
from numdaplot.errors.missing_dependency_error import MissingDependencyError
from numdaplot.errors.missing_type_error import MissingTypeError
from numdaplot.errors.missing_value_error import MissingValueError
from numdaplot.errors.not_single_value_error import NotSingleValueError
from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.occupied_cell_error import OccupiedCellError
from numdaplot.errors.out_of_domain_error import OutOfDomainError
from numdaplot.errors.readability_warning import ReadabilityWarning
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.errors.shape_mismatch_error import ShapeMismatchError
from numdaplot.errors.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.errors.unknown_time_zone_error import UnknownTimeZoneError
from numdaplot.errors.unsupported_image_format_error import UnsupportedImageFormatError
from numdaplot.errors.unsupported_index_error import UnsupportedIndexError
from numdaplot.errors.unsupported_missing_error import UnsupportedMissingError
from numdaplot.errors.unsupported_type_error import UnsupportedTypeError
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.ordering.missing_position import MissingPosition
from numdaplot.ordering.order import Order
from numdaplot.package_version import find_package_version
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.bar_layout import BarLayout
from numdaplot.plots.charts.bin_count import BinCount
from numdaplot.plots.charts.bin_width import BinWidth
from numdaplot.plots.charts.box_chart import BoxChart
from numdaplot.plots.charts.cell_values import CellValues
from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.color_scale import ColorScale
from numdaplot.plots.charts.heatmap_chart import HeatmapChart
from numdaplot.plots.charts.histogram_chart import HistogramChart
from numdaplot.plots.charts.line_chart import LineChart
from numdaplot.plots.charts.line_type import LineType
from numdaplot.plots.charts.marker_shape import MarkerShape
from numdaplot.plots.charts.missing_chart import MissingChart
from numdaplot.plots.charts.orientation import Orientation
from numdaplot.plots.charts.outliers import Outliers
from numdaplot.plots.charts.percentages import Percentages
from numdaplot.plots.charts.pie_chart import PieChart
from numdaplot.plots.charts.scatter_chart import ScatterChart
from numdaplot.plots.charts.value_axis import ValueAxis
from numdaplot.plots.figure.cell import Cell
from numdaplot.plots.figure.figure import Figure
from numdaplot.plots.figure.figure_style import FigureStyle
from numdaplot.plots.figure.layout import Layout
from numdaplot.plots.plot import Plot
from numdaplot.plots.plot_bar import plot_bar
from numdaplot.plots.plot_box import plot_box
from numdaplot.plots.plot_heatmap import plot_heatmap
from numdaplot.plots.plot_histogram import plot_histogram
from numdaplot.plots.plot_line import plot_line
from numdaplot.plots.plot_missing_by_column import plot_missing_by_column
from numdaplot.plots.plot_missing_map import plot_missing_map
from numdaplot.plots.plot_pie import plot_pie
from numdaplot.plots.plot_scatter import plot_scatter
from numdaplot.plots.style.color import Color
from numdaplot.plots.style.custom_color import CustomColor
from numdaplot.plots.style.grid_lines import GridLines
from numdaplot.plots.style.image_options import ImageOptions
from numdaplot.plots.style.legend_position import LegendPosition
from numdaplot.plots.style.plot_style import PlotStyle
from numdaplot.plots.style.size import Size
from numdaplot.plots.style.size_unit import SizeUnit
from numdaplot.positions.axis import Axis
from numdaplot.positions.index import Index
from numdaplot.positions.range import Range
from numdaplot.positions.region import Region
from numdaplot.ratios.measure import Measure
from numdaplot.rules.between import Between
from numdaplot.rules.bounds import Bounds
from numdaplot.rules.case import Case
from numdaplot.rules.contains import Contains
from numdaplot.rules.equal import Equal
from numdaplot.rules.greater import Greater
from numdaplot.rules.greater_or_equal import GreaterOrEqual
from numdaplot.rules.is_in import IsIn
from numdaplot.rules.is_missing import IsMissing
from numdaplot.rules.is_present import IsPresent
from numdaplot.rules.less import Less
from numdaplot.rules.less_or_equal import LessOrEqual
from numdaplot.rules.not_equal import NotEqual
from numdaplot.rules.rule import Rule
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
from numdaplot.statistics.standard_deviation import StandardDeviation
from numdaplot.statistics.statistic import Statistic
from numdaplot.statistics.sum import Sum
from numdaplot.tables.aggregation.aggregation import Aggregation
from numdaplot.tables.aggregation.calculation import Calculation
from numdaplot.tables.columns.column_choice import ColumnChoice
from numdaplot.tables.columns.column_mode import ColumnMode
from numdaplot.tables.columns.conversion import Conversion
from numdaplot.tables.columns.name_change import NameChange
from numdaplot.tables.columns.new_column import NewColumn
from numdaplot.tables.columns.renaming import Renaming
from numdaplot.tables.conflict import Conflict
from numdaplot.tables.description.description import Description
from numdaplot.tables.duplicates.deduplication import Deduplication
from numdaplot.tables.duplicates.keep import Keep
from numdaplot.tables.files.csv_options import CsvOptions
from numdaplot.tables.files.encoding import Encoding
from numdaplot.tables.files.excel_options import ExcelOptions
from numdaplot.tables.files.json_layout import JsonLayout
from numdaplot.tables.files.json_options import JsonOptions
from numdaplot.tables.files.sas_options import SasOptions
from numdaplot.tables.files.xpt_options import XptOptions
from numdaplot.tables.filtering.column_match import ColumnMatch
from numdaplot.tables.filtering.condition import Condition
from numdaplot.tables.filtering.filter import Filter
from numdaplot.tables.filtering.filter_mode import FilterMode
from numdaplot.tables.missing.missing_count import MissingCount
from numdaplot.tables.missing.missing_drop import MissingDrop
from numdaplot.tables.missing.missing_mode import MissingMode
from numdaplot.tables.missing.missing_ratio import MissingRatio
from numdaplot.tables.missing.ratio_comparison import RatioComparison
from numdaplot.tables.pivot.pivot_table import PivotTable
from numdaplot.tables.preview.preview import Preview
from numdaplot.tables.preview.shown_columns import ShownColumns
from numdaplot.tables.preview.side import Side
from numdaplot.tables.sorting.sort_key import SortKey
from numdaplot.tables.sorting.sorting import Sorting
from numdaplot.tables.table import Table

__version__ = find_package_version()

__all__ = [
	"Absolute",
	"Aggregation",
	"Array",
	"ArraySorting",
	"Axis",
	"BarChart",
	"BarLayout",
	"Between",
	"BinCount",
	"BinWidth",
	"Bounds",
	"BoxChart",
	"BroadcastWarning",
	"CalculationWarning",
	"Calculation",
	"Case",
	"Cell",
	"CellOutOfRangeError",
	"CellValues",
	"Chart",
	"Color",
	"ColorScale",
	"ColumnChoice",
	"ColumnMatch",
	"ColumnMode",
	"ColumnNotFoundError",
	"Condition",
	"Conflict",
	"ConflictingSettingsError",
	"Contains",
	"Conversion",
	"Cosine",
	"Count",
	"CountDistinct",
	"CountedMissing",
	"CsvOptions",
	"CustomColor",
	"CustomDateFormat",
	"DateFormat",
	"DatePart",
	"DatePartUnit",
	"DatePeriod",
	"Deduplication",
	"Description",
	"DimensionError",
	"Distribution",
	"DuplicateColumnError",
	"DuplicateLabelError",
	"DuplicateStatisticError",
	"DurationIn",
	"DurationUnit",
	"EmptyArrayError",
	"EmptyListError",
	"EmptyRegionError",
	"EmptyTextError",
	"EmptyTotalError",
	"EmptyValuesError",
	"Encoding",
	"Equal",
	"Equality",
	"ExcelOptions",
	"Exponential",
	"Figure",
	"FigureStyle",
	"FileAccessError",
	"FileExistsError",
	"FileNotFoundError",
	"Filter",
	"FilterMode",
	"Greater",
	"GreaterOrEqual",
	"GridLines",
	"HeatmapChart",
	"HistogramChart",
	"ImageOptions",
	"IncompatibleChartsError",
	"IncompatibleTypesError",
	"IntegerOverflowError",
	"Index",
	"InvalidBaseError",
	"InvalidBinWidthError",
	"InvalidBoundsError",
	"InvalidChartDataError",
	"InvalidColorCountError",
	"InvalidColorError",
	"InvalidColumnNameError",
	"InvalidConversionError",
	"InvalidCountError",
	"InvalidDateFormatError",
	"InvalidDeviationError",
	"InvalidFractionError",
	"InvalidOpacityError",
	"InvalidPointSizeError",
	"InvalidPositionError",
	"InvalidResolutionError",
	"InvalidRotationError",
	"InvalidSeedError",
	"InvalidSeparatorError",
	"InvalidShapeError",
	"InvalidSheetNameError",
	"InvalidSizeError",
	"InvalidStepError",
	"InvalidTimeZoneChangeError",
	"InvalidTypeError",
	"IrregularListError",
	"IsIn",
	"IsMissing",
	"IsPresent",
	"JsonLayout",
	"JsonOptions",
	"Keep",
	"Layout",
	"LegendPosition",
	"Less",
	"LessOrEqual",
	"Library",
	"LineChart",
	"LineType",
	"Logarithm",
	"MarkerShape",
	"MathFunction",
	"Max",
	"Mean",
	"Measure",
	"Median",
	"Min",
	"MissingChart",
	"MissingCount",
	"MissingDependencyError",
	"MissingDrop",
	"MissingMode",
	"MissingPosition",
	"MissingRatio",
	"MissingTypeError",
	"MissingValueError",
	"MostFrequent",
	"MostFrequentCount",
	"NameChange",
	"NewColumn",
	"Normal",
	"NotEqual",
	"NotSingleValueError",
	"NumdaplotError",
	"OccupiedCellError",
	"Order",
	"Orientation",
	"OutOfDomainError",
	"Outliers",
	"Percentages",
	"PeriodUnit",
	"PieChart",
	"PivotTable",
	"Plot",
	"PlotStyle",
	"Preview",
	"Quantile",
	"RandomIntegers",
	"Range",
	"RatioComparison",
	"ReadabilityWarning",
	"RefusedOperationError",
	"RefusedSettingError",
	"Region",
	"Renaming",
	"Replacement",
	"Round",
	"Rule",
	"SasOptions",
	"ScatterChart",
	"Shape",
	"ShapeMismatchError",
	"ShownColumns",
	"Side",
	"Sine",
	"Size",
	"SizeUnit",
	"SortKey",
	"Sorting",
	"Spacing",
	"SquareRoot",
	"StandardDeviation",
	"Statistic",
	"Sum",
	"Table",
	"TimeFunction",
	"TimeZone",
	"TimeZoneChange",
	"TimeZoneMismatchError",
	"TimeZoneMode",
	"ToDuration",
	"Type",
	"TypeMatch",
	"Uniform",
	"UnknownTimeZoneError",
	"UnsupportedImageFormatError",
	"UnsupportedIndexError",
	"UnsupportedMissingError",
	"UnsupportedTypeError",
	"ValueAxis",
	"ValueConversionError",
	"XptOptions",
	"plot_bar",
	"plot_box",
	"plot_heatmap",
	"plot_histogram",
	"plot_line",
	"plot_missing_by_column",
	"plot_missing_map",
	"plot_pie",
	"plot_scatter",
]
