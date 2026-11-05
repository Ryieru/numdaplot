"""
Functional tests of the base classes of numdaplot, as a user creates and uses them.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp

PRICES = [12.0, 15.5]
DRAW_SHAPE = ndp.Shape((2,))
BASE_CLASS_MESSAGES = [
	(ndp.Rule, "Creating a Rule with ndp.Rule() is not available, use a rule such as ndp.Greater instead."),
	(
		ndp.Statistic,
		"Creating a Statistic with ndp.Statistic() is not available, use a statistic such as ndp.Mean instead.",
	),
	(
		ndp.MathFunction,
		"Creating a MathFunction with ndp.MathFunction() is not available, use a math function such as "
		"ndp.SquareRoot instead.",
	),
	(
		ndp.TimeFunction,
		"Creating a TimeFunction with ndp.TimeFunction() is not available, use a time function such as "
		"ndp.DatePart instead.",
	),
	(
		ndp.Distribution,
		"Creating a Distribution with ndp.Distribution() is not available, use a distribution such as "
		"ndp.Uniform instead.",
	),
	(ndp.Chart, "Creating a Chart with ndp.Chart() is not available, use a chart such as ndp.LineChart instead."),
]
EXPECTED_DISTRIBUTION_MESSAGE = (
	"The distribution CustomDistribution is not available, use a distribution of numdaplot instead."
)
EXPECTED_CUSTOM_CHART_MESSAGE = "The chart CustomChart with plot_bar is not available, use a BarChart instead."
EXPECTED_LINE_CHART_MESSAGE = "The chart LineChart with add_bar is not available, use a BarChart instead."


class CustomDistribution(ndp.Distribution):
	"""
	A distribution written outside numdaplot.

	.. versionadded:: 0.1.0
	"""


class CustomChart(ndp.Chart):
	"""
	A chart written outside numdaplot.

	.. versionadded:: 0.1.0
	"""


@pytest.mark.parametrize(("base_class", "expected_message"), BASE_CLASS_MESSAGES)
def test_base_class_creation_points_to_its_subclasses(base_class: type, expected_message: str) -> None:
	"""
	Check that creating a base class names one of its subclasses.

	.. versionadded:: 0.1.0

	Parameters
	----------
	base_class
		The base class created.
	expected_message
		The message naming a subclass.
	"""
	with pytest.raises(ndp.RefusedOperationError) as error_info:
		base_class()

	message = str(error_info.value)
	assert message == expected_message


def test_random_refuses_a_distribution_written_outside_numdaplot() -> None:
	"""
	Check that Array.random names the distributions of numdaplot.

	.. versionadded:: 0.1.0
	"""
	distribution = CustomDistribution()

	with pytest.raises(ndp.RefusedOperationError) as error_info:
		# The type checker refuses this call too, as it does in the editor of a user.
		ndp.Array.random(distribution, shape=DRAW_SHAPE)  # pyright: ignore[reportArgumentType]

	message = str(error_info.value)
	assert message == EXPECTED_DISTRIBUTION_MESSAGE


def test_plot_function_refuses_a_chart_written_outside_numdaplot() -> None:
	"""
	Check that plot_bar names the chart it draws.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)
	chart = CustomChart()

	with pytest.raises(ndp.RefusedOperationError) as error_info:
		# The type checker refuses this call too, as it does in the editor of a user.
		ndp.plot_bar(prices, chart)  # pyright: ignore[reportArgumentType]

	message = str(error_info.value)
	assert message == EXPECTED_CUSTOM_CHART_MESSAGE


def test_add_method_refuses_the_chart_of_another_method() -> None:
	"""
	Check that add_bar names the chart it draws when it receives a LineChart.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)
	plot = ndp.plot_bar(prices, ndp.BarChart())
	line = ndp.LineChart()

	with pytest.raises(ndp.RefusedOperationError) as error_info:
		# The type checker refuses this call too, as it does in the editor of a user.
		plot.add_bar(prices, line)  # pyright: ignore[reportArgumentType]

	message = str(error_info.value)
	assert message == EXPECTED_LINE_CHART_MESSAGE
