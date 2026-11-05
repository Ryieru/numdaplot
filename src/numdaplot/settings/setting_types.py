"""
Check of the kind of value a setting receives.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_setting_type_error import InvalidSettingTypeError

LIST_EXPECTED = "a list such as [{text!r}]"


def require_setting_type(setting_name: str, expected: str, value: object, accepted_types: tuple[type, ...]) -> None:
	"""
	Check that a setting receives a value of one of the accepted kinds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	setting_name
		The setting and what owns it, such as ``"Region rows"``.
	expected
		What the setting accepts, shown in the error message, such as ``"an Index, a Range or None"``.
	value
		The received value.
	accepted_types
		The accepted classes, with ``type(None)`` when the setting may be omitted.

	Raises
	------
	InvalidSettingTypeError
		When the value is of none of the accepted kinds.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.settings.setting_types import require_setting_type
	>>> try:
	... 	require_setting_type("Preview side", "a Side such as Side.END", "end", (ndp.Side,))
	... except ndp.InvalidSettingTypeError as error:
	... 	print(error)
	Preview side expects a Side such as Side.END, got 'end'.
	"""
	is_accepted = isinstance(value, accepted_types)
	if not is_accepted:
		raise InvalidSettingTypeError(setting_name, expected, value)


def require_list_not_text(setting_name: str, value: object) -> None:
	"""
	Check that a setting expecting a list does not receive a single text, which would be read letter by letter.

	.. versionadded:: 0.1.0

	Parameters
	----------
	setting_name
		The setting and what owns it, such as ``"BarChart y"``.
	value
		The received value.

	Raises
	------
	InvalidSettingTypeError
		When the value is a text, with a message showing the text inside a list.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.settings.setting_types import require_list_not_text
	>>> try:
	... 	require_list_not_text("BarChart y", "price")
	... except ndp.InvalidSettingTypeError as error:
	... 	print(error)
	BarChart y expects a list such as ['price'], got 'price'.
	"""
	if isinstance(value, str):
		expected = LIST_EXPECTED.format(text=value)
		raise InvalidSettingTypeError(setting_name, expected, value)


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
