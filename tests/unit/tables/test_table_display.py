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
from numdaplot.tables.preview.shown_columns import ShownColumns
from numdaplot.tables.table_display import TableDisplay
from numdaplot.tables.table_missing import TableMissing

FRAME = pandas.DataFrame({"price": [1.0, 2.0]})
PREVIEW_FRAME = pandas.DataFrame({"price": [2.0]})
CHOOSE_PREVIEW_ROWS_NAME = "choose_preview_rows"
SHOW_FRAME_NAME = "show_frame"
SUMMARIZE_MISSING_NAME = "summarize_missing"
SHOW_PANDAS_FRAME_NAME = "show_pandas_frame"
SUMMARY_FRAME = pandas.DataFrame({"column": ["price", "total"]})
FAKE_TEXT = "fake table text"
FORMAT_TABLE_NAME = "format_table"
FORMAT_TABLE_HTML_NAME = "format_table_html"
FAKE_HTML = "<table>fake</table>"


class ShownRows:
	"""
	Fake display keeping what it receives.

	.. versionadded:: 0.1.0
	"""

	def __init__(self) -> None:
		"""
		Start without any display.

		.. versionadded:: 0.1.0
		"""
		self.frames = list[pandas.DataFrame]()
		self.shown_columns = list[ShownColumns]()

	def show(self, frame: pandas.DataFrame, shown_columns: ShownColumns) -> None:
		"""
		Keep the rows and the setting of the columns.

		.. versionadded:: 0.1.0

		Parameters
		----------
		frame
			The rows to show.
		shown_columns
			Whether every column is shown.
		"""
		self.frames.append(frame)
		self.shown_columns.append(shown_columns)


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
	shown_rows = ShownRows()
	monkeypatch.setattr(table_display, CHOOSE_PREVIEW_ROWS_NAME, choose_fake_rows)
	monkeypatch.setattr(table_display, SHOW_FRAME_NAME, shown_rows.show)
	table = TableDisplay._create(FRAME)

	table.preview(Preview(columns=ShownColumns.COMPACT))

	assert shown_rows.frames == [PREVIEW_FRAME]
	assert shown_rows.shown_columns == [ShownColumns.COMPACT]


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
	monkeypatch.setattr(table_display, SHOW_FRAME_NAME, ShownRows().show)
	table = TableDisplay._create(FRAME)

	table.preview()

	assert received_previews == [Preview()]


def format_fake_table(frame: pandas.DataFrame) -> str:
	"""
	Fake text of a Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns, ignored.

	Returns
	-------
	str
		Always the fake text.
	"""
	return FAKE_TEXT


class TableHtmlRecorder:
	"""
	Fake HTML builder recording the columns setting it receives.

	.. versionadded:: 0.1.0
	"""

	def __init__(self) -> None:
		"""
		Start without any recorded call.

		.. versionadded:: 0.1.0
		"""
		self.shown_columns = list[ShownColumns]()

	def format_table_html(self, frame: pandas.DataFrame, shown_columns: ShownColumns) -> str:
		"""
		Record the columns setting and return the fake HTML.

		.. versionadded:: 0.1.0

		Parameters
		----------
		frame
			The columns, ignored.
		shown_columns
			The recorded setting.

		Returns
		-------
		str
			Always the fake HTML.
		"""
		self.shown_columns.append(shown_columns)

		return FAKE_HTML


def test_repr_gives_the_text_of_the_table(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the text of the Table comes from format_table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the text builder with a fake.
	"""
	monkeypatch.setattr(table_display, FORMAT_TABLE_NAME, format_fake_table)
	table = TableDisplay._create(FRAME)

	table_text = repr(table)

	assert table_text == FAKE_TEXT


def test_repr_html_gives_the_html_table_with_every_column(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the notebook HTML of the Table comes from format_table_html, with every column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the HTML builder with a fake.
	"""
	recorder = TableHtmlRecorder()
	monkeypatch.setattr(table_display, FORMAT_TABLE_HTML_NAME, recorder.format_table_html)
	table = TableDisplay._create(FRAME)

	table_html = table._repr_html_()

	assert table_html == FAKE_HTML
	assert recorder.shown_columns == [ShownColumns.ALL]
