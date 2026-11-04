"""
Links of the names of a text written in code in the documentation.

.. versionadded:: 0.1.0
"""

import html
import re

import griffe
from link_targets import PATH_SEPARATOR, PUBLIC_PREFIX, LinkContext, find_identifier, find_object, object_exists

CODE_TOKEN = re.compile(
	r"""(?P<quoted>"[^"]*"|'[^']*')"""
	r"|(?P<name>[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)(?P<parentheses>\(\)|\()?"
	r"|(?P<bracket>[()])"
)
MARKDOWN_CHARACTERS = str.maketrans({"*": "&#42;", "_": "&#95;", "[": "&#91;", "]": "&#93;", "\\": "&#92;"})
OPENING_PARENTHESIS = "("
EMPTY_PARENTHESES = "()"
KEYWORD_SIGN = "="
EQUALITY_SIGN = "=="
LINK_TEMPLATE = (
	'<span class="api-link api-link-{kind}"><autoref identifier="{identifier}" optional>{text}</autoref></span>'
)


def link_code_tokens(code_text: str, context: LinkContext) -> str | None:
	"""
	Return a text written in code with a link on each of its names that matches an object.

	.. versionadded:: 0.1.0

	Parameters
	----------
	code_text
		The code, such as ``ndp.Uniform(low=0, high=10)``.
	context
		What the names can link to.

	Returns
	-------
	str or None
		The code as HTML holding its links, or ``None`` when no name matches an object.
	"""
	pieces = list[str]()
	callees = list[str | None]()
	position = 0
	has_link = False

	for token in CODE_TOKEN.finditer(code_text):
		plain_text = code_text[position : token.start()]
		escaped_text = escape_code(plain_text)
		pieces.append(escaped_text)
		position = token.end()

		token_identifier = None
		if token.group("name") is not None:
			token_identifier = find_token_identifier(token, callees, context)

		token_piece = build_token_piece(token, token_identifier, context.loader)
		pieces.append(token_piece)
		has_link = has_link or token_identifier is not None
		update_callees(token, token_identifier, callees)

	if not has_link:
		return None

	remaining_text = code_text[position:]
	escaped_text = escape_code(remaining_text)
	pieces.append(escaped_text)
	links = "".join(pieces)

	return links


def escape_code(text: str) -> str:
	"""
	Return a text shown in code as HTML that Markdown leaves as it is.

	.. versionadded:: 0.1.0

	Parameters
	----------
	text
		The text.

	Returns
	-------
	str
		The text with its HTML and Markdown characters written as entities.
	"""
	html_text = html.escape(text, quote=False)
	escaped_text = html_text.translate(MARKDOWN_CHARACTERS)

	return escaped_text


def find_token_identifier(token: re.Match[str], callees: list[str | None], context: LinkContext) -> str | None:
	"""
	Return the path of the object a name of a code refers to.

	.. versionadded:: 0.1.0

	Parameters
	----------
	token
		The match of the name.
	callees
		The path of each call around the name, the innermost last, ``None`` for an unknown call.
	context
		What the name can link to.

	Returns
	-------
	str or None
		The attribute for an argument given by keyword, otherwise the object found by ``find_identifier``, a
		member of the documented class read on its instance, such as ``array.to_list``, or an enum member.
	"""
	name = token.group("name")
	following_text = token.string[token.end() :]
	is_keyword = following_text.startswith(KEYWORD_SIGN) and not following_text.startswith(EQUALITY_SIGN)
	if is_keyword and callees:
		keyword_identifier = find_keyword_identifier(name, callees[-1], context.loader)
		return keyword_identifier

	identifier = find_identifier(name, context)
	if identifier is not None:
		return identifier

	instance_identifier = find_instance_member(name, context)
	if instance_identifier is not None:
		return instance_identifier

	enum_member_identifier = context.enum_member_paths.get(name)

	return enum_member_identifier


def find_keyword_identifier(name: str, callee: str | None, loader: griffe.GriffeLoader) -> str | None:
	"""
	Return the path of the attribute an argument given by keyword sets.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		The name of the argument.
	callee
		The path of the call receiving it, ``None`` for an unknown call.
	loader
		The loader that holds every loaded module.

	Returns
	-------
	str or None
		The path of the attribute, ``None`` when the call has none of this name.
	"""
	if callee is None:
		return None

	attribute_path = callee + PATH_SEPARATOR + name
	exists = object_exists(attribute_path, loader)
	if not exists:
		return None

	return attribute_path


def find_instance_member(name: str, context: LinkContext) -> str | None:
	"""
	Return the path of a member of the documented class read on an instance named after it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	name
		A name written in code, such as ``array.to_list`` in the documentation of ``Array``.
	context
		What the name can link to.

	Returns
	-------
	str or None
		The path of the member, ``None`` when the name is not written this way.
	"""
	if context.class_path is None:
		return None

	class_name = context.class_path.rpartition(PATH_SEPARATOR)[-1]
	head, separator, member_name = name.partition(PATH_SEPARATOR)
	lowered_class_name = class_name.lower()
	if separator == "" or head != lowered_class_name:
		return None

	member_path = context.class_path + PATH_SEPARATOR + member_name
	exists = object_exists(member_path, context.loader)
	if not exists:
		return None

	return member_path


def build_token_piece(token: re.Match[str], identifier: str | None, loader: griffe.GriffeLoader) -> str:
	"""
	Return the HTML of a token of a code: its links for a name that matches an object, else its escaped text.

	Empty parentheses stay part of the link of their name, such as ``ndp.Mean()``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	token
		The match of the token.
	identifier
		The path of the object the token refers to, ``None`` when there is none.
	loader
		The loader that holds every loaded module.

	Returns
	-------
	str
		The HTML of the token.
	"""
	if identifier is None:
		escaped_token = escape_code(token.group(0))
		return escaped_token

	name = token.group("name")
	parentheses = token.group("parentheses")
	if parentheses == EMPTY_PARENTHESES:
		links = build_links(name + parentheses, identifier, loader)
		return links

	links = build_links(name, identifier, loader)
	piece = links + (parentheses or "")

	return piece


def update_callees(token: re.Match[str], identifier: str | None, callees: list[str | None]) -> None:
	"""
	Update the calls around the next token after reading a token that opens or closes parentheses.

	.. versionadded:: 0.1.0

	Parameters
	----------
	token
		The match of the token.
	identifier
		The path of the object the token refers to, ``None`` when there is none.
	callees
		The path of each open call, the innermost last, updated in place.
	"""
	if token.group("parentheses") == OPENING_PARENTHESIS:
		callees.append(identifier)
		return

	bracket = token.group("bracket")
	if bracket == OPENING_PARENTHESIS:
		callees.append(None)
		return

	if bracket is not None and callees:
		callees.pop()


def build_links(code_text: str, identifier: str, loader: griffe.GriffeLoader) -> str:
	"""
	Return the links of a name: one for the whole name, or one for its owner and one for its member.

	.. versionadded:: 0.1.0

	Parameters
	----------
	code_text
		The name as written, such as ``Conflict.ERROR``, ``ndp.Greater`` or ``from_csv()``. The ``ndp.`` prefix
		stays part of the first link.
	identifier
		The path of the object the whole name refers to.
	loader
		The loader that holds every loaded module.

	Returns
	-------
	str
		The links, joined by a dot when the name holds one.
	"""
	prefix = PUBLIC_PREFIX if code_text.startswith(PUBLIC_PREFIX) else ""
	short_text = code_text.removeprefix(PUBLIC_PREFIX)
	owner_text, separator, member_text = short_text.rpartition(PATH_SEPARATOR)
	if separator == "":
		whole_link = build_link(code_text, identifier, loader)
		return whole_link

	owner_identifier, _, _ = identifier.rpartition(PATH_SEPARATOR)
	owner_link = build_link(prefix + owner_text, owner_identifier, loader)
	member_link = build_link(member_text, identifier, loader)
	links = owner_link + PATH_SEPARATOR + member_link

	return links


def build_link(text: str, identifier: str, loader: griffe.GriffeLoader) -> str:
	"""
	Return an optional link to an object, in a span whose class names the kind of the object.

	.. versionadded:: 0.1.0

	Parameters
	----------
	text
		The text of the link.
	identifier
		The path of the object.
	loader
		The loader that holds every loaded module.

	Returns
	-------
	str
		The link, such as ``api-link-class`` for a class, ``api-link-object`` for an unknown object.
	"""
	target = find_object(identifier, loader)
	kind = "object" if target is None else target.kind.value
	link = LINK_TEMPLATE.format(kind=kind, identifier=identifier, text=text)

	return link
