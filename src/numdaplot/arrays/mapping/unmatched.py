"""
What happens to a value that no setting gives a new value.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Unmatched(Enum):
	"""
	What happens to a value of an Array that a ``ValueMapping`` gives no new value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> sexes = ndp.Array.from_list([1, 2, 9])
	>>> changes = [ndp.ValueChange(1, "Homme"), ndp.ValueChange(2, "Femme")]
	>>> sexes.apply(ndp.ValueMapping(changes=changes, others=ndp.Unmatched.MISSING))
	Array(['Homme', 'Femme', nan], dtype=TEXT)
	"""

	ERROR = auto()
	"""
	The value raises ``UnmatchedValueError``. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> sexes = ndp.Array.from_list([1, 9])
	>>> try:
	... 	sexes.apply(ndp.ValueMapping(changes=[ndp.ValueChange(1, "Homme")], others=ndp.Unmatched.ERROR))
	... except ndp.UnmatchedValueError as error:
	... 	print(error)
	The value 9 has no ValueChange. Add one, or give others=Unmatched.MISSING to make it missing,
	or others=Unmatched.KEEP to keep it.
	"""

	MISSING = auto()
	"""
	The value becomes missing.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> sexes = ndp.Array.from_list([1, 9])
	>>> sexes.apply(ndp.ValueMapping(changes=[ndp.ValueChange(1, "Homme")], others=ndp.Unmatched.MISSING))
	Array(['Homme', nan], dtype=TEXT)
	"""

	KEEP = auto()
	"""
	The value stays as it is, so that only the listed values change. The result takes the type that holds both the
	values of the Array and the new values. ``Brackets`` refuses it, as a number cannot name a bracket.

	.. versionadded:: 0.2.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> answers = ndp.Array.from_list([1.0, 7.0, 3.0, 9.0])
	>>> unknown_answers = [ndp.ValueChange(7, None), ndp.ValueChange(9, None)]
	>>> answers.apply(ndp.ValueMapping(changes=unknown_answers, others=ndp.Unmatched.KEEP))
	Array([ 1., nan,  3., nan], dtype=FLOAT64)
	"""
