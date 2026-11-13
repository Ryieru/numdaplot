"""
Error raised when a missing value is given for a type that cannot hold one.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

BOOL_TYPE_NAME = "BOOL"
LIST_MESSAGE = "{type_name} values cannot be missing in an Array. {advice}"
COLUMN_MESSAGE = (
	"The column {column_name!r} has missing values, which {article} {type_name} Array cannot hold. {advice}"
)
ARTICLE_BEFORE_VOWEL = "an"
ARTICLE = "a"
VOWELS = "AEIOU"
LIST_ADVICE = "Remove them."
LIST_DECIMAL_ADVICE = "Remove them, or give dtype=ndp.Type.FLOAT64."
COLUMN_ADVICE = "Remove them with drop_missing."
COLUMN_DECIMAL_ADVICE = "Remove them with drop_missing, or convert the column to FLOAT64."


class UnsupportedMissingError(NumdaplotError):
	"""
	Raised when a missing value (``None``) is given for a type that cannot hold one in an Array.

	Only integers and booleans cannot be missing in an Array. A Table accepts their missing values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	type_name
		Name of the ``ndp.Type`` member that cannot hold a missing value.
	column_name
		Name of the Table column holding the missing values. When omitted, the values were given to an Array.
	advice
		What to do instead, for values given to an Array by an operation that has its own solution. When omitted,
		the advice of ``Array.from_list``.

	Attributes
	----------
	type_name
		Name of the ``ndp.Type`` member that cannot hold a missing value.
	column_name
		Name of the Table column holding the missing values, or ``None`` for values given to an Array.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Array.from_list([1, None])
	... except ndp.UnsupportedMissingError as error:
	... 	print(error)
	INT64 values cannot be missing in an Array. Remove them, or give dtype=ndp.Type.FLOAT64.
	"""

	def __init__(self, type_name: str, column_name: str | None = None, advice: str | None = None) -> None:
		"""
		Build the error message from the type name, the column name and the advice.

		.. versionadded:: 0.1.0

		Parameters
		----------
		type_name
			Name of the ``ndp.Type`` member that cannot hold a missing value.
		column_name
			Name of the Table column holding the missing values. When omitted, the values were given to an Array.
		advice
			What to do instead, for values given to an Array. When omitted, the advice of ``Array.from_list``.
		"""
		message = write_missing_message(type_name, column_name, advice)
		super().__init__(message)

		self.type_name = type_name
		self.column_name = column_name


def write_missing_message(type_name: str, column_name: str | None, advice: str | None = None) -> str:
	"""
	Return the message of the error, with the solutions that apply to the type.

	Whole numbers can become decimals, which hold missing values. Booleans cannot.

	.. versionadded:: 0.1.0

	Parameters
	----------
	type_name
		Name of the ``ndp.Type`` member that cannot hold a missing value.
	column_name
		Name of the Table column holding the missing values, or ``None`` for values given to an Array.
	advice
		What to do instead, for values given to an Array. When omitted, the advice of ``Array.from_list``.

	Returns
	-------
	str
		The message.

	Examples
	--------
	>>> from numdaplot.errors.types.unsupported_missing_error import write_missing_message
	>>> write_missing_message("BOOL", None)
	'BOOL values cannot be missing in an Array. Remove them.'
	>>> write_missing_message("BOOL", "paid")
	"The column 'paid' has missing values, which a BOOL Array cannot hold. Remove them with drop_missing."
	"""
	converts_to_decimal = type_name != BOOL_TYPE_NAME
	if column_name is None:
		list_advice = LIST_DECIMAL_ADVICE if converts_to_decimal else LIST_ADVICE
		if advice is not None:
			list_advice = advice

		list_message = LIST_MESSAGE.format(type_name=type_name, advice=list_advice)
		return list_message

	column_advice = COLUMN_DECIMAL_ADVICE if converts_to_decimal else COLUMN_ADVICE
	first_letter = type_name[0]
	article = ARTICLE_BEFORE_VOWEL if first_letter in VOWELS else ARTICLE
	column_message = COLUMN_MESSAGE.format(
		column_name=column_name,
		article=article,
		type_name=type_name,
		advice=column_advice,
	)

	return column_message
