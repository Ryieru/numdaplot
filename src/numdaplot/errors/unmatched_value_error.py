"""
Error raised when a value has no new value in a ValueMapping, or is in no bracket of Brackets.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

VALUE_MAPPING_NAME = "ValueMapping"
BRACKETS_NAME = "Brackets"
UNMATCHED_MESSAGES = {
	VALUE_MAPPING_NAME: (
		"The value {value!r}{column_text} has no ValueChange. Add one, or give others=Unmatched.MISSING to make it "
		"missing, or others=Unmatched.KEEP to keep it."
	),
	BRACKETS_NAME: (
		"The value {value!r}{column_text} is in no bracket. Open the first or the last bracket, or give "
		"others=Unmatched.MISSING to make it missing."
	),
}
COLUMN_TEXT = " of the column {column_name!r}"
NO_COLUMN_TEXT = ""


class UnmatchedValueError(NumdaplotError):
	"""
	Raised when a value has no new value in a ``ValueMapping``, or is in no bracket of ``Brackets``.

	Both raise it while their ``others`` is ``Unmatched.ERROR``.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		The message of a ``ValueMapping`` also offers ``others=Unmatched.KEEP``. The message names the Table column
		holding the value.

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
	column_name
		Name of the Table column holding the value, or ``None`` for the values of an Array.

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
	... 	ages.convert(ndp.TableConversion(column="age", dtype=ndp.Type.CATEGORY, format=brackets))
	... except ndp.UnmatchedValueError as error:
	... 	print(error)
	The value 105 of the column 'age' is in no bracket. Open the first or the last bracket,
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
		self.value = value
		self.setting_name = setting_name
		self.column_name: str | None = None
		message = self.write_message(NO_COLUMN_TEXT)
		super().__init__(message)

	def write_message(self, column_text: str) -> str:
		"""
		Return the message, with the advice of the setting that found no match.

		.. versionadded:: 0.2.0

		Parameters
		----------
		column_text
			The words naming the column after the value, or an empty text.

		Returns
		-------
		str
			The message.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> print(ndp.UnmatchedValueError(105, "Brackets").write_message(""))
		The value 105 is in no bracket. Open the first or the last bracket,
		or give others=Unmatched.MISSING to make it missing.
		"""
		message_template = UNMATCHED_MESSAGES[self.setting_name]
		message = message_template.format(value=self.value, column_text=column_text)

		return message

	def name_column(self, column_name: str) -> None:
		"""
		Name the Table column holding the value in the message, unless a column is already named.

		.. versionadded:: 0.2.0

		Parameters
		----------
		column_name
			The name of the column.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> error = ndp.UnmatchedValueError(3)
		>>> error.name_column("sex")
		>>> print(error)
		The value 3 of the column 'sex' has no ValueChange. Add one,
		or give others=Unmatched.MISSING to make it missing, or others=Unmatched.KEEP to keep it.
		"""
		if self.column_name is not None:
			return

		self.column_name = column_name
		column_text = COLUMN_TEXT.format(column_name=column_name)
		message = self.write_message(column_text)
		self.args = (message,)
