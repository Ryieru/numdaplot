"""
Error raised when a value has no new value in a ValueMapping, or is in no bracket of Brackets.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

VALUE_MAPPING_NAME = "ValueMapping"
BRACKETS_NAME = "Brackets"
UNMATCHED_MESSAGES = {
	VALUE_MAPPING_NAME: (
		"The value {value!r} has no ValueChange. Add one, or give others=Unmatched.MISSING to make it missing, or "
		"others=Unmatched.KEEP to keep it."
	),
	BRACKETS_NAME: (
		"The value {value!r} is in no bracket. Open the first or the last bracket, or give others=Unmatched.MISSING "
		"to make it missing."
	),
}


class UnmatchedValueError(NumdaplotError):
	"""
	Raised when a value has no new value in a ``ValueMapping``, or is in no bracket of ``Brackets``.

	Both raise it while their ``others`` is ``Unmatched.ERROR``.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		The message of a ``ValueMapping`` also offers ``others=Unmatched.KEEP``.

	Parameters
	----------
	value
		The first value without new value or bracket.
	setting_name
		``"ValueMapping"`` by default, or ``"Brackets"``: the setting that found no match, which chooses the advice.

	Attributes
	----------
	value
		The first value without new value or bracket.
	setting_name
		The setting that found no match.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> sexes = ndp.Array.from_list([1, 2, 3])
	>>> try:
	... 	sexes.apply(ndp.ValueMapping(changes=[ndp.ValueChange(1, "Homme"), ndp.ValueChange(2, "Femme")]))
	... except ndp.UnmatchedValueError as error:
	... 	print(error)
	The value 3 has no ValueChange. Add one, or give others=Unmatched.MISSING to make it missing,
	or others=Unmatched.KEEP to keep it.
	>>> ages = ndp.Table.from_arrays({"age": ndp.Array.from_list([5, 105])})
	>>> brackets = ndp.Brackets(limits=[0, 18, 100])
	>>> try:
	... 	ages.convert(ndp.Conversion(column="age", dtype=ndp.Type.CATEGORY, format=brackets))
	... except ndp.UnmatchedValueError as error:
	... 	print(error)
	The value 105 is in no bracket. Open the first or the last bracket,
	or give others=Unmatched.MISSING to make it missing.
	"""

	def __init__(self, value: object, setting_name: str = VALUE_MAPPING_NAME) -> None:
		"""
		Build the error message from the value and the setting that found no match.

		.. versionadded:: 0.1.0

		Parameters
		----------
		value
			The first value without new value or bracket.
		setting_name
			The setting that found no match, ``"ValueMapping"`` by default.
		"""
		message_template = UNMATCHED_MESSAGES[setting_name]
		message = message_template.format(value=value)
		super().__init__(message)

		self.value = value
		self.setting_name = setting_name
