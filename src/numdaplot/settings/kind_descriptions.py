"""
Description of what a setting accepts, as written in the message of an InvalidTypeError.

.. versionadded:: 0.2.0
"""

from collections.abc import Sequence

from numdaplot.settings.annotation_kinds import NONE_NAME, AcceptedKinds

VOWELS = "aeiouAEIOU"
# These words start with a vowel letter but with a consonant sound, as in "a Uniform".
CONSONANT_SOUND_PREFIXES = ("Uni",)
ARTICLE_FORMAT = "{article} {name}"
NAMES_SEPARATOR = ", "
LAST_NAME_FORMAT = "{names} or {last_name}"
LIST_OF_FORMAT = "a list of {names}"
ANY_LIST = "a list"
LIST_SUCH_AS_FORMAT = "a list such as [{text!r}]"


def describe_kinds(kinds: AcceptedKinds, value: object) -> str:
	"""
	Return what a setting accepts, as written in the error message.

	A text given in place of a list is shown inside a list, the most likely thing to write.

	.. versionadded:: 0.1.0

	Parameters
	----------
	kinds
		What the setting accepts.
	value
		The rejected value.

	Returns
	-------
	str
		The description, such as ``an Index, a Range or None``.

	Examples
	--------
	>>> from numdaplot.settings.annotation_kinds import read_accepted_kinds
	>>> from numdaplot.settings.kind_descriptions import describe_kinds
	>>> describe_kinds(read_accepted_kinds(list[str]), "price")
	"a list such as ['price']"
	>>> describe_kinds(read_accepted_kinds(int | None), "2")
	'an int or None'
	"""
	if kinds.list_items is not None and isinstance(value, str):
		return LIST_SUCH_AS_FORMAT.format(text=value)

	descriptions = [add_article(name) for name in kinds.names]
	if kinds.list_items is not None:
		list_description = describe_list(kinds.list_items)
		descriptions.append(list_description)

	description = join_names(descriptions)

	return description


def describe_list(list_items: AcceptedKinds) -> str:
	"""
	Return what a list accepts, as written in the error message.

	.. versionadded:: 0.1.0

	Parameters
	----------
	list_items
		What the items of the list accept.

	Returns
	-------
	str
		``a list of str``, or ``a list`` when its items accept anything.

	Examples
	--------
	>>> from typing import Any
	>>> from numdaplot.settings.annotation_kinds import read_accepted_kinds
	>>> from numdaplot.settings.kind_descriptions import describe_list
	>>> describe_list(read_accepted_kinds(str)), describe_list(read_accepted_kinds(Any))
	('a list of str', 'a list')
	"""
	if object in list_items.classes:
		return ANY_LIST

	item_names = join_names(list_items.names)

	return LIST_OF_FORMAT.format(names=item_names)


def add_article(name: str) -> str:
	"""
	Return the name of a class with its article, None staying as it is.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		The name of a class.

	Returns
	-------
	str
		The name with ``a`` or ``an``.

	Examples
	--------
	>>> from numdaplot.settings.kind_descriptions import add_article
	>>> add_article("Index"), add_article("Range"), add_article("None")
	('an Index', 'a Range', 'None')
	"""
	if name == NONE_NAME:
		return name

	starts_with_vowel_sound = name[0] in VOWELS and not name.startswith(CONSONANT_SOUND_PREFIXES)
	article = "an" if starts_with_vowel_sound else "a"

	return ARTICLE_FORMAT.format(article=article, name=name)


def join_names(names: Sequence[str]) -> str:
	"""
	Return names separated by commas, the last one after ``or``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	names
		The names, at least one.

	Returns
	-------
	str
		The joined names.

	Examples
	--------
	>>> from numdaplot.settings.kind_descriptions import join_names
	>>> join_names(["an Index", "a Range", "None"])
	'an Index, a Range or None'
	"""
	first_names = names[:-1]
	last_name = names[-1]
	if not first_names:
		return last_name

	joined_names = NAMES_SEPARATOR.join(first_names)

	return LAST_NAME_FORMAT.format(names=joined_names, last_name=last_name)
