"""
Functional tests of the display of a Plot or a Figure without window.

The tests run with the matplotlib backend set by ``conftest.py``, which opens no window.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp

PRICES = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
PLOT_ADVICE = "save it with Plot.save"
FIGURE_ADVICE = "save it with Figure.save"


def test_showing_a_plot_without_window_warns_at_the_user_line() -> None:
	"""
	Check that Plot.show emits a DisplayWarning naming this file and Plot.save.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.bar(PRICES)

	with pytest.warns(ndp.DisplayWarning, match=PLOT_ADVICE) as caught_warnings:
		plot.show()

	warning_file = caught_warnings[0].filename
	assert warning_file == __file__


def test_showing_a_figure_without_window_warns_at_the_user_line() -> None:
	"""
	Check that Figure.show emits a DisplayWarning naming this file and Figure.save.

	.. versionadded:: 0.1.0
	"""
	plot = ndp.Plot.bar(PRICES)
	empty_figure = ndp.Figure(ndp.Layout(rows=1, columns=1))
	figure = empty_figure.place(plot, ndp.Cell(row=0, column=0))

	with pytest.warns(ndp.DisplayWarning, match=FIGURE_ADVICE) as caught_warnings:
		figure.show()

	warning_file = caught_warnings[0].filename
	assert warning_file == __file__
