"""
Natural order of texts, which reads the numbers inside them as numbers.

.. versionadded:: 0.2.0
"""

import re

DIGIT_RUN = re.compile(r"(\d+)")


def find_natural_key(text: str) -> tuple[list[int | str], str]:
	"""
	Return the key sorting texts in natural order: numbers as numbers, without regard to case.

	The parts of a text alternate between letters and digits, so two keys always compare parts of the same kind.
	Texts equal but for their case, or for leading zeros, keep the order of the texts themselves.

	.. versionadded:: 0.2.0

	Parameters
	----------
	text
		The text to sort.

	Returns
	-------
	tuple[list[int | str], str]
		The parts of the text in lower case, each run of digits as its number, then the text itself.

	Examples
	--------
	>>> from numdaplot.ordering.natural_order import find_natural_key
	>>> sorted(["Cluster 10", "noise", "Cluster 2"], key=find_natural_key)
	['Cluster 2', 'Cluster 10', 'noise']
	"""
	folded_text = text.casefold()
	text_parts = DIGIT_RUN.split(folded_text)
	key_parts = list[int | str]()

	for text_part in text_parts:
		if text_part.isdecimal():
			number = int(text_part)
			key_parts.append(number)
			continue

		key_parts.append(text_part)

	natural_key = (key_parts, text)

	return natural_key
