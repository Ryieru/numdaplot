"""
Error raised when a key appears several times where a join expects it once.

.. versionadded:: 0.1.0
"""

from typing import Any

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.repeated_key import RepeatedKey

JOIN_RELATION_MESSAGE = (
	"Expected each key of {table_name} to appear once for {relation_name}, but {key_names} {key_values} appears "
	"{count} times."
)
VALUE_SEPARATOR = ", "
COMBINATION_FORMAT = "({joined_values})"
SINGLE_KEY_COUNT = 1


class JoinRelationError(NumdaplotError):
	"""
	Raised when a key appears several times in a Table of a join whose ``Relation`` expects it once.

	For example, ``Relation.ONE_TO_MANY`` expects each key once in the left Table, the one joined.

	.. versionadded:: 0.1.0

	Parameters
	----------
	relation_name
		The relation checked, such as ``"Relation.ONE_TO_MANY"``.
	table_name
		The Table holding the repeated key: ``"the left Table"`` or ``"the right Table"``.
	repeated_key
		The first repeated key, its values and its number of rows.

	Attributes
	----------
	relation_name
		The relation checked.
	table_name
		The Table holding the repeated key.
	repeated_key
		The first repeated key, its values and its number of rows.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> accidents = ndp.Table.from_arrays({"Num_Acc": ndp.Array.from_list([101, 101])})
	>>> users = ndp.Table.from_arrays({"Num_Acc": ndp.Array.from_list([101])})
	>>> try:
	... 	accidents.join(ndp.Join(other=users, keys=["Num_Acc"], relation=ndp.Relation.ONE_TO_MANY))
	... except ndp.JoinRelationError as error:
	... 	print(error)
	Expected each key of the left Table to appear once for Relation.ONE_TO_MANY, but 'Num_Acc' 101 appears 2 times.
	"""

	def __init__(self, relation_name: str, table_name: str, repeated_key: RepeatedKey) -> None:
		"""
		Build the error message from the relation, the Table and the repeated key.

		.. versionadded:: 0.1.0

		Parameters
		----------
		relation_name
			The relation checked.
		table_name
			The Table holding the repeated key.
		repeated_key
			The first repeated key, its values and its number of rows.
		"""
		key_names = format_key_names(repeated_key.key_names)
		key_values = format_key_values(repeated_key.key_values)
		message = JOIN_RELATION_MESSAGE.format(
			table_name=table_name,
			relation_name=relation_name,
			key_names=key_names,
			key_values=key_values,
			count=repeated_key.count,
		)
		super().__init__(message)

		self.relation_name = relation_name
		self.table_name = table_name
		self.repeated_key = repeated_key


def format_key_names(key_names: list[str]) -> str:
	"""
	Return the names of the key columns as written in the message: one name, or the combination of several.

	.. versionadded:: 0.1.0

	Parameters
	----------
	key_names
		The names of the key columns.

	Returns
	-------
	str
		``'Num_Acc'`` for one key, ``('Num_Acc', 'id_vehicule')`` for several.

	Examples
	--------
	>>> from numdaplot.errors.join_relation_error import format_key_names
	>>> format_key_names(["Num_Acc"]), format_key_names(["Num_Acc", "id_vehicule"])
	("'Num_Acc'", "('Num_Acc', 'id_vehicule')")
	"""
	quoted_names = [repr(key_name) for key_name in key_names]
	names_text = format_combination(quoted_names)

	return names_text


def format_key_values(key_values: list[Any]) -> str:
	"""
	Return the values of a key as written in the message, texts in quotes.

	.. versionadded:: 0.1.0

	Parameters
	----------
	key_values
		The value of each key column.

	Returns
	-------
	str
		``202500000001`` for one key, ``(202500000001, 'A01')`` for several.

	Examples
	--------
	>>> from numdaplot.errors.join_relation_error import format_key_values
	>>> format_key_values([202500000001, "A01"])
	"(202500000001, 'A01')"
	"""
	value_texts = list[str]()

	for key_value in key_values:
		value_text = str(key_value)
		if isinstance(key_value, str):
			value_text = repr(key_value)

		value_texts.append(value_text)

	values_text = format_combination(value_texts)

	return values_text


def format_combination(texts: list[str]) -> str:
	"""
	Return a single text as it is, or several texts between parentheses.

	.. versionadded:: 0.1.0

	Parameters
	----------
	texts
		The text of each key column.

	Returns
	-------
	str
		The single text, or the texts separated by commas between parentheses.

	Examples
	--------
	>>> from numdaplot.errors.join_relation_error import format_combination
	>>> format_combination(["101"]), format_combination(["101", "'A01'"])
	('101', "(101, 'A01')")
	"""
	text_count = len(texts)
	if text_count == SINGLE_KEY_COUNT:
		return texts[0]

	joined_values = VALUE_SEPARATOR.join(texts)
	combination = COMBINATION_FORMAT.format(joined_values=joined_values)

	return combination
