"""
Unit tests of TableDisplay.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

from numdaplot.tables import table_display
from numdaplot.tables.preview.preview import Preview
from numdaplot.tables.table_display import TableDisplay

FRAME = pandas.DataFrame({"price": [1.0, 2.0]})
PREVIEW_FRAME = pandas.DataFrame({"price": [2.0]})
CHOOSE_PREVIEW_ROWS_NAME = "choose_preview_rows"
SHOW_FRAME_NAME = "show_frame"


def choose_fake_rows(frame: pandas.DataFrame, preview: Preview) -> pandas.DataFrame:
	"""
	Fake row choice returning known rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns, ignored.
	preview
		The preview, ignored.

	Returns
	-------
	pandas.DataFrame
		Always the fake rows.
	"""
	return PREVIEW_FRAME


def test_preview_shows_the_chosen_rows(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the rows chosen by the preview are the ones shown.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the row choice and the display with fakes.
	"""
	shown_frames = list[pandas.DataFrame]()
	monkeypatch.setattr(table_display, CHOOSE_PREVIEW_ROWS_NAME, choose_fake_rows)
	monkeypatch.setattr(table_display, SHOW_FRAME_NAME, shown_frames.append)
	table = TableDisplay(FRAME)

	table.preview(Preview())

	assert shown_frames == [PREVIEW_FRAME]
