"""
Unit tests of TableDisplay and of the display of the missing values summary.

.. versionadded:: 0.1.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

import pandas
import pytest

from numdaplot.tables import table_display, table_missing
from numdaplot.tables.preview.preview import Preview
from numdaplot.tables.table_display import TableDisplay
from numdaplot.tables.table_missing import TableMissing

FRAME = pandas.DataFrame({"price": [1.0, 2.0]})
PREVIEW_FRAME = pandas.DataFrame({"price": [2.0]})
CHOOSE_PREVIEW_ROWS_NAME = "choose_preview_rows"
SHOW_FRAME_NAME = "show_frame"
SUMMARIZE_MISSING_NAME = "summarize_missing"
SHOW_PANDAS_FRAME_NAME = "show_pandas_frame"
SUMMARY_FRAME = pandas.DataFrame({"column": ["price", "total"]})


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
	table = TableDisplay._create(FRAME)

	table.preview(Preview())

	assert shown_frames == [PREVIEW_FRAME]


def give_fake_summary(frame: pandas.DataFrame) -> pandas.DataFrame:
	"""
	Fake summary of missing values returning a known summary.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns, ignored.

	Returns
	-------
	pandas.DataFrame
		Always the fake summary.
	"""
	return SUMMARY_FRAME


def test_preview_missing_shows_the_summary_as_it_is(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the summary of missing values is shown without the types under the column names.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the summary and the display with fakes.
	"""
	shown_frames = list[pandas.DataFrame]()
	monkeypatch.setattr(table_missing, SUMMARIZE_MISSING_NAME, give_fake_summary)
	monkeypatch.setattr(table_missing, SHOW_PANDAS_FRAME_NAME, shown_frames.append)
	table = TableMissing._create(FRAME)

	table.preview_missing()

	assert shown_frames == [SUMMARY_FRAME]


def test_preview_without_settings_shows_the_default_preview(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that preview without settings chooses the rows with the default Preview.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the row choice and the display with fakes.
	"""
	received_previews = list[Preview]()

	def choose_recorded_rows(frame: pandas.DataFrame, preview: Preview) -> pandas.DataFrame:
		"""
		Keep the preview and return the fake rows.

		.. versionadded:: 0.1.0

		Parameters
		----------
		frame
			The columns, ignored.
		preview
			The preview received.

		Returns
		-------
		pandas.DataFrame
			Always the fake rows.
		"""
		received_previews.append(preview)

		return PREVIEW_FRAME

	monkeypatch.setattr(table_display, CHOOSE_PREVIEW_ROWS_NAME, choose_recorded_rows)
	monkeypatch.setattr(table_display, SHOW_FRAME_NAME, list[pandas.DataFrame]().append)
	table = TableDisplay._create(FRAME)

	table.preview()

	assert received_previews == [Preview()]
