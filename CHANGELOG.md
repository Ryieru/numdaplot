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
