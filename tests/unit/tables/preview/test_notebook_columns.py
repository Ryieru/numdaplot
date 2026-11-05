"""
Unit tests of the columns of the HTML table shown in a notebook.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

from numdaplot.tables.preview import notebook_display
from numdaplot.tables.preview.notebook_display import show_frame
from numdaplot.tables.preview.shown_columns import ShownColumns

LONG_NAME = "long_column_name_"
COLUMN_COUNT = 30
WIDE_FRAME = pandas.DataFrame({f"{LONG_NAME}{number}": [float(number)] for number in range(COLUMN_COUNT)})
COMPACT_MARK = "..."
IS_NOTEBOOK_NAME = "is_notebook"
DISPLAY_HTML_NAME = "display_html"


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


def show_wide_html(monkeypatch: pytest.MonkeyPatch, shown_columns: ShownColumns) -> str:
	"""
	Return the HTML table a notebook receives for a wide frame.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the notebook check and the HTML display with fakes.
	shown_columns
		Whether every column is shown.

	Returns
	-------
	str
		The HTML table.
	"""
	shown_tables = list[str]()
	monkeypatch.setattr(notebook_display, IS_NOTEBOOK_NAME, answer_true)
	monkeypatch.setattr(notebook_display, DISPLAY_HTML_NAME, shown_tables.append)

	show_frame(WIDE_FRAME, shown_columns)

	return shown_tables[0]


def test_show_frame_gives_every_column_to_a_notebook(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the HTML table holds every column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the notebook check and the HTML display with fakes.
	"""
	shown_html = show_wide_html(monkeypatch, ShownColumns.ALL)

	assert shown_html.count(LONG_NAME) == COLUMN_COUNT


def test_show_frame_gives_a_compact_table_to_a_notebook(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the compact HTML table only holds some columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the notebook check and the HTML display with fakes.
	"""
	shown_html = show_wide_html(monkeypatch, ShownColumns.COMPACT)

	assert shown_html.count(LONG_NAME) < COLUMN_COUNT
	assert COMPACT_MARK in shown_html
