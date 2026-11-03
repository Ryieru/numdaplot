# Changelog

All notable changes to numdaplot are listed in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and numdaplot follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `Array`: values of one type in one or several dimensions, created with `from_list`, `from_numpy`,
  `filled`, `from_range`, `from_spacing` and `random`; combined with `+`, `-`, `*`, `/`, `//`, `%`, `**`
  and, for booleans, `&`, `|`, `~`; read with `select`, `check`, `take`, `replace`, `compute`, `apply`,
  `reshape`, `transpose`, `flatten`, `sort`, `unique`, `to_list`, `to_value`, `to_numpy` and `is_equal`.
- Array settings: `Shape`, `Spacing`, `ArraySorting`, `Replacement`, `Equality` and the `TypeMatch` enum.
- `Table`: named columns of one type each, read with `from_csv`, `from_json`, `from_excel`, `from_parquet`,
  `from_stata`, `from_sas`, `from_xpt`, `from_pandas` and `from_arrays`; written with `to_csv`, `to_json`,
  `to_excel`, `to_parquet` and `to_stata`; changed with `filter`, `take`, `choose_columns`, `rename`, `convert`,
  `add_column`, `aggregate`, `describe`, `sort` and `drop_duplicates`; read with `column`, `to_value`,
  `to_pandas`, `is_equal`, `row_count`, `column_names`, `column_types`, `preview` and `print`.
- Table settings: `CsvOptions`, `JsonOptions`, `ExcelOptions`, `SasOptions`, `XptOptions`, `Filter`, `Condition`,
  `Aggregation`, `Calculation`, `Description`, `ColumnChoice`, `Renaming`, `Conversion`, `NewColumn`, `Sorting`,
  `SortKey`, `Deduplication`, `Preview`, and the `Encoding`, `JsonLayout`, `Conflict`, `FilterMode`,
  `ColumnMatch`, `ColumnMode`, `Keep` and `Side` enums. `Equality` compares two Tables as well as two Arrays.
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
