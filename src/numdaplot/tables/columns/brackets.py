"""
Brackets cutting a number column into categories.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.arrays.mapping.unmatched import Unmatched
from numdaplot.errors.duplicate_label_error import DuplicateLabelError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.errors.invalid_label_count_error import InvalidLabelCountError
from numdaplot.errors.invalid_limits_error import InvalidLimitsError
from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.rules.bounds import Bounds
from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.columns.bracket_end import BracketEnd

LIMIT_ITEM_NAME = "limit"
BRACKETS_NAME = "Brackets"
ACCEPTED_BOUNDS = frozenset({Bounds.LOW_ONLY, Bounds.HIGH_ONLY})
REFUSED_BOUNDS_NAME = "Bounds.{bounds_name}"
KEEP_SETTING_NAME = "Unmatched.KEEP"


@dataclass(frozen=True)
class Brackets:
	"""
	Brackets cutting a number column into categories, used as the ``format`` of a ``Conversion`` to ``CATEGORY``.

	The categories keep the order of the brackets, so that sorting and plots follow it. A missing value stays missing.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Refuses ``others=Unmatched.KEEP``.

	Parameters
	----------
	limits
		The limits between the brackets, at least one, in strictly increasing order. Two limits make one bracket.
	bounds
		Which limit of each bracket it holds: ``Bounds.LOW_ONLY`` by default, ``0 <= x < 10``, or
		``Bounds.HIGH_ONLY``, ``0 < x <= 10``. The other members are refused, as they would put a value in two
		brackets or in none.
	labels
		The name of each bracket, in order. When omitted, each name gives the values the bracket holds: ``0 to 9`` for
		integers, ``0 to under 10`` for decimals, ``80 or more`` or ``under 0`` for an open bracket. Whole limits are
		written without decimals.
	first
		Whether the first bracket stops at the first limit, ``BracketEnd.CLOSED`` by default, or holds every value
		below it with ``BracketEnd.OPEN``.
	last
		Whether the last bracket stops at the last limit, ``BracketEnd.CLOSED`` by default, or holds every value
		above it with ``BracketEnd.OPEN``.
	others
		What happens to a value in no bracket, ``Unmatched.ERROR`` by default, or ``Unmatched.MISSING``.
		``Unmatched.KEEP`` is refused, as a number cannot name a bracket.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	EmptyListError
		When ``limits`` is an empty list.
	RefusedSettingError
		When ``bounds`` is ``Bounds.INCLUDED`` or ``Bounds.EXCLUDED``, or ``others`` is ``Unmatched.KEEP``.
	InvalidLimitsError
		When the limits do not strictly increase, or a single limit has no open end.
	InvalidLabelCountError
		When ``labels`` does not give one name per bracket.
	DuplicateLabelError
		When a label appears twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ages = ndp.Array.from_list([4, 17, 30, 92])
	>>> victims = ndp.Table.from_arrays({"age": ages})
	>>> brackets = ndp.Brackets(limits=[0, 10, 20], last=ndp.BracketEnd.OPEN)
	>>> victims.convert(ndp.Conversion(column="age", dtype=ndp.Type.CATEGORY, format=brackets))
	          age
	     CATEGORY
	0      0 to 9
	1    10 to 19
	2  20 or more
	3  20 or more
	"""

	limits: list[int | float]
	bounds: Bounds = Bounds.LOW_ONLY
	labels: list[str] | None = None
	first: BracketEnd = BracketEnd.CLOSED
	last: BracketEnd = BracketEnd.CLOSED
	others: Unmatched = Unmatched.ERROR

	def __post_init__(self) -> None:
		"""
		Check the limits, the bounds and the labels.

		.. versionadded:: 0.1.0
		.. versionchanged:: 0.2.0
			Refuses ``others=Unmatched.KEEP``.

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		EmptyListError
			When ``limits`` is an empty list.
		RefusedSettingError
			When ``bounds`` is ``Bounds.INCLUDED`` or ``Bounds.EXCLUDED``, or ``others`` is ``Unmatched.KEEP``.
		InvalidLimitsError
			When the limits do not strictly increase, or a single limit has no open end.
		InvalidLabelCountError
			When ``labels`` does not give one name per bracket.
		DuplicateLabelError
			When a label appears twice.
		"""
		require_field_types(self)

		if self.limits == []:
			raise EmptyListError(LIMIT_ITEM_NAME)

		if self.bounds not in ACCEPTED_BOUNDS:
			bounds_name = REFUSED_BOUNDS_NAME.format(bounds_name=self.bounds.name)
			raise RefusedSettingError(bounds_name, BRACKETS_NAME)

		if self.others == Unmatched.KEEP:
			raise RefusedSettingError(KEEP_SETTING_NAME, BRACKETS_NAME)

		require_increasing_limits(self.limits)
		bracket_count = self.count_brackets()
		if bracket_count == 0:
			raise InvalidLimitsError(self.limits)

		if self.labels is not None:
			require_bracket_labels(self.labels, bracket_count)
			labels_copy = list(self.labels)
			object.__setattr__(self, "labels", labels_copy)

		limits_copy = list(self.limits)
		object.__setattr__(self, "limits", limits_copy)

	def count_brackets(self) -> int:
		"""
		Return the number of brackets: one between two limits, plus one per open end.

		.. versionadded:: 0.1.0

		Returns
		-------
		int
			The number of brackets.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Brackets(limits=[0, 18, 65], last=ndp.BracketEnd.OPEN).count_brackets()
		3
		"""
		limit_count = len(self.limits)
		bracket_count = limit_count - 1
		if self.first == BracketEnd.OPEN:
			bracket_count += 1

		if self.last == BracketEnd.OPEN:
			bracket_count += 1

		return bracket_count


def require_increasing_limits(limits: list[int | float]) -> None:
	"""
	Check that each limit is greater than the one before.

	.. versionadded:: 0.1.0

	Parameters
	----------
	limits
		The limits of brackets.

	Raises
	------
	InvalidLimitsError
		When a limit is not greater than the one before, or is NaN.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.brackets import require_increasing_limits
	>>> try:
	... 	require_increasing_limits([20, 10])
	... except ndp.InvalidLimitsError as error:
	... 	print(error)
	Expected limits in strictly increasing order, got 10 after 20.
	"""
	for earlier_limit, later_limit in zip(limits, limits[1:], strict=False):
		is_greater = later_limit > earlier_limit
		if not is_greater:
			raise InvalidLimitsError(limits)


def require_bracket_labels(labels: list[str], bracket_count: int) -> None:
	"""
	Check that the labels give one distinct name per bracket.

	.. versionadded:: 0.1.0

	Parameters
	----------
	labels
		The names of the brackets.
	bracket_count
		The number of brackets.

	Raises
	------
	InvalidLabelCountError
		When there is not one label per bracket.
	DuplicateLabelError
		At the first label given twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.brackets import require_bracket_labels
	>>> try:
	... 	require_bracket_labels(["child", "child"], 2)
	... except ndp.DuplicateLabelError as error:
	... 	print(error)
	The label 'child' appears more than once.
	"""
	label_count = len(labels)
	if label_count != bracket_count:
		raise InvalidLabelCountError(bracket_count, label_count)

	seen_labels = set[str]()
	for label in labels:
		if label in seen_labels:
			raise DuplicateLabelError(label)

		seen_labels.add(label)
