"""
MkDocs hook turning the names written in code in the pages, such as the changelog, into links.

The docstrings get their links from the ``cross_references`` griffe extension. The other pages, written
in Markdown, name the same objects in code, such as `Array` or `Table.filter`: this hook links each name
that matches a public object, or a member that only one public class has, with the colors of its kind.

.. versionadded:: 0.1.0
"""

import re
from dataclasses import dataclass
from functools import cache
from typing import Any

import griffe
from code_links import build_links
from link_targets import (
	LinkContext,
	find_enum_member_paths,
	find_identifier,
	find_public_paths,
	find_unique_member_paths,
)
from value_types import find_value_type_paths

PACKAGE_NAME = "numdaplot"
SOURCE_FOLDER = "src"
API_FOLDER = "api/"
INLINE_CODE = re.compile(r"<code>(?P<name>[A-Za-z_][\w.]*)(?P<call>\(\))?</code>")
CODE_TEMPLATE = "<code>{content}</code>"


@dataclass(frozen=True)
class ReferenceIndex:
	"""
	What the names of the pages can link to.

	.. versionadded:: 0.1.0

	Parameters
	----------
	context
		The public names and the loader, without class.
	member_paths
		The path of each member name that only one public class has.
	"""

	context: LinkContext
	member_paths: dict[str, str]


@cache
def load_reference_index() -> ReferenceIndex:
	"""
	Return the public names of numdaplot and the members only one public class has, loaded once.

	.. versionadded:: 0.1.0

	Returns
	-------
	ReferenceIndex
		What the names can link to.
	"""
	loader = griffe.GriffeLoader(search_paths=[SOURCE_FOLDER])
	package = loader.load(PACKAGE_NAME)
	loader.resolve_aliases()
	if not isinstance(package, griffe.Module):
		raise TypeError(package.path)

	value_type_paths = find_value_type_paths(loader)
	public_paths = find_public_paths(package) | value_type_paths
	member_paths = find_unique_member_paths(public_paths, loader)
	enum_member_paths = find_enum_member_paths(member_paths)
	context = LinkContext(None, public_paths, loader, enum_member_paths)
	index = ReferenceIndex(context, member_paths)

	return index


def link_inline_code(html: str, index: ReferenceIndex) -> str:
	"""
	Return HTML whose inline code naming a numdaplot object links to its documentation.

	.. versionadded:: 0.1.0

	Parameters
	----------
	html
		The HTML of a page.
	index
		What the names can link to.

	Returns
	-------
	str
		The same HTML, each matching name holding colored links. Blocks of code are left unchanged.
	"""

	def replace_code(code_match: re.Match[str]) -> str:
		"""
		Return the links replacing one inline code, or the code itself when it names nothing.

		.. versionadded:: 0.1.0

		Parameters
		----------
		code_match
			The match of an inline code.

		Returns
		-------
		str
			The code holding links, or the original code.
		"""
		name = code_match.group("name")
		identifier = find_identifier(name, index.context)
		if identifier is None:
			identifier = index.member_paths.get(name)

		if identifier is None:
			return code_match.group(0)

		call = code_match.group("call")
		code_text = name if call is None else name + call
		links = build_links(code_text, identifier, index.context.loader)
		code = CODE_TEMPLATE.format(content=links)

		return code

	linked_html = INLINE_CODE.sub(replace_code, html)

	return linked_html


def on_page_content(html: str, page: Any, **kwargs: Any) -> str:
	"""
	Link the inline code of each page outside the API reference, called by MkDocs after rendering it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	html
		The HTML of the page.
	page
		The MkDocs page, whose source path tells whether it belongs to the API reference.
	**kwargs
		The configuration and the files MkDocs gives to its hooks, unused.

	Returns
	-------
	str
		The HTML with its links. The API pages already get theirs from their docstrings.
	"""
	source_path = page.file.src_uri
	if source_path.startswith(API_FOLDER):
		return html

	index = load_reference_index()
	linked_html = link_inline_code(html, index)

	return linked_html
