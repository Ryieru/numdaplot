"""
Functional tests of the constructors of Array, Table and Plot, refused as a user calls them.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

import numdaplot as ndp

PRICES = [12.0, 15.5]
EXPECTED_ARRAY_MESSAGE = (
	"Creating an Array with ndp.Array(...) is not available, use ndp.Array.from_list, from_numpy, filled, "
	"from_range, from_spacing or random instead."
)
EXPECTED_TABLE_MESSAGE = (
	"Creating a Table with ndp.Table(...) is not available, use ndp.Table.from_arrays, from_pandas "
	"or a file method such as from_csv instead."
)
EXPECTED_PLOT_MESSAGE = (
	"Creating a Plot with ndp.Plot(...) is not available, use ndp.Plot.line, bar, scatter, histogram, box, pie, "
	"heatmap, missing_by_column or missing_map instead."
)


def test_array_constructor_points_to_the_from_methods() -> None:
	"""
	Check that ndp.Array called on a numpy array names the from_* methods.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(PRICES)

	with pytest.raises(ndp.RefusedOperationError) as error_info:
		# The type checker refuses this call too, as it does in the editor of a user.
		ndp.Array(values)  # pyright: ignore[reportArgumentType]

	message = str(error_info.value)
	assert message == EXPECTED_ARRAY_MESSAGE


def test_table_constructor_points_to_the_from_methods() -> None:
	"""
	Check that ndp.Table called on columns names the from_* methods.

	.. versionadded:: 0.1.0
	"""
	columns = {"price": PRICES}

	with pytest.raises(ndp.RefusedOperationError) as error_info:
		# The type checker refuses this call too, as it does in the editor of a user.
		ndp.Table(columns)  # pyright: ignore[reportArgumentType]

	message = str(error_info.value)
	assert message == EXPECTED_TABLE_MESSAGE


def test_plot_constructor_points_to_the_creation_methods() -> None:
	"""
	Check that ndp.Plot called directly names the creation methods.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.RefusedOperationError) as error_info:
		ndp.Plot()

	message = str(error_info.value)
	assert message == EXPECTED_PLOT_MESSAGE
