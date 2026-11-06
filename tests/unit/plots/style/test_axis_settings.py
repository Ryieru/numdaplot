"""
Unit tests of the check of the style of a chart without axes.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import pytest

import numdaplot as ndp
from numdaplot.plots.style.axis_settings import require_no_axis_settings


def test_require_no_axis_settings_accepts_a_title() -> None:
	"""
	Check that a pie style may have a title.

	.. versionadded:: 0.1.0
	"""
	require_no_axis_settings(ndp.PlotStyle(title="Sales"))


def test_require_no_axis_settings_accepts_no_style() -> None:
	"""
	Check that the default style passes.

	.. versionadded:: 0.1.0
	"""
	require_no_axis_settings(None)


@pytest.mark.parametrize(
	"style",
	[
		ndp.PlotStyle(y_label="Sales"),
		ndp.PlotStyle(right_label="Price"),
		ndp.PlotStyle(x_tick_rotation=45),
		ndp.PlotStyle(y_tick_rotation=45),
	],
)
def test_require_no_axis_settings_rejects_every_axis_setting(style: ndp.PlotStyle) -> None:
	"""
	Check that each axis setting raises RefusedSettingError for a pie.

	.. versionadded:: 0.1.0

	Parameters
	----------
	style
		A style with one axis setting.
	"""
	with pytest.raises(ndp.RefusedSettingError):
		require_no_axis_settings(style)
