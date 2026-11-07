# Changelog

All notable changes to numdaplot are listed in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and numdaplot follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `numdaplot.__version__` gives the version of the installed package.
- `dir(numdaplot)` and the completion of notebooks show only the public names and `__version__`.
- `Array`: values of one type in one or several dimensions, created with `Array.from_list`, `Array.from_numpy`,
  `Array.filled`, `Array.from_range`, `Array.from_spacing`, `Array.from_date_parts` and `Array.random`; combined with
  `+`, `-`, `*`, `/`, `//`, `%`, `**` and, for booleans, `&`, `|`, `~`; read with `Array.select`, `Array.check`,
  `Array.take`, `Array.replace`, `Array.compute`, `Array.apply`, `Array.reshape`, `Array.transpose`, `Array.flatten`,
  `Array.sort`, `Array.unique`, `Array.to_list`, `Array.to_value`, `Array.to_numpy` and `Array.is_equal`.
- `Array.from_date_parts(DateParts(year, month, day))` builds a `DATE` Array from three Arrays of whole numbers, such
  as the day, month and year columns of a file, a date being missing where a part is missing; `ValueConversionError`
  names a part that is not whole or a year, month and day that form no date.
- Array settings: `Shape`, `Spacing`, `ArraySorting`, `Replacement`, `Equality` and the `TypeMatch` enum.
- Dates: arithmetic between dates, datetimes, durations and numbers on `Array`, time functions applied by
  `Array.apply` (`TimeFunction`, `DatePart`, `DatePeriod`, `DurationIn`, `ToDuration`, with the `DatePartUnit`,
  `PeriodUnit` and `DurationUnit` enums), date formats and time zones for `Table.convert` (`DateFormat` enum,
  `CustomDateFormat`, `TimeZone`, `TimeZoneChange` and the `TimeZoneMode` enum), and `Table.column_time_zones`.
- Plots: `Plot.line`, `Plot.bar`, `Plot.scatter`, `Plot.histogram`, `Plot.box`, `Plot.pie`, `Plot.heatmap`,
  `Plot.missing_by_column` and `Plot.missing_map` create a `Plot`, shown with `Plot.show`, saved as a PNG, SVG
  or PDF image with `Plot.save` and turned into a matplotlib figure with `Plot.to_matplotlib`. `Plot.add_line`,
  `Plot.add_bar` and `Plot.add_scatter` draw other charts over a Plot, on its axis or on a second axis on the
  right with the `ValueAxis` enum.
- Plots of missing values: `Plot.missing_by_column` writes the count and the share of the rows above each bar, and
  `Plot.missing_map` keeps a mark for every missing value of a long Table, with its total in a legend past the axes.
- `PlotStyle(renaming=Renaming(...))` shows columns under other names in the legend, the labels of boxes, heatmaps
  and missing value charts and the default title and axis labels, on every chart of a Plot, without renaming the
  Table; the columns of an Array are named `"0"`, `"1"`...
- Plot titles and axis labels are written by default: the title is the `y` label by the `x` label, such as
  `sales by month`, and `PlotStyle` replaces them or removes them with an empty text.
- Plots with many text labels, such as bars, heatmaps and boxes, only create the labels that fit, so they stay fast
  on long Tables.
- `Plot.heatmap` shows the mean of the cells in each band when they do not fit in the image, with a
  `ReadabilityWarning`, instead of leaving most of them out.
- Figures: `Figure` places Plots on the cells of a `Layout` with `Figure.place` and `Cell`, takes its title and its
  size from a `FigureStyle`, and has `show`, `save` and `to_matplotlib` like a Plot.
- Plot settings: `Chart`, `LineChart`, `BarChart`, `ScatterChart`, `HistogramChart`, `BoxChart`, `PieChart`,
  `HeatmapChart`, `MissingChart`, `BinCount`, `BinWidth`, `PlotStyle`, `Size`, `CustomColor`, `ImageOptions`, and the
  `Color`, `LineType`, `MarkerShape`, `Orientation`, `BarLayout`, `Outliers`, `Percentages`, `ColorScale`,
  `CellValues`, `LegendPosition`, `GridLines` and `SizeUnit` enums.
- Plots: the labels of an axis without enough room are left out, one out of as many as needed from the first one,
  with a `ReadabilityWarning` when they may be texts.
- Plot errors and warning: `ConflictingSettingsError`, `DuplicateLabelError`, `EmptyTotalError`,
  `InvalidBinWidthError`, `InvalidChartDataError`, `InvalidColorCountError`, `InvalidColorError`,
  `InvalidOpacityError`, `InvalidPointSizeError`, `InvalidResolutionError`, `InvalidRotationError`,
  `InvalidSizeError`, `MissingValueError`, `RefusedSettingError`,
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
  `Table.column_count`, `Table.column_names`, `Table.column_types`, `Table.preview`, `Table.preview_missing`
  and `print`.
- `Table.from_csv` gives each column the type of all its values, even when pandas reads a long file in blocks: a
  column mixing numbers and texts keeps every text as written, such as `01`, without the pandas `DtypeWarning`.
- `Array`, `Table` and `Plot`, and the base classes `Rule`, `Statistic`, `MathFunction`, `TimeFunction`,
  `Distribution` and `Chart`, refuse their constructor with `RefusedOperationError`, which names what to use instead.
  Settings, methods and arithmetic operators check their values against their annotations and raise
  `InvalidTypeError`, which names what they accept.
- Settings that work as they are may be omitted: `Array.sort`, `Table.preview`, `Table.describe`,
  `Table.drop_duplicates`, `Table.drop_missing` and `Table.count_missing` use their default settings, and the Plot
  creation methods and `Plot.add_*`, except `Plot.pie`, their default chart.
- `Table.convert` converts booleans to numbers, 1 for `True` and 0 for `False`, and numbers to booleans, only 0 and
  1 by default or every number but 0 as `True` with `BooleanRule.NONZERO_TRUE`.
- File settings, separate for reading and writing so that each setting only exists where it applies:
  `CsvReadOptions`, `CsvWriteOptions`, `JsonReadOptions`, `JsonWriteOptions`, `ExcelReadOptions`,
  `ExcelWriteOptions`, `SasReadOptions`, `XptReadOptions`, `ParquetReadOptions` and `StataReadOptions`.
- Every file reading and `Table.from_pandas` remove the spaces, tabs and line breaks at the start and the end of each
  column name, unless `ColumnNames.KEPT` is given; two names that become the same raise `DuplicateColumnError`.
- `CsvReadOptions` and `ExcelReadOptions` take `missing_texts`, the texts read as missing values, which replace the 19
  texts pandas reads as missing by default; an Excel column named like one of them, such as `NA`, keeps its name.
- Table settings: `Filter`, `Condition`,
  `Aggregation`, `Calculation`, `PivotTable`, `Description`, `ColumnChoice`, `Renaming`, `NameChange`, `Conversion`, `NewColumn`,
  `Sorting`, `SortKey`, `Deduplication`, `Preview`, `MissingCount`, `MissingDrop`, `MissingRatio`, and the `BooleanRule`, `Encoding`,
  `JsonLayout`, `Conflict`, `FilterMode`, `ColumnMatch`, `ColumnMode`, `Keep`, `Side`, `ShownColumns`, `MissingMode`,
  `RatioComparison` and `Measure` enums. `Equality` compares two Tables as well as two Arrays.
- Table errors: `ColumnNotFoundError`, `DuplicateColumnError`, `DuplicateStatisticError`, `EmptyListError`,
  `FileAccessError`, `FileExistsError`, `FileNotFoundError`, `InvalidColumnNameError`, `InvalidSeparatorError`,
  `InvalidSheetNameError`, `MissingDependencyError` and `UnsupportedIndexError`. `FileNotFoundError` and
  `FileExistsError` are also the Python errors of the same name, and `FileAccessError` is also an `OSError`.
- Distributions: `Distribution`, `Uniform`, `Normal`, `RandomIntegers`.
- Number brackets: `Conversion(dtype=Type.CATEGORY, format=Brackets(limits, bounds, labels, first, last, others))`
  cuts a number column into categories kept in the order of the brackets, named after the values they hold, such as
  `0 to 9` or `65 or more`, with the `BracketEnd` enum and the `InvalidLimitsError` and `InvalidLabelCountError`
  errors; `UnmatchedValueError` also names a value in no bracket.
- Value mapping: `Array.apply(ValueMapping(changes=[ValueChange(old_value, new_value)], others=Unmatched.ERROR))`
  replaces listed values by new ones, such as codes by labels, with `DuplicateValueError` for an old value given twice
  and `UnmatchedValueError` for a value without new value; `Unmatched.MISSING` makes those values missing.
- Math functions: `MathFunction`, `SquareRoot`, `Exponential`, `Logarithm`, `Absolute`, `Round`, `Sine`, `Cosine`.
- Array errors: `DimensionError`, `EmptyArrayError`, `IncompatibleTypesError`, `InvalidBaseError`,
  `InvalidCountError`, `InvalidDeviationError`, `InvalidPositionError`, `InvalidSeedError`,
  `IntegerOverflowError`, `InvalidShapeError`, `IrregularListError`, `MissingTypeError`, `NotSingleValueError`, `OutOfDomainError`,
  `RefusedOperationError`, `ShapeMismatchError`, `TimeOverflowError`, `UnsupportedMissingError`,
  `ValueConversionError`.
- `Type.TIME`: times of day from 00:00 to 23:59:59.999999, created from `datetime.time` values with
  `Array.from_list`, read back as `datetime.time` by `to_list`, `to_numpy` and `Table.to_pandas`, compared by the
  rules and sorted; durations of any unit read from numpy or pandas stay `DURATION`.
- `Table.convert` reads texts as `TIME`, as `HH:MM`, `HH:MM:SS` or `HH:MM:SS.ffffff` by default or with a
  `CustomDateFormat` of a time only such as `"%H%M"`, takes the local time of day of a `DATETIME`, and writes `TIME` as
  texts or categories, `15:35:00` by default.
- Calculations on `TIME`: two times subtracted give a `DURATION`, a duration added or subtracted moves a time within
  its day with a `TimeOverflowError` past midnight, a `DATE` plus a `TIME` gives a `DATETIME`, `DatePart` reads the
  hour, the minute and the second, and `Min`, `Max`, `Count`, `CountDistinct` and `MostFrequent` apply to times.
- `TIME` columns are written as texts such as `15:35:00` in CSV, JSON, Excel and Stata files, read back as `TEXT`,
  and as Parquet times read back as `TIME`.
- `Type` enum of value types and its conversion to numpy and pandas dtypes, and the `Library` enum read on
  `UnsupportedTypeError`.
- Rules: `Equal`, `NotEqual`, `Greater`, `GreaterOrEqual`, `Less`, `LessOrEqual`, `Between`, `IsIn`,
  `Contains`, `IsMissing`, `IsPresent`, with the `Bounds` and `Case` enums.
- Statistics: `Sum`, `Mean`, `Median`, `Min`, `Max`, `Count` with the `CountedMissing` enum, `CountDistinct`,
  `StandardDeviation`, `Quantile`, `MostFrequent`, `MostFrequentCount`.
- Positions: `Region`, `Index`, `Range` and the `Axis` enum.
- Sort settings: `Order` and `MissingPosition` enums.
- Errors: `NumdaplotError`, `EmptyRegionError`, `EmptyTextError`, `EmptyValuesError`, `InvalidBoundsError`,
  `InvalidFractionError`, `InvalidTypeError`, `InvalidStepError`, `UnsupportedTypeError`, and the
  `BroadcastWarning` and `CalculationWarning` warnings.
- `NumdaplotWarning`, the base of every numdaplot warning, filters them all at once with the `warnings` module.
