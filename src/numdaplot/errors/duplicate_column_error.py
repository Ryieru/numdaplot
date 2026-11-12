r"""
Error raised when a column name appears more than once.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

DUPLICATE_COLUMN_MESSAGE = "The column name {column_name!r} appears more than once."
DUPLICATE_CLEANED_MESSAGE = (
	"The column names {first_name!r} and {second_name!r} both become {column_name!r} once cleaned. "
	"Use ColumnNames.KEPT to keep them as written."
)
RESULT_NAME_ADVICE = "Give each Calculation its own result_name."
ADVICE_SEPARATOR = " "


class DuplicateColumnError(NumdaplotError):
	r"""
	Raised when a column name appears twice.

	For example in a file header, in a list of columns, when renaming or adding a column, or when two names of a file
	become the same once their spaces and line breaks are removed.

	.. versionadded:: 0.1.0

	.. versionchanged:: 0.2.0
		Takes an advice, such as giving each ``Calculation`` its own ``result_name``.

	Parameters
	----------
	column_name
		The repeated name.
	original_names
		The two names, as written in the file, that both become ``column_name`` once cleaned. When omitted, the
		name itself appears twice.
	advice
		A sentence added at the end of the message, telling how to avoid the repeated name, no advice when omitted.

	Attributes
	----------
	column_name
		The repeated name.
	original_names
		The two names as written before cleaning, ``None`` when the name itself appears twice.
	advice
		The sentence added at the end of the message, ``None`` without advice.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.ColumnChoice(columns=["price", "price"])
	... except ndp.DuplicateColumnError as error:
	... 	print(error)
	The column name 'price' appears more than once.
	>>> path = Path(tempfile.mkdtemp()) / "sales.csv"
	>>> _ = path.write_text("id,id \n1,2\n")
	>>> try:
	... 	ndp.Table.from_csv(path)
	... except ndp.DuplicateColumnError as error:
	... 	print(error)
	The column names 'id' and 'id ' both become 'id' once cleaned. Use ColumnNames.KEPT to keep them as written.
	>>> first_mean = ndp.Calculation(column="price", function=ndp.Mean())
	>>> second_mean = ndp.Calculation(column="price", function=ndp.Mean())
	>>> try:
	... 	ndp.Aggregation(calculations=[first_mean, second_mean])
	... except ndp.DuplicateColumnError as error:
	... 	print(error)
	The column name 'price_mean' appears more than once. Give each Calculation its own result_name.
	"""

	def __init__(self, column_name: str, original_names: list[str] | None = None, advice: str | None = None) -> None:
		"""
		Build the error message from the column name, from the names before cleaning and from the advice.

		.. versionadded:: 0.1.0

		.. versionchanged:: 0.2.0
			Takes an advice.

		Parameters
		----------
		column_name
			The repeated name.
		original_names
			The two names before cleaning. When omitted, the name itself appears twice.
		advice
			A sentence added at the end of the message, no advice when omitted.
		"""
		message = DUPLICATE_COLUMN_MESSAGE.format(column_name=column_name)
		if original_names is not None:
			first_name, second_name = original_names
			message = DUPLICATE_CLEANED_MESSAGE.format(
				first_name=first_name, second_name=second_name, column_name=column_name
			)

		if advice is not None:
			message = message + ADVICE_SEPARATOR + advice

		super().__init__(message)

		self.column_name = column_name
		self.original_names = original_names
		self.advice = advice
