"""
Unit tests of Preview, the rows it shows and their display.

.. versionadded:: 0.1.0
"""

from types import SimpleNamespace

import pandas
import pytest

from numdaplot.errors.invalid_count_error import InvalidCountError
from numdaplot.errors.invalid_seed_error import InvalidSeedError
from numdaplot.tables.preview import notebook_display
from numdaplot.tables.preview.notebook_display import is_notebook, show_frame
from numdaplot.tables.preview.preview import Preview
from numdaplot.tables.preview.preview_rows import choose_preview_rows
from numdaplot.tables.preview.side import Side

FRAME = pandas.DataFrame({"price": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]})
DEFAULT_COUNT = 5
SEED = 7
REJECTED_COUNT = 0
REJECTED_SEED = -1
TWO_ROWS = 2
EXPECTED_FIRST_ROWS = [0, 1]
EXPECTED_LAST_ROWS = [4, 5]
LARGE_COUNT = 10
EXPECTED_ROW_COUNT = 6
IS_NOTEBOOK_NAME = "is_notebook"
IMPORT_MODULE_NAME = "import_module"
FIND_SPEC_NAME = "find_spec"
EXPECTED_TEXT_START = "price"
EXPECTED_HTML_START = "<table"
NOTEBOOK_CONFIG = dict[str, object]({"IPKernelApp": None})
TERMINAL_CONFIG = dict[str, object]()
FOUND_PACKAGE = object()


class ModuleGiver:
	"""
	Fake module import giving the same module whatever its name.

	.. versionadded:: 0.1.0

	Parameters
	----------
	module
		The module to give.
	"""

	def __init__(self, module: SimpleNamespace) -> None:
		"""
		Keep the module to give.

		.. versionadded:: 0.1.0

		Parameters
		----------
		module
			The module to give.
		"""
		self.module = module

	def __call__(self, module_name: str) -> SimpleNamespace:
		"""
		Give the module.

		.. versionadded:: 0.1.0

		Parameters
		----------
		module_name
			The imported name, ignored.

		Returns
		-------
		SimpleNamespace
			The kept module.
		"""
		return self.module


def build_fake_ipython(config: dict[str, object] | None) -> SimpleNamespace:
	"""
	Return a fake IPython module whose shell has a configuration, or no shell.

	.. versionadded:: 0.1.0

	Parameters
	----------
	config
		The configuration of the shell, or ``None`` for no shell.

	Returns
	-------
	SimpleNamespace
		A module with a ``get_ipython`` function.
	"""
	shell = None
	if config is not None:
		shell = SimpleNamespace(config=config)

	fake_module = SimpleNamespace(get_ipython=lambda: shell)

	return fake_module


def find_no_package(package_name: str) -> None:
	"""
	Fake package lookup that finds nothing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	package_name
		The searched package, ignored.
	"""
	return None


def find_any_package(package_name: str) -> object:
	"""
	Fake package lookup that finds every package.

	.. versionadded:: 0.1.0

	Parameters
	----------
	package_name
		The searched package, ignored.

	Returns
	-------
	object
		A found package.
	"""
	return FOUND_PACKAGE


def answer_true() -> bool:
	"""
	Fake notebook check that always answers yes.

	.. versionadded:: 0.1.0

	Returns
	-------
	bool
		Always True.
	"""
	return True


def test_preview_shows_the_first_five_rows_by_default() -> None:
	"""
	Check the default count, side and seed.

	.. versionadded:: 0.1.0
	"""
	preview = Preview()

	assert preview.count == DEFAULT_COUNT
	assert preview.side == Side.START
	assert preview.seed is None


def test_preview_rejects_a_count_below_one() -> None:
	"""
	Check that 0 rows raises InvalidCountError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidCountError):
		Preview(count=REJECTED_COUNT)


def test_preview_rejects_a_negative_seed() -> None:
	"""
	Check that a negative seed raises InvalidSeedError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidSeedError):
		Preview(seed=REJECTED_SEED)


@pytest.mark.parametrize(
	("side", "expected_rows"),
	[
		(Side.START, EXPECTED_FIRST_ROWS),
		(Side.END, EXPECTED_LAST_ROWS),
	],
)
def test_choose_preview_rows_takes_the_first_or_last_rows(side: Side, expected_rows: list[int]) -> None:
	"""
	Check the row numbers of the first and the last two rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	side
		Which rows to show.
	expected_rows
		Their row numbers.
	"""
	preview = Preview(count=TWO_ROWS, side=side)

	chosen_rows = choose_preview_rows(FRAME, preview)

	row_numbers = chosen_rows.index.tolist()
	assert row_numbers == expected_rows


def test_choose_preview_rows_draws_the_same_rows_with_the_same_seed() -> None:
	"""
	Check that a seed gives the same draw twice, shown in the order of the Table.

	.. versionadded:: 0.1.0
	"""
	preview = Preview(count=TWO_ROWS, side=Side.RANDOM, seed=SEED)

	first_draw = choose_preview_rows(FRAME, preview)
	second_draw = choose_preview_rows(FRAME, preview)

	first_rows = first_draw.index.tolist()
	second_rows = second_draw.index.tolist()
	sorted_rows = sorted(first_rows)
	assert first_rows == second_rows
	assert first_rows == sorted_rows


def test_choose_preview_rows_shows_every_row_of_a_short_table() -> None:
	"""
	Check that a random draw of more rows than the Table has shows all of them.

	.. versionadded:: 0.1.0
	"""
	preview = Preview(count=LARGE_COUNT, side=Side.RANDOM)

	chosen_rows = choose_preview_rows(FRAME, preview)

	row_count = len(chosen_rows)
	assert row_count == EXPECTED_ROW_COUNT


def test_show_frame_prints_text_outside_a_notebook(capsys: pytest.CaptureFixture[str]) -> None:
	"""
	Check that the text of the rows is printed.

	.. versionadded:: 0.1.0

	Parameters
	----------
	capsys
		Captures the printed text.
	"""
	show_frame(FRAME)

	captured = capsys.readouterr()
	printed_text = captured.out.strip()
	assert printed_text.startswith(EXPECTED_TEXT_START)


def test_show_frame_displays_html_in_a_notebook(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that a notebook receives an HTML table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the notebook check and the IPython display module with fakes.
	"""
	shown_objects = list[str]()
	display_module = SimpleNamespace(HTML=str, display=shown_objects.append)
	monkeypatch.setattr(notebook_display, IS_NOTEBOOK_NAME, answer_true)
	monkeypatch.setattr(notebook_display, IMPORT_MODULE_NAME, ModuleGiver(display_module))

	show_frame(FRAME)

	shown_html = shown_objects[0]
	assert shown_html.startswith(EXPECTED_HTML_START)


def test_is_notebook_is_false_without_ipython(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that a missing IPython means no notebook.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the package lookup with one that finds nothing.
	"""
	monkeypatch.setattr(notebook_display, FIND_SPEC_NAME, find_no_package)

	runs_in_notebook = is_notebook()

	assert not runs_in_notebook


@pytest.mark.parametrize(
	("config", "expected_answer"),
	[
		(None, False),
		(TERMINAL_CONFIG, False),
		(NOTEBOOK_CONFIG, True),
	],
)
def test_is_notebook_checks_for_a_jupyter_kernel(
	monkeypatch: pytest.MonkeyPatch,
	config: dict[str, object] | None,
	expected_answer: bool,
) -> None:
	"""
	Check the answer without shell, in an IPython terminal and in a Jupyter kernel.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces IPython with a fake.
	config
		The configuration of the fake shell, or None for no shell.
	expected_answer
		Whether it is a notebook.
	"""
	fake_ipython = build_fake_ipython(config)
	monkeypatch.setattr(notebook_display, FIND_SPEC_NAME, find_any_package)
	monkeypatch.setattr(notebook_display, IMPORT_MODULE_NAME, ModuleGiver(fake_ipython))

	runs_in_notebook = is_notebook()

	assert runs_in_notebook == expected_answer
