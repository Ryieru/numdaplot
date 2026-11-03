"""
Griffe extension showing the version directives of the docstrings as boxes of the documentation site.

Docstrings use the Sphinx directives ``.. versionadded::``, ``.. versionchanged::`` and ``.. deprecated::``,
which editors show as they are. The Markdown of the documentation site does not know them, so this
extension turns each one into an admonition when ``mkdocs`` reads the docstrings. The added and changed
versions use their own admonition types, styled as a discreet line by ``docs/stylesheets/symbols.css``.

.. versionadded:: 0.1.0
"""

import re
from typing import Any

import griffe

VERSION_DIRECTIVE = re.compile(
	r"^(?P<indent>[ \t]*)\.\. (?P<directive>versionadded|versionchanged|deprecated):: (?P<version>\S+)[ \t]*$",
	re.MULTILINE,
)
ADMONITIONS = {
	"versionadded": '!!! version-added "Added in version {version}"',
	"versionchanged": '!!! version-changed "Changed in version {version}"',
	"deprecated": '!!! warning "Deprecated since version {version}"',
}


def convert_version_directives(docstring_text: str) -> str:
	r"""
	Return a docstring whose version directives are written as Markdown admonitions.

	.. versionadded:: 0.1.0

	Parameters
	----------
	docstring_text
		The text of a docstring.

	Returns
	-------
	str
		The same text, each directive line replaced with an admonition line at the same indentation.

	Examples
	--------
	>>> from version_directives import convert_version_directives
	>>> convert_version_directives("Mean of the values.\n\n.. versionadded:: 0.1.0")
	'Mean of the values.\n\n!!! version-added "Added in version 0.1.0"'
	"""
	converted_text = VERSION_DIRECTIVE.sub(write_admonition, docstring_text)

	return converted_text


def write_admonition(directive_match: re.Match[str]) -> str:
	"""
	Return the admonition line replacing one version directive.

	.. versionadded:: 0.1.0

	Parameters
	----------
	directive_match
		The match of a directive line, with its indentation, its directive name and its version.

	Returns
	-------
	str
		The admonition line, at the indentation of the directive.

	Examples
	--------
	>>> from version_directives import VERSION_DIRECTIVE, write_admonition
	>>> directive_match = VERSION_DIRECTIVE.search(".. deprecated:: 0.2.0")
	>>> write_admonition(directive_match)
	'!!! warning "Deprecated since version 0.2.0"'
	"""
	indent = directive_match.group("indent")
	directive = directive_match.group("directive")
	version = directive_match.group("version")
	admonition_template = ADMONITIONS[directive]
	admonition = admonition_template.format(version=version)
	admonition_line = indent + admonition

	return admonition_line


class VersionDirectives(griffe.Extension):
	"""
	Griffe extension turning the version directives of every docstring into admonitions.

	``mkdocs.yml`` loads it in the ``extensions`` option of the mkdocstrings Python handler.

	.. versionadded:: 0.1.0
	"""

	def on_object(self, *, obj: griffe.Object, **kwargs: Any) -> None:
		"""
		Convert the version directives of the docstring of an object, if it has one.

		.. versionadded:: 0.1.0

		Parameters
		----------
		obj
			A module, class, function or attribute read by griffe.
		**kwargs
			The other arguments griffe gives to its extensions, unused.
		"""
		if obj.docstring is None:
			return

		converted_text = convert_version_directives(obj.docstring.value)
		obj.docstring.value = converted_text
