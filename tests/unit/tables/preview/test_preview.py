"""
Unit tests of Preview, the rows it shows and their display.

.. versionadded:: 0.1.0
"""

from types import SimpleNamespace
from typing import Any, cast

import pandas
import pytest

from numdaplot.errors.invalid_count_error import InvalidCountError
from numdaplot.errors.invalid_seed_error import InvalidSeedError
from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.tables.preview import notebook_display
from numdaplot.tables.preview.notebook_display import show_frame, show_pandas_frame
from numdaplot.tables.preview.preview import Preview
from numdaplot.tables.preview.preview_rows import choose_preview_rows
from numdaplot.tables.preview.shown_columns import ShownColumns
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
EXPECTED_TEXT_START = "price"
EXPECTED_PLAIN_TEXT = "price\n0    1.0"
PLAIN_FRAME = pandas.DataFrame({"price": [1.0]})
EXPECTED_HTML_START = "<table"


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
	show_frame(FRAME, ShownColumns.ALL)

	captured = capsys.readouterr()
	printed_text = captured.out.strip()
	assert printed_text.startswith(EXPECTED_TEXT_START)


def test_show_frame_displays_html_in_a_notebook(monkeypatch: pytest.MonkeyPatch, module_giver: Any) -> None:
	"""
	Check that a notebook receives an HTML table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the notebook check and the IPython display module with fakes.
	module_giver
		Builds the fake import giving the display module.
	"""
	shown_objects = list[str]()
	display_module = SimpleNamespace(HTML=str, display=shown_objects.append)
	monkeypatch.setattr(notebook_display, IS_NOTEBOOK_NAME, answer_true)
	fake_import = module_giver(display_module)
	monkeypatch.setattr(notebook_display, IMPORT_MODULE_NAME, fake_import)

	show_frame(FRAME, ShownColumns.ALL)

	shown_html = shown_objects[0]
	assert shown_html.startswith(EXPECTED_HTML_START)


def test_show_pandas_frame_prints_the_frame_without_types(capsys: pytest.CaptureFixture[str]) -> None:
	"""
	Check that the text of a pandas DataFrame is printed as pandas writes it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	capsys
		Captures the printed text.
	"""
	show_pandas_frame(PLAIN_FRAME)

	captured = capsys.readouterr()
	printed_text = captured.out.strip()
	assert printed_text == EXPECTED_PLAIN_TEXT


def test_show_pandas_frame_displays_html_in_a_notebook(monkeypatch: pytest.MonkeyPatch, module_giver: Any) -> None:
	"""
	Check that a notebook receives an HTML table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the notebook check and the IPython display module with fakes.
	module_giver
		Builds the fake import giving the display module.
	"""
	shown_objects = list[str]()
	display_module = SimpleNamespace(HTML=str, display=shown_objects.append)
	monkeypatch.setattr(notebook_display, IS_NOTEBOOK_NAME, answer_true)
	fake_import = module_giver(display_module)
	monkeypatch.setattr(notebook_display, IMPORT_MODULE_NAME, fake_import)

	show_pandas_frame(PLAIN_FRAME)

	shown_html = shown_objects[0]
	assert shown_html.startswith(EXPECTED_HTML_START)


def test_preview_rejects_a_side_written_as_text() -> None:
	"""
	Check that a text in place of a Side raises InvalidTypeError.

	.. versionadded:: 0.1.0
	"""
	untyped_preview = cast(Any, Preview)

	with pytest.raises(InvalidTypeError):
		untyped_preview(side="end")


@pytest.mark.parametrize("side", [Side.START, Side.END])
def test_preview_rejects_a_seed_without_random_draw(side: Side) -> None:
	"""
	Check that a seed with the first or the last rows raises RefusedSettingError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	side
		A side that draws nothing.
	"""
	with pytest.raises(RefusedSettingError):
		Preview(side=side, seed=SEED)


def test_preview_keeps_a_seed_for_a_random_draw() -> None:
	"""
	Check that a random draw accepts a seed.

	.. versionadded:: 0.1.0
	"""
	preview = Preview(side=Side.RANDOM, seed=SEED)

	assert preview.seed == SEED


def test_preview_shows_every_column_by_default() -> None:
	"""
	Check the default of the setting of the columns.

	.. versionadded:: 0.1.0
	"""
	preview = Preview()

	assert preview.columns == ShownColumns.ALL


def test_preview_keeps_the_setting_of_the_columns() -> None:
	"""
	Check that the setting is available as an attribute.

	.. versionadded:: 0.1.0
	"""
	preview = Preview(columns=ShownColumns.COMPACT)

	assert preview.columns == ShownColumns.COMPACT
