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
from numdaplot.data_types.type import Type
from numdaplot.errors.broadcast_warning import BroadcastWarning
from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.dimension_error import DimensionError
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.empty_array_error import EmptyArrayError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.errors.empty_text_error import EmptyTextError
from numdaplot.errors.empty_values_error import EmptyValuesError
from numdaplot.errors.file_exists_error import FileExistsError
from numdaplot.errors.file_not_found_error import FileNotFoundError
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.invalid_base_error import InvalidBaseError
from numdaplot.errors.invalid_bounds_error import InvalidBoundsError
from numdaplot.errors.invalid_column_name_error import InvalidColumnNameError
from numdaplot.errors.invalid_count_error import InvalidCountError
from numdaplot.errors.invalid_deviation_error import InvalidDeviationError
from numdaplot.errors.invalid_fraction_error import InvalidFractionError
from numdaplot.errors.invalid_position_error import InvalidPositionError
from numdaplot.errors.invalid_seed_error import InvalidSeedError
from numdaplot.errors.invalid_separator_error import InvalidSeparatorError
from numdaplot.errors.invalid_shape_error import InvalidShapeError
from numdaplot.errors.invalid_step_error import InvalidStepError
from numdaplot.errors.irregular_list_error import IrregularListError
from numdaplot.errors.missing_dependency_error import MissingDependencyError
from numdaplot.errors.missing_type_error import MissingTypeError
from numdaplot.errors.not_single_value_error import NotSingleValueError
from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.out_of_domain_error import OutOfDomainError
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.errors.shape_mismatch_error import ShapeMismatchError
from numdaplot.errors.unsupported_index_error import UnsupportedIndexError
from numdaplot.errors.unsupported_missing_error import UnsupportedMissingError
from numdaplot.errors.unsupported_operand_error import UnsupportedOperandError
from numdaplot.errors.unsupported_type_error import UnsupportedTypeError
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.ordering.missing_position import MissingPosition
from numdaplot.ordering.order import Order
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
from numdaplot.tables.preview.preview import Preview
from numdaplot.tables.preview.side import Side
from numdaplot.tables.sorting.sort_key import SortKey
from numdaplot.tables.sorting.sorting import Sorting
from numdaplot.tables.table import Table

__all__ = [
	"Absolute",
	"Aggregation",
	"Array",
	"ArraySorting",
	"Axis",
	"Between",
	"Bounds",
	"BroadcastWarning",
	"Calculation",
	"Case",
	"ColumnChoice",
	"ColumnMatch",
	"ColumnMode",
	"ColumnNotFoundError",
	"Condition",
	"Conflict",
	"Contains",
	"Conversion",
	"Cosine",
	"Count",
	"CountDistinct",
	"CsvOptions",
	"Deduplication",
	"Description",
	"DimensionError",
	"Distribution",
	"DuplicateColumnError",
	"EmptyArrayError",
	"EmptyListError",
	"EmptyTextError",
	"EmptyValuesError",
	"Encoding",
	"Equal",
	"Equality",
	"ExcelOptions",
	"Exponential",
	"FileExistsError",
	"FileNotFoundError",
	"Filter",
	"FilterMode",
	"Greater",
	"GreaterOrEqual",
	"IncompatibleTypesError",
	"Index",
	"InvalidBaseError",
	"InvalidBoundsError",
	"InvalidColumnNameError",
	"InvalidCountError",
	"InvalidDeviationError",
	"InvalidFractionError",
	"InvalidPositionError",
	"InvalidSeedError",
	"InvalidSeparatorError",
	"InvalidShapeError",
	"InvalidStepError",
	"IrregularListError",
	"IsIn",
	"IsMissing",
	"IsPresent",
	"JsonLayout",
	"JsonOptions",
	"Keep",
	"Less",
	"LessOrEqual",
	"Logarithm",
	"MathFunction",
	"Max",
	"Mean",
	"Measure",
	"Median",
	"Min",
	"MissingCount",
	"MissingDependencyError",
	"MissingDrop",
	"MissingMode",
	"MissingPosition",
	"MissingRatio",
	"MissingTypeError",
	"MostFrequent",
	"MostFrequentCount",
	"NewColumn",
	"Normal",
	"NotEqual",
	"NotSingleValueError",
	"NumdaplotError",
	"Order",
	"OutOfDomainError",
	"Preview",
	"Quantile",
	"RandomIntegers",
	"Range",
	"RatioComparison",
	"RefusedOperationError",
	"Region",
	"Renaming",
	"Replacement",
	"Round",
	"Rule",
	"SasOptions",
	"Shape",
	"ShapeMismatchError",
	"Side",
	"Sine",
	"SortKey",
	"Sorting",
	"Spacing",
	"SquareRoot",
	"StandardDeviation",
	"Statistic",
	"Sum",
	"Table",
	"Type",
	"TypeMatch",
	"Uniform",
	"UnsupportedIndexError",
	"UnsupportedMissingError",
	"UnsupportedOperandError",
	"UnsupportedTypeError",
	"ValueConversionError",
	"XptOptions",
]
