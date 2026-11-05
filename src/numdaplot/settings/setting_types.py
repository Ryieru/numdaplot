"""
Check that a method receives an object and not its class.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_setting_type_error import InvalidSettingTypeError


def require_object_not_class(setting_name: str, expected: str, value: object) -> None:
	"""
	Check that a setting receives an object and not its class, such as ``ndp.Sum()`` and not ``ndp.Sum``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	setting_name
		The setting and what owns it, such as ``"compute statistic"``.
	expected
		What the setting accepts, such as ``"a statistic such as ndp.Mean()"``.
	value
		The received value.

	Raises
	------
	InvalidSettingTypeError
		When the value is a class, with a message adding the parentheses.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.settings.setting_types import require_object_not_class
	>>> try:
	... 	require_object_not_class("compute statistic", "a statistic such as ndp.Mean()", ndp.Mean)
	... except ndp.InvalidSettingTypeError as error:
	... 	print(error)
	ndp.Mean is a class, use ndp.Mean() instead.
	"""
	if isinstance(value, type):
		raise InvalidSettingTypeError(setting_name, expected, value)
