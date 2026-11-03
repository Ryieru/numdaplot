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
```

## Status

Version 0.1.0 is in development. The shared foundations (types, rules, statistics, positions,
sort settings, errors) and `Array` are available. Table and plots are not available yet.

## Requirements

- Python 3.13 or later
- numpy 2.2+, pandas 2.3+ and matplotlib 3.10+
- Optional extras: `excel` (openpyxl) and `parquet` (pyarrow)

## Installation

From a clone of the repository, with [uv](https://docs.astral.sh/uv/):

```
uv sync
```

## Run the tests

The test entry point runs the unit tests, the functional tests and every docstring example:

```
uv run python run_tests.py
```

Arguments are passed to pytest, for example `uv run python run_tests.py -k between`.

## Check the code

```
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

## Documentation

The documentation site is generated from the docstrings:

```
uv run mkdocs serve
```

## Code organization

```
src/numdaplot/
	__init__.py     every public name, available as ndp.*
	arrays/         Array and its settings: Shape, Spacing, distributions, math functions...
	errors/         NumdaplotError, the precise errors and BroadcastWarning
	data_types/     the Type enum and its conversion to numpy and pandas dtypes
	ratios/         validation of fractions between 0 and 1
	rules/          tests applied to each value: Equal, Greater, Between, IsIn, Contains, IsMissing...
	statistics/     Sum, Mean, Median, Quantile, StandardDeviation...
	positions/      Region, Index, Range and Axis
	ordering/       Order and MissingPosition
tests/
	unit/           one test file per source file, mirroring src/numdaplot
	functional/     one test file per notion, using the library as ndp
docs/               pages of the documentation site
run_tests.py        test entry point
```

## License

BSD-3-Clause, see [LICENSE](LICENSE).
