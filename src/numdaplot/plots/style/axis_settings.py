"""
Check of the style of a chart without axes.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.plots.style.plot_style import PlotStyle

CHART_NAME = "PieChart"
X_LABEL_SETTING = "x_label"
Y_LABEL_SETTING = "y_label"
RIGHT_LABEL_SETTING = "right_label"
X_TICK_ROTATION_SETTING = "x_tick_rotation"
Y_TICK_ROTATION_SETTING = "y_tick_rotation"


def require_no_axis_settings(style: PlotStyle | None) -> None:
	"""
	Check that the style of a pie has no axis setting, a pie having no axes.

	The grid lines and the legend keep their default values, so a pie leaves them without effect.

	.. versionadded:: 0.1.0

	Parameters
	----------
	style
		The style given, or None.

	Raises
	------
	RefusedSettingError
		When the style has an ``x_label``, a ``y_label``, a ``right_label``, an ``x_tick_rotation`` or a
		``y_tick_rotation``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.style.axis_settings import require_no_axis_settings
	>>> try:
	... 	require_no_axis_settings(ndp.PlotStyle(x_tick_rotation=45))
	... except ndp.RefusedSettingError as error:
	... 	print(error)
	PieChart does not accept x_tick_rotation.
	"""
	if style is None:
		return

	axis_settings = [
		(X_LABEL_SETTING, style.x_label),
		(Y_LABEL_SETTING, style.y_label),
		(RIGHT_LABEL_SETTING, style.right_label),
		(X_TICK_ROTATION_SETTING, style.x_tick_rotation),
		(Y_TICK_ROTATION_SETTING, style.y_tick_rotation),
	]

	for setting_name, setting_value in axis_settings:
		if setting_value is not None:
			raise RefusedSettingError(setting_name, CHART_NAME)
