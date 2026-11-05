"""
Rule keeping the texts that contain a given text.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.empty_text_error import EmptyTextError
from numdaplot.rules.case import Case
from numdaplot.rules.rule import Rule
from numdaplot.settings.field_types import require_field_types


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
	InvalidTypeError
		When a setting is not of the type its annotation names.
	EmptyTextError
		When ``text`` is empty.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> emails = ndp.Array.from_list(["ana@shop.fr", "bob@mail.com"])
	>>> emails.select(ndp.Contains(".fr"))
	Array(['ana@shop.fr'], dtype=TEXT)
	"""

	text: str
	case: Case = Case.SENSITIVE

	def __post_init__(self) -> None:
		"""
		Check that the searched text is not empty.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		EmptyTextError
			When ``text`` is empty.
		"""
		require_field_types(self)

		if self.text == "":
			raise EmptyTextError()
