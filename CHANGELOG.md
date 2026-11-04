# Changelog

All notable changes to numdaplot are listed in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and numdaplot follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `Array`: values of one type in one or several dimensions, created with `Array.from_list`, `Array.from_numpy`,
  `Array.filled`, `Array.from_range`, `Array.from_spacing` and `Array.random`; combined with `+`, `-`, `*`, `/`,
  `//`, `%`, `**` and, for booleans, `&`, `|`, `~`; read with `Array.select`, `Array.check`, `Array.take`,
  `Array.replace`, `Array.compute`, `Array.apply`, `Array.reshape`, `Array.transpose`, `Array.flatten`,
  `Array.sort`, `Array.unique`, `Array.to_list`, `Array.to_value`, `Array.to_numpy` and `Array.is_equal`.
- Array settings: `Shape`, `Spacing`, `ArraySorting`, `Replacement`, `Equality` and the `TypeMatch` enum.
- `Table`: named columns of one type each, read with `Table.from_csv`, `Table.from_json`, `Table.from_excel`,
  `Table.from_parquet`, `Table.from_stata`, `Table.from_sas`, `Table.from_xpt`, `Table.from_pandas` and
  `Table.from_arrays`; written with `Table.to_csv`, `Table.to_json`, `Table.to_excel`, `Table.to_parquet` and
  `Table.to_stata`; changed with `Table.filter`, `Table.take`, `Table.choose_columns`, `Table.rename`,
  `Table.convert`, `Table.add_column`, `Table.aggregate`, `Table.describe`, `Table.sort`,
  `Table.drop_duplicates` and `Table.drop_missing`; read with `Table.column`, `Table.check`,
  `Table.count_missing`, `Table.to_value`, `Table.to_pandas`, `Table.is_equal`, `Table.row_count`,
  `Table.column_names`, `Table.column_types`, `Table.preview`, `Table.preview_missing` and `print`.
- Table settings: `CsvOptions`, `JsonOptions`, `ExcelOptions`, `SasOptions`, `XptOptions`, `Filter`, `Condition`,
  `Aggregation`, `Calculation`, `Description`, `ColumnChoice`, `Renaming`, `Conversion`, `NewColumn`, `Sorting`,
  `SortKey`, `Deduplication`, `Preview`, `MissingCount`, `MissingDrop`, `MissingRatio`, and the `Encoding`,
  `JsonLayout`, `Conflict`, `FilterMode`, `ColumnMatch`, `ColumnMode`, `Keep`, `Side`, `MissingMode`,
  `RatioComparison` and `Measure` enums. `Equality` compares two Tables as well as two Arrays.
- Table errors: `ColumnNotFoundError`, `DuplicateColumnError`, `EmptyListError`, `FileExistsError`,
  `FileNotFoundError`, `InvalidColumnNameError`, `InvalidSeparatorError`, `MissingDependencyError` and
  `UnsupportedIndexError`. `FileNotFoundError` and `FileExistsError` are also the Python errors of the same name.
- Distributions: `Distribution`, `Uniform`, `Normal`, `RandomIntegers`.
- Math functions: `MathFunction`, `SquareRoot`, `Exponential`, `Logarithm`, `Absolute`, `Round`, `Sine`, `Cosine`.
- Array errors: `DimensionError`, `EmptyArrayError`, `IncompatibleTypesError`, `InvalidBaseError`,
  `InvalidCountError`, `InvalidDeviationError`, `InvalidPositionError`, `InvalidSeedError`,
  `InvalidShapeError`, `IrregularListError`, `MissingTypeError`, `NotSingleValueError`, `OutOfDomainError`,
  `RefusedOperationError`, `ShapeMismatchError`, `UnsupportedMissingError`, `UnsupportedOperandError`,
  `ValueConversionError`.
- `Type` enum of value types and its conversion to numpy and pandas dtypes.
- Rules: `Equal`, `NotEqual`, `Greater`, `GreaterOrEqual`, `Less`, `LessOrEqual`, `Between`, `IsIn`,
  `Contains`, `IsMissing`, `IsPresent`, with the `Bounds` and `Case` enums.
- Statistics: `Sum`, `Mean`, `Median`, `Min`, `Max`, `Count`, `CountDistinct`, `StandardDeviation`,
  `Quantile`, `MostFrequent`, `MostFrequentCount`.
- Positions: `Region`, `Index`, `Range` and the `Axis` enum.
- Sort settings: `Order` and `MissingPosition` enums.
- Errors: `NumdaplotError`, `EmptyTextError`, `EmptyValuesError`, `InvalidBoundsError`,
  `InvalidFractionError`, `InvalidStepError`, `UnsupportedTypeError`, and the `BroadcastWarning` warning.
