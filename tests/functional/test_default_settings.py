"""
Functional tests of the settings a user may omit, and of the settings that are always needed.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp

CITIES = ["Paris", "Lyon", "Paris", "Pau", "Nice", "Lille"]
PRICES = [120.0, None, 120.0, 90.0, 80.0, 70.0]
EXPECTED_EMPTY_REGION_MESSAGE = "A Region needs rows, columns or both, got neither."


def build_sales() -> ndp.Table:
	"""
	Return a Table of six sales with a duplicated row and a missing price.

	.. versionadded:: 0.1.0

	Returns
	-------
	Table
		The sales.
	"""
	cities = ndp.Array.from_list(CITIES)
	prices = ndp.Array.from_list(PRICES)
	sales = ndp.Table.from_arrays({"city": cities, "price": prices})

	return sales


def test_preview_without_settings_shows_the_first_five_rows(capsys: pytest.CaptureFixture[str]) -> None:
	"""
	Check that preview without settings shows what preview with the default Preview shows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	capsys
		Captures the printed rows.
	"""
	sales = build_sales()

	sales.preview()
	short_capture = capsys.readouterr()
	sales.preview(ndp.Preview())
	explicit_capture = capsys.readouterr()

	assert short_capture.out == explicit_capture.out


def test_table_methods_without_settings_match_their_default_settings() -> None:
	"""
	Check describe, drop_duplicates, drop_missing and count_missing without settings.

	.. versionadded:: 0.1.0
	"""
	sales = build_sales()

	short_results = [sales.describe(), sales.drop_duplicates(), sales.drop_missing(), sales.count_missing()]

	explicit_results = [
		sales.describe(ndp.Description()),
		sales.drop_duplicates(ndp.Deduplication()),
		sales.drop_missing(ndp.MissingDrop()),
		sales.count_missing(ndp.MissingCount()),
	]
	for short_result, explicit_result in zip(short_results, explicit_results, strict=True):
		equality = ndp.Equality(other=explicit_result)
		is_same = short_result.is_equal(equality)
		assert is_same


def test_sort_without_settings_sorts_in_ascending_order() -> None:
	"""
	Check that sort without settings matches sort with the default ArraySorting.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)

	sorted_prices = prices.sort()

	expected_prices = prices.sort(ndp.ArraySorting())
	equality = ndp.Equality(other=expected_prices)
	is_same = sorted_prices.is_equal(equality)
	assert is_same


def test_plot_functions_without_chart_draw_an_array() -> None:
	"""
	Check that plot_line and add_bar draw an Array without chart.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list([12.0, 15.5, 14.0])

	line_plot = ndp.plot_line(prices)
	plot = line_plot.add_bar(prices)

	figure = plot.to_matplotlib()
	drawn_line_count = len(figure.axes[0].lines)
	assert drawn_line_count == 1


def test_empty_region_is_refused() -> None:
	"""
	Check that a Region without rows and columns names what it needs.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.EmptyRegionError) as error_info:
		ndp.Region()

	message = str(error_info.value)
	assert message == EXPECTED_EMPTY_REGION_MESSAGE


def test_pie_chart_needs_its_labels_and_values() -> None:
	"""
	Check that a PieChart without labels and values cannot be created.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(TypeError):
		# The type checker refuses this call too, as it does in the editor of a user.
		ndp.PieChart()  # pyright: ignore[reportCallIssue]
