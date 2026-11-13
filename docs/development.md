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

## Checks before a commit and a push

Git runs the checks of `tools/checks/` through the hooks of `tools/git_hooks/`, once enabled in the clone:

```
git config core.hooksPath tools/git_hooks
```

Before a commit, ruff and pyright check the staged files, then the size, repeated code, writing rules, version notes
and changelog entries are checked. Before a push, ruff checks every file, then the three jobs of the CI run at the same
time, each in its own copy of the project under `/tmp/numdaplot-*`: Python 3.13 and 3.14 with the latest
dependencies, Python 3.13 with the minimum ones. Each copy resolves its dependencies again, then runs pyright, the
tests with their coverage and the strict build of the site.

A line tells when each command starts and ends, and the full output of each command is kept in a dated log file under
`/tmp/numdaplot-*/logs/`. A blocking failure stops the git action; a warning is only shown. The same checks run by hand:

```
uv run --frozen python tools/checks/run_checks.py commit
uv run --frozen python tools/checks/run_checks.py push
```

`git commit --no-verify` or `git push --no-verify` skips the hook once.

The CI job "Writing checks" runs the same checks on the commits of each push to `main` and of each pull request,
without the tools its other jobs already run, so a commit made without the hooks is checked too. Its problems are
also shown on the lines of the commits in GitHub.

## Documentation

The site is generated from the docstrings, and shown locally with:

```
uv run mkdocs serve
```

## Review before a push

The hooks run every check a program can make. A reader still checks the following by hand.

### Changelog

1. List the commits: `git log --oneline origin/main..HEAD`.
2. Every commit that changes what a user sees has an entry under `[Unreleased]`: Added for a new notion,
   Changed for a new behavior, Fixed for a wrong behavior. Internal moves and renames have none.
3. Each entry states the current behavior, names the objects in code style, and matches the code.
4. No two entries tell the same change, and no entry contradicts another one.

### Documentation

1. The names used in `README.md` and in `docs/*.md` exist, with the settings they take today.
2. The code organization below lists every folder and its main objects.
3. For each behavior a commit changes, search the docstrings for the former wording of that behavior and rewrite what
   does not match the code.
4. Every public object whose behavior or signature changes has `.. versionchanged::` with one sentence,
   enum members included. A new member gets its own `.. versionadded::`.
5. Open the pages of the new and changed objects on the local site (`uv run mkdocs serve`): section, examples, images.

### Code

1. A notion repeated with small differences, that the duplicate checks cannot see, is shared.
2. A function needing a comment has a full NumPy docstring, and no comment tells the history of the code.
3. The warnings of the report are read one by one: each is fixed, or kept for a reason.
4. Every new function has unit tests, every new notion functional tests.

## Code organization

```
src/numdaplot/
	__init__.py     every public name, available as ndp.*
	arrays/         Array and its settings: Spacing, distributions, math functions...
	tables/         Table and its settings: file options, Filter, Aggregation, PivotTable, TableSorting, Preview...
	conversions/    TableConversion, ArrayConversion, BooleanRule and the conversion of values to another type
	dates/          DateFormat, TimeZone, TimeZoneChange, DatePart, DatePeriod, DurationIn, ToDuration...
	plots/          Plot and its creation methods, the charts, the PlotStyle and Figure
	errors/         NumdaplotError, the precise errors, NumdaplotWarning and the precise warnings
	data_types/     the Type enum and its conversion to numpy and pandas dtypes
	ratios/         validation of fractions between 0 and 1, and the Measure enum
	rules/          tests applied to each value: Equal, Greater, Between, IsIn, Contains, IsMissing...
	statistics/     Sum, Mean, Median, Quantile, StandardDeviation...
	shapes/         Shape, the dimensions of an Array or a Table
	positions/      Region, Index, Range, First, Last and Axis
	ordering/       Order, MissingPosition and the natural order of texts
	settings/       check of the settings against their annotations, InvalidTypeError being raised
tests/
	unit/           mirroring src/numdaplot, the small objects of a notion tested together
	functional/     one test file per notion, using the library as ndp
docs/               pages, images and stylesheet of the documentation site
tools/docs/         griffe extensions and MkDocs hooks building the documentation site and its API pages
tools/checks/       checks run before a commit and a push, outside the tests and the coverage
tools/git_hooks/    the pre-commit and pre-push hooks running tools/checks/
run_tests.py        test entry point
conftest.py         pytest settings shared by the tests and the docstring examples
```

