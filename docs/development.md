# Development

## Setup

From a clone of the repository, with [uv](https://docs.astral.sh/uv/):

```
uv sync --all-extras
```

The extras are needed to run every test, since the Excel and Parquet tests write real files.

## Run the tests

The test entry point runs the unit tests, the functional tests and every docstring example:

```
uv run python run_tests.py
```

Arguments are passed to pytest, for example `uv run python run_tests.py -k between`.

## Measure the coverage

The coverage of every line and every branch of `src/numdaplot` and `tools/docs` is measured while the whole suite
runs, and must reach 99.50%:

```
uv run coverage run run_tests.py
uv run coverage report
```

`uv run coverage html` writes a detailed report in `htmlcov/`.

## Check the code

```
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

## Documentation

The site is generated from the docstrings, and shown locally with:

```
uv run mkdocs serve
```

## Code organization

```
src/numdaplot/
	__init__.py     every public name, available as ndp.*
	arrays/         Array and its settings: Spacing, distributions, math functions...
	tables/         Table and its settings: file options, Filter, Aggregation, PivotTable, Sorting, Preview...
	conversions/    TableConversion, ArrayConversion, BooleanRule and the conversion of values to another type
	dates/          DateFormat, TimeZone, TimeZoneChange, DatePart, DatePeriod, DurationIn, ToDuration...
	plots/          Plot and its creation methods, the charts, the PlotStyle and Figure
	errors/         NumdaplotError, the precise errors, NumdaplotWarning and the precise warnings
	data_types/     the Type enum and its conversion to numpy and pandas dtypes
	ratios/         validation of fractions between 0 and 1, and the Measure enum
	rules/          tests applied to each value: Equal, Greater, Between, IsIn, Contains, IsMissing...
	statistics/     Sum, Mean, Median, Quantile, StandardDeviation...
	shapes/         Shape, the dimensions of an Array or a Table
	positions/      Region, Index, Range and Axis
	ordering/       Order and MissingPosition
	settings/       check of the settings against their annotations, InvalidTypeError being raised
tests/
	unit/           one test file per source file, mirroring src/numdaplot
	functional/     one test file per notion, using the library as ndp
docs/               pages, images and stylesheet of the documentation site
tools/docs/         griffe extensions and MkDocs hooks building the documentation site and its API pages
run_tests.py        test entry point
conftest.py         pytest settings shared by the tests and the docstring examples
```

