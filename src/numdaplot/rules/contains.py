"""
Rule keeping the texts that contain a given text.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.empty_text_error import EmptyTextError
from numdaplot.rules.case import Case
from numdaplot.rules.rule import Rule


@dataclass(frozen=True)
class Contains(Rule):
	"""
	Keep the texts that contain a given text. Applies to text values only.

	.. versionadded:: 0.1.0

	Parameters
	----------
	text
		The text to look for, anywhere in each value. It cannot be empty.
	case
		Whether upper and lower case are distinguished. Sensitive by default.

	Raises
	------
	EmptyTextError
		When ``text`` is empty.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Contains("paris")
	Contains(text='paris', case=<Case.SENSITIVE: 1>)
	"""

	text: str
	case: Case = Case.SENSITIVE

	def __post_init__(self) -> None:
		"""
		Check that the searched text is not empty.

		.. versionadded:: 0.1.0

		Raises
		------
		EmptyTextError
			When ``text`` is empty.
		"""
		if self.text == "":
			raise EmptyTextError()
