# Changelog

All notable changes to numdaplot are listed in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and numdaplot follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `Table.shape` gives the number of rows and columns of a table as a `Shape`, like `Array.shape`.
- `Unmatched.KEEP` keeps the values a `ValueMapping` gives no new value, so that only the listed values change.
  `Brackets` refuses it.
- `Array.convert` changes the type of the values of an Array with an `ArrayConversion`, as `Table.convert` does
  for columns.
- `Table.count_values` gives how many rows hold each value of a column with a `ValueCount`, as a number or,
  with `Measure.RATIO`, as a fraction of every row, from the most frequent value to the least frequent. With
  `ValueCount(weights="weight")`, each row counts as much as its weight, such as the weights of a survey, and a
  negative weight raises `InvalidWeightError`.
- `Share` gives the fraction of the values satisfying a rule, of an Array or of each group in `aggregate`,
  `pivot_table` and `describe`, without the missing values unless `missing=CountedMissing.INCLUDED`.
- `Aggregation(row_count=...)` adds the number of rows of each group, without choosing a column, right after the
  group columns. `calculations` becomes optional, and `EmptyAggregationError` is raised when neither is given.
- `Equal`, `NotEqual`, `Greater`, `GreaterOrEqual`, `Less` and `LessOrEqual` accept an Array as reference value,
  which compares each value with the value at its position, such as the rows whose city of departure is also their
  city of arrival with `ndp.Equal(table.column("arrival"))`. `Between` accepts Arrays as bounds, and raises
  `InvalidBoundsError` at the first position whose low bound is above its high bound. These rules work in `check`,
  `select`, `filter` and in a `Share`, by group in `aggregate`, `pivot_table` and `describe` too.
- `First` and `Last` choose the first or the last positions in a `Region`, such as the first 10 rows of a sorted
  Table with `table.take(ndp.Region(rows=ndp.First(10)))`. A dimension shorter than the count gives every position.
- `BarChart(value_labels=ValueLabels(decimals=2))` writes the value of each bar past its end, or in the middle of
  each part of stacked bars, rounded to the decimals asked. The axis makes room for the values, values too wide
  for their bars turn upright, and values that still do not fit are left out with a `ReadabilityWarning`.
- `Table.apply` applies a math function, a time function or a `ValueMapping` to several columns at once with a
  `TableApplication`, each column replaced at its place. An integer or boolean column keeps its type when a
  `ValueMapping` gives it missing values.

### Changed

- `Conversion` is renamed `TableConversion`.
- `Sorting` is renamed `TableSorting`.
- `TableConversion` takes `columns`, a list, in place of `column`, so that `Table.convert` converts several columns
  to the same type at once.
- The default label of the axis of several series is `Value`, as for an Array, since the legend names them. The
  default title still names them, such as `price, cost by month`. One series keeps its column name.
- The legend and the colors of the groups of a `ScatterChart` `color_by` column follow the natural order of its
  values, such as `Cluster 2` before `Cluster 10` and without regard to case, or the order of the categories of a
  column of categories, instead of the order of the rows. A group keeps its color whatever the order of the rows.
- `OutOfDomainError` and `UnmatchedValueError` name the Table column holding the value, such as a value in no
  bracket of `Brackets` in `Table.convert`.
- The message of `UnmatchedValueError` for a `ValueMapping` also offers `others=Unmatched.KEEP`.
- Numbers given by a `ValueMapping` to an Array of numbers take its type, as with the operators: `INT8` codes stay
  `INT8`, integers given to decimals give decimals, and a number that does not fit raises `ValueConversionError`.
  Decimals given to integers still give `FLOAT64`.
- The message of `IntegerOverflowError` gives the range of the type, and advises `INT64` for smaller integers,
  `FLOAT64` for `INT64` and `UINT64`.
- The documentation shows the latest version note of each object and folds the earlier ones in a version history.
  Every enum member tells its version. Class pages no longer repeat the parameters of the creation.
- The documentation lists `TableConversion` and `BooleanRule` in a Conversions section.
- The documentation lists `Measure` in a Measures section, shared by tables and plots, and groups the settings of
  `aggregate`, `pivot_table`, `describe` and `count_values` under Statistic settings.
- After ten series or `color_by` groups without chosen colors, the default colors go on with the light colors of the
  first ten instead of starting again. After 20, they start again with a `ReadabilityWarning`.
- `LegendPosition.BEST` places the legend past the axes on the right when it would hide a value inside them, such as a
  point, a part of a line or a bar.
- The title of a Plot is centered above the whole Plot, its legend included, and goes on several lines when it is
  too wide. It is the title of the matplotlib figure, or subfigure in a `Figure`, given by `to_matplotlib`.
- The `DuplicateColumnError` of an `Aggregation` giving two results the same name advises a `result_name` for each
  calculation.
- The documentation lists every method and operator of `Array`, `Table` and `Plot`, `Table.pivot_table` and
  `Table.join` included, in sections that follow the code: the same notion has the same title on every page, such
  as Calculation and Layout.
- The documentation links each object to its source on GitHub instead of showing the code.
- The documentation groups the errors and warnings by notion, such as File errors, Type errors and Plot errors.
- The advice of `ValueConversionError` and `InvalidConversionError` about formats speaks of the values, which fits an
  Array as well as a column.
- Each member of `Type` gives the rules of its type with examples, such as the type of a sum or of a division, and
  the page of `Type` no longer says that integers wrap around.

### Fixed

- `Description` refuses two statistics giving rows of the same name, such as two `Share`, with
  `DuplicateStatisticError`. A statistic whose settings hold a list no longer raises `TypeError`.
- `SquareRoot`, `Exponential`, `Logarithm`, `Sine` and `Cosine` give `FLOAT64` for integers of any size: they raised
  `UnsupportedTypeError` on `INT8` and `UINT8` values, and gave `FLOAT32` on `INT16` and `UINT16` values.
- `IntegerOverflowError` names the type of the Array when a number written before an operator does not fit it,
  such as `1000 * values` on `INT8` values, instead of `INT64`.
- A `ValueMapping` whose new values are all missing keeps the type of the Array: it raised `MissingTypeError`.
  On integers or booleans, `UnsupportedMissingError` advises to convert the Array first.

## [0.1.2] - 2026-11-10

### Changed

- The description of the package has changed to "A typed API for arrays, tables and plots, built on
  numpy, pandas and matplotlib".
- The README presents the library only; the development and release guides are pages of the documentation.

## [0.1.1] - 2026-11-10

### Added

- The PyPI page links to the changelog and to the issues, and lists keywords.

### Fixed

- The source distribution credits the pandas license of the SAS and XPT sample files.

## [0.1.0] - 2026-11-10

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
- `Plot.show` and `Figure.show` emit a `DisplayWarning` at the line calling them when no window can be opened, such
  as without `tkinter` or on a server, suggesting to install `tkinter` or to save the image.
- Plot settings: `Chart`, `LineChart`, `BarChart`, `ScatterChart`, `HistogramChart`, `BoxChart`, `PieChart`,
  `HeatmapChart`, `MissingChart`, `BinCount`, `BinWidth`, `PlotStyle`, `Size`, `CustomColor`, `ImageOptions`, and the
  `Color`, `LineType`, `MarkerShape`, `Orientation`, `BarLayout`, `Outliers`, `Percentages`, `ColorScale`,
  `CellValues`, `LegendPosition`, `GridLines` and `SizeUnit` enums.
- Plots: the labels of an axis without enough room are left out, one out of as many as needed from the first one,
  with a `ReadabilityWarning` when they may be texts.
- Plot errors and warnings: `ConflictingSettingsError`, `DuplicateLabelError`, `EmptyTotalError`,
  `InvalidBinWidthError`, `InvalidChartDataError`, `InvalidColorCountError`, `InvalidColorError`,
  `InvalidOpacityError`, `InvalidPointSizeError`, `InvalidResolutionError`, `InvalidRotationError`,
  `InvalidSizeError`, `MissingValueError`, `RefusedSettingError`,
  `UnsupportedImageFormatError`, `IncompatibleChartsError`, `OccupiedCellError`, `CellOutOfRangeError`,
  `ReadabilityWarning` and `DisplayWarning`.
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
- A `Table` written at the end of a notebook cell is shown as the HTML table of `Table.preview`, with every column
  and the type of each column under its name; a long Table shows its first and last rows, as its text does.
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
- `Table.from_excel` reads columns of time cells as `TIME` and columns of duration cells as `DURATION`.
- Plots place `TIME` columns at their hours on the x axis of line, bar and scatter charts, labeled `HH:MM`, and
  name heatmap rows, pie slices, `color_by` groups and box `group_by` groups with `HH:MM` labels.
- Plots measure `TIME` values on an axis labeled `HH:MM`: `y` of line and scatter charts, box charts, histograms
  and Arrays of times of day. A histogram of times has one bin per hour from 00:00 to 24:00 by default, and
  `BinWidth` takes a duration of at most a day for times of day.
- `Table.join` joins two Tables on key columns (`Join`, `JoinMode`, `JoinSuffixes`, `KeyTypes`): inner, left,
  right and outer joins, missing keys never matching, keys of one family by default, an optional check of how many
  times each key appears (`Relation`), `InvalidSuffixesError` and `JoinRelationError`.
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
