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
- Dates: arithmetic between dates, datetimes, durations and numbers on `Array`, time functions applied by
  `Array.apply` (`TimeFunction`, `DatePart`, `DatePeriod`, `DurationIn`, `ToDuration`, with the `DatePartUnit`,
  `PeriodUnit` and `DurationUnit` enums), date formats and time zones for `Table.convert` (`DateFormat` enum,
  `CustomDateFormat`, `TimeZone`, `TimeZoneChange` and the `TimeZoneMode` enum), and `Table.column_time_zones`.
- Plots: `plot_line`, `plot_bar`, `plot_scatter`, `plot_histogram`, `plot_box`, `plot_pie`, `plot_heatmap`,
  `plot_missing_by_column` and `plot_missing_map` return a `Plot`, shown with `Plot.show`, saved as a PNG, SVG
  or PDF image with `Plot.save` and turned into a matplotlib figure with `Plot.to_matplotlib`. `Plot.add_line`,
  `Plot.add_bar` and `Plot.add_scatter` draw other charts over a Plot, on its axis or on a second axis on the
  right with the `ValueAxis` enum.
- Figures: `Figure` places Plots on the cells of a `Layout` with `Figure.place` and `Cell`, and has `show`,
  `save` and `to_matplotlib` like a Plot.
- Plot settings: `Chart`, `LineChart`, `BarChart`, `ScatterChart`, `HistogramChart`, `BoxChart`, `PieChart`,
  `HeatmapChart`, `MissingChart`, `BinCount`, `BinWidth`, `Style`, `Size`, `CustomColor`, `ImageOptions`, and the
  `Color`, `LineType`, `MarkerShape`, `Orientation`, `BarLayout`, `Outliers`, `Percentages`, `ColorScale`,
  `CellValues`, `LegendPosition`, `GridLines` and `SizeUnit` enums.
- Plot errors and warning: `ConflictingSettingsError`, `DuplicateLabelError`, `EmptyTotalError`,
  `InvalidBinWidthError`, `InvalidChartDataError`, `InvalidColorCountError`, `InvalidColorError`,
  `InvalidResolutionError`, `InvalidRotationError`, `InvalidSizeError`, `MissingValueError`, `RefusedSettingError`, `UnsupportedDataError`,
  `UnsupportedImageFormatError`, `IncompatibleChartsError`, `OccupiedCellError`, `CellOutOfRangeError` and
  `ReadabilityWarning`.
- Date errors: `InvalidConversionError`, `InvalidDateFormatError`, `InvalidTimeZoneChangeError`,
  `TimeZoneMismatchError` and `UnknownTimeZoneError`.
- `Table`: named columns of one type each, read with `Table.from_csv`, `Table.from_json`, `Table.from_excel`,
  `Table.from_parquet`, `Table.from_stata`, `Table.from_sas`, `Table.from_xpt`, `Table.from_pandas` and
  `Table.from_arrays`; written with `Table.to_csv`, `Table.to_json`, `Table.to_excel`, `Table.to_parquet` and
  `Table.to_stata`; changed with `Table.filter`, `Table.take`, `Table.choose_columns`, `Table.rename`,
  `Table.convert`, `Table.add_column`, `Table.aggregate`, `Table.describe`, `Table.sort`,
  `Table.drop_duplicates` and `Table.drop_missing`; read with `Table.column`, `Table.check`,
  `Table.count_missing`, `Table.to_value`, `Table.to_pandas`, `Table.is_equal`, `Table.row_count`,
  `Table.column_names`, `Table.column_types`, `Table.preview`, `Table.preview_missing` and `print`.
- `Array`, `Table` and `Plot`, and the base classes `Rule`, `Statistic`, `MathFunction`, `TimeFunction`,
  `Distribution` and `Chart`, refuse their constructor with `RefusedOperationError`, which names what to use instead.
  The plot functions and `Plot.add_*` refuse a chart of another class the same way.
- Settings that work as they are may be omitted: `Array.sort`, `Table.preview`, `Table.describe`,
  `Table.drop_duplicates`, `Table.drop_missing` and `Table.count_missing` use their default settings, and the plot
  functions and `Plot.add_*`, except `plot_pie`, their default chart.
- Table settings: `CsvOptions`, `JsonOptions`, `ExcelOptions`, `SasOptions`, `XptOptions`, `Filter`, `Condition`,
  `Aggregation`, `Calculation`, `Description`, `ColumnChoice`, `Renaming`, `Conversion`, `NewColumn`, `Sorting`,
  `SortKey`, `Deduplication`, `Preview`, `MissingCount`, `MissingDrop`, `MissingRatio`, and the `Encoding`,
  `JsonLayout`, `Conflict`, `FilterMode`, `ColumnMatch`, `ColumnMode`, `Keep`, `Side`, `MissingMode`,
  `RatioComparison` and `Measure` enums. `Equality` compares two Tables as well as two Arrays.
- Table errors: `ColumnNotFoundError`, `DuplicateColumnError`, `EmptyListError`, `FileExistsError`,
  `FileNotFoundError`, `InvalidColumnNameError`, `InvalidSeparatorError`, `InvalidSheetNameError`,
  `MissingDependencyError` and `UnsupportedIndexError`. `FileNotFoundError` and `FileExistsError` are also the
  Python errors of the same name.
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
- Errors: `NumdaplotError`, `EmptyRegionError`, `EmptyTextError`, `EmptyValuesError`, `InvalidBoundsError`,
  `InvalidFractionError`, `InvalidSettingTypeError`, `InvalidStepError`, `UnsupportedTypeError`, and the
  `BroadcastWarning` warning.
