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
	The value 9 has no ValueChange. Add one, or give others=Unmatched.MISSING to make it missing.
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
