"""
Unit tests of Chart.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.settings.refused_operation_error import RefusedOperationError
from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.line_chart import LineChart


class CustomChart(Chart):
	"""
	A Chart written outside numdaplot.

	.. versionadded:: 0.1.0
	"""


def test_chart_refuses_its_own_creation() -> None:
	"""
	Check that creating the base class itself raises RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedOperationError):
		Chart()


def test_chart_lets_a_subclass_of_numdaplot_be_created() -> None:
	"""
	Check that a subclass of numdaplot is created.

	.. versionadded:: 0.1.0
	"""
	created = LineChart()

	assert isinstance(created, Chart)


def test_chart_lets_a_subclass_written_outside_numdaplot_be_created() -> None:
	"""
	Check that a subclass without its own constructor is created.

	.. versionadded:: 0.1.0
	"""
	created = CustomChart()

	assert isinstance(created, Chart)
