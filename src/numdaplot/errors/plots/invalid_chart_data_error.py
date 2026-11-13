"""
Error raised when the columns given to a chart do not fit the data it draws.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

MISSING_SETTING_MESSAGE = "{chart_name} needs {setting_name} for {data_name}."
EXTRA_SETTING_MESSAGE = "{chart_name} takes no {setting_name} for {data_name}."


class InvalidChartDataError(NumdaplotError):
	"""
	Raised when a chart misses a column setting a Table needs, or has one an Array does not use.

	A Table needs the ``y`` columns of a chart, while an Array draws each of its columns and takes no column name.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart_name
		Name of the chart class, such as ``LineChart``.
	setting_name
		Name of the setting, such as ``y``.
	data_name
		The data drawn: ``a Table`` or ``an Array``.
	needs_setting
		True when the setting is missing, False when it is given but not used.

	Attributes
	----------
	chart_name
		Name of the chart class, such as ``LineChart``.
	setting_name
		Name of the setting, such as ``y``.
	data_name
		The data drawn: ``a Table`` or ``an Array``.
	needs_setting
		True when the setting is missing, False when it is given but not used.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> chart = ndp.LineChart(y=["price"])
	>>> try:
	... 	ndp.Plot.line(prices, chart)
	... except ndp.InvalidChartDataError as error:
	... 	print(error)
	LineChart takes no y for an Array.
	"""

	def __init__(self, chart_name: str, setting_name: str, data_name: str, needs_setting: bool) -> None:
		"""
		Build the error message from the chart, the setting and whether it is missing or extra.

		.. versionadded:: 0.1.0

		Parameters
		----------
		chart_name
			Name of the chart class, such as ``LineChart``.
		setting_name
			Name of the setting, such as ``y``.
		data_name
			The data drawn: ``a Table`` or ``an Array``.
		needs_setting
			True when the setting is missing, False when it is given but not used.
		"""
		message_template = EXTRA_SETTING_MESSAGE
		if needs_setting:
			message_template = MISSING_SETTING_MESSAGE

		message = message_template.format(chart_name=chart_name, setting_name=setting_name, data_name=data_name)
		super().__init__(message)
		self.chart_name = chart_name
		self.setting_name = setting_name
		self.data_name = data_name
		self.needs_setting = needs_setting
