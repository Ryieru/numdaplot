# numdaplot

A simpler, explicit API over numpy, pandas and matplotlib.

Each action has exactly one way to be written, settings are typed objects that check their values
when they are created, and every operation returns a new object.

```python
import numdaplot as ndp

prices = ndp.Array.from_list([12.5, 8.0, None, 30.0])
taxed_prices = prices * 1.2
high_prices = taxed_prices.select(ndp.Greater(10))
mean_price = prices.compute(ndp.Mean()).to_value()

sales = ndp.Table.from_csv("sales.csv")
expensive = ndp.Condition(rule=ndp.Greater(100), columns=["price"])
expensive_sales = sales.filter(ndp.Filter(conditions=[expensive]))
average_price = ndp.Calculation(column="price", function=ndp.Mean())
by_city = expensive_sales.aggregate(ndp.Aggregation(calculations=[average_price], group_by=["city"]))

chart = ndp.BarChart(x="city", y=["price_mean"])
style = ndp.PlotStyle(title="Average price per city")
plot = ndp.Plot.bar(by_city, chart, style)
plot.save("prices.png")
```

## Status

numdaplot is in alpha: the API can still change between versions, and `ndp.__version__` gives the installed version.
The shared foundations (types, rules, statistics, positions,
sort settings, errors), `Array`, `Table`, the tools for missing values and dates (formats, time zones,
parts, periods and durations), line, bar, scatter, histogram, box, pie, heatmap and missing value plots,
charts overlaid on a plot, and figures placing plots on a grid are available.

## Requirements

- Python 3.13 or later
- numpy 2.2+, pandas 2.3+ and matplotlib 3.10.7+
- Optional extras: `excel` (openpyxl) and `parquet` (pyarrow)

## Installation

```
pip install numdaplot
pip install "numdaplot[excel,parquet]"
```

The `excel` extra reads and writes Excel files, the `parquet` extra reads and writes Parquet files.

## Development

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

The documentation is online at https://ryieru.github.io/numdaplot/. It is generated from the docstrings,
and shown locally with:

```
uv run mkdocs serve
```

## Release

A version is published by pushing a tag `v<version>`. The `Release` workflow then runs the checks, builds the
package, publishes it on TestPyPI, waits for an approval on GitHub, publishes it on PyPI, publishes the
documentation site and creates the GitHub release with the changes of `CHANGELOG.md`.

1. A minor or major version, such as `0.2.0` or `1.0.0`, is first tried as a release candidate: set
   `version = "0.2.0rc1"` in `pyproject.toml`, commit, push, then push the tag. A release candidate only goes to
   TestPyPI. Check its page and its installation, and fix with `0.2.0rc2` and so on until it is right.
2. Set the final version in `pyproject.toml`, and replace `## [Unreleased]` with `## [0.2.0] - <date>` in
   `CHANGELOG.md`. Commit, push, then push the tag.
3. Check the version on TestPyPI, then approve the `pypi` environment in the workflow run on GitHub.

A patch version, such as `0.1.1`, skips step 1. When TestPyPI shows a problem, the approval is refused and the patch
is tried again as `0.1.1rc1`.

```
git tag v0.2.0rc1
git push origin v0.2.0rc1
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ numdaplot==0.2.0rc1
```

## Code organization

```
src/numdaplot/
	__init__.py     every public name, available as ndp.*
	arrays/         Array and its settings: Shape, Spacing, distributions, math functions...
	tables/         Table and its settings: file options, Filter, Aggregation, PivotTable, Sorting, Preview...
	dates/          DateFormat, TimeZone, TimeZoneChange, DatePart, DatePeriod, DurationIn, ToDuration...
	plots/          Plot and its creation methods, the charts, the PlotStyle and Figure
	errors/         NumdaplotError, the precise errors, NumdaplotWarning and the precise warnings
	data_types/     the Type enum and its conversion to numpy and pandas dtypes
	ratios/         validation of fractions between 0 and 1, and the Measure enum
	rules/          tests applied to each value: Equal, Greater, Between, IsIn, Contains, IsMissing...
	statistics/     Sum, Mean, Median, Quantile, StandardDeviation...
	positions/      Region, Index, Range and Axis
	ordering/       Order and MissingPosition
	settings/       check of the settings against their annotations, InvalidTypeError being raised
tests/
	unit/           one test file per source file, mirroring src/numdaplot
	functional/     one test file per notion, using the library as ndp
docs/               pages and stylesheet of the documentation site
tools/docs/         griffe extensions and MkDocs hooks building the documentation site and its API pages
run_tests.py        test entry point
conftest.py         pytest settings shared by the tests and the docstring examples
```

## License

BSD-3-Clause, see [LICENSE](https://github.com/Ryieru/numdaplot/blob/main/LICENSE).
