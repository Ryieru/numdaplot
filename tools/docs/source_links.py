"""
MkDocs hook linking each object of the API pages to its source on GitHub.

The heading of each documented object gets a link to the lines of the file defining it, at the tag of the documented
version, so that the link shows the code the page describes. A method inherited from a group of methods links to
the file of that group.

.. versionadded:: 0.2.0
"""

import re
import tomllib
from dataclasses import dataclass
from functools import cache, partial
from importlib.util import find_spec
from pathlib import Path
from typing import Any

import griffe

PACKAGE_NAME = "numdaplot"
SOURCE_FOLDER = "src"
API_FOLDER = "api/"
PROJECT_FILE = Path("pyproject.toml")
PROJECT_KEY = "project"
VERSION_KEY = "version"
REPOSITORY_KEY = "repo_url"
VERSION_TAG = "v{version}"
SOURCE_URL = "{repository_url}/blob/{tag}/{file_path}#L{first_line}-L{last_line}"
THEME_PACKAGE = "material"
TEMPLATES_PATH = Path("templates")
ICON_PATH = TEMPLATES_PATH / ".icons" / "octicons" / "mark-github-16.svg"
SOURCE_LINK = (
	'<a class="source-link" href="{url}" title="Source of {name} on GitHub" target="_blank" rel="noopener">'
	"{icon}<span>Source</span></a>"
)
HEADING = re.compile(
	r'(?P<heading><h[1-6] id="numdaplot\.(?P<path>[^"]+)" class="doc doc-heading">.*?)'
	r'(?P<permalink><a href="#numdaplot\.(?P=path)" class="headerlink")',
	re.DOTALL,
)
PATH_SEPARATOR = "."


@dataclass(frozen=True)
class SourceLines:
	"""
	The lines of the file defining an object.

	.. versionadded:: 0.2.0

	Parameters
	----------
	file_path
		The path of the file from the root of the repository, such as ``src/numdaplot/arrays/array.py``.
	first_line
		The first line of the object.
	last_line
		The last line of the object, its docstring included for an attribute.
	"""

	file_path: str
	first_line: int
	last_line: int


@dataclass(frozen=True)
class SourceSite:
	"""
	Where the sources are shown, and the icon of the links.

	.. versionadded:: 0.2.0

	Parameters
	----------
	repository_url
		The address of the repository on GitHub.
	tag
		The tag of the documented version, such as ``v0.2.0``.
	icon
		The SVG of the GitHub icon.
	"""

	repository_url: str
	tag: str
	icon: str


def read_version_tag(project_file: Path) -> str:
	"""
	Return the tag of the version written in the project file.

	.. versionadded:: 0.2.0

	Parameters
	----------
	project_file
		The ``pyproject.toml`` file.

	Returns
	-------
	str
		The tag, ``v`` followed by the version, as the release workflow names it.

	Examples
	--------
	>>> from pathlib import Path
	>>> from source_links import read_version_tag
	>>> read_version_tag(Path("pyproject.toml")).startswith("v")
	True
	"""
	project_text = project_file.read_text()
	project_settings = tomllib.loads(project_text)
	project_table = project_settings[PROJECT_KEY]
	version = project_table[VERSION_KEY]
	version_tag = VERSION_TAG.format(version=version)

	return version_tag


def find_theme_file(relative_path: Path) -> Path:
	"""
	Return a file of the Material theme, such as one of its icons.

	.. versionadded:: 0.2.0

	Parameters
	----------
	relative_path
		The path of the file inside the theme package.

	Returns
	-------
	Path
		The path of the file where the theme is installed.

	Examples
	--------
	>>> from pathlib import Path
	>>> from source_links import ICON_PATH, find_theme_file
	>>> find_theme_file(ICON_PATH).name
	'mark-github-16.svg'
	"""
	theme_spec = find_spec(THEME_PACKAGE)
	if theme_spec is None or theme_spec.origin is None:
		raise ModuleNotFoundError(THEME_PACKAGE)

	theme_init = Path(theme_spec.origin)
	theme_folder = theme_init.parent
	theme_file = theme_folder / relative_path

	return theme_file


@cache
def load_source_site(repository_url: str) -> SourceSite:
	"""
	Return the repository, the version tag and the icon of the source links, read once.

	.. versionadded:: 0.2.0

	Parameters
	----------
	repository_url
		The address of the repository on GitHub, the ``repo_url`` of ``mkdocs.yml``.

	Returns
	-------
	SourceSite
		Where the links lead, and their icon.
	"""
	version_tag = read_version_tag(PROJECT_FILE)
	icon_file = find_theme_file(ICON_PATH)
	icon = icon_file.read_text()
	source_site = SourceSite(repository_url, version_tag, icon)

	return source_site


@cache
def load_package() -> griffe.Object:
	"""
	Return the numdaplot package as griffe reads it, loaded once.

	.. versionadded:: 0.2.0

	Returns
	-------
	griffe.Object
		The package, its members and the members its classes inherit.
	"""
	loader = griffe.GriffeLoader(search_paths=[SOURCE_FOLDER])
	package = loader.load(PACKAGE_NAME)
	if not isinstance(package, griffe.Object):
		raise TypeError(package.path)

	return package


def find_object(package: griffe.Object, object_path: str) -> griffe.Object | None:
	"""
	Return the object documented under a path of the package, inherited members included.

	.. versionadded:: 0.2.0

	Parameters
	----------
	package
		The numdaplot package.
	object_path
		The path inside the package, such as ``arrays.array.Array.convert``.

	Returns
	-------
	griffe.Object or None
		The object defining it, the method of a group of methods for an inherited one, or None for a path that is
		not an object.

	Examples
	--------
	>>> from source_links import find_object, load_package
	>>> find_object(load_package(), "arrays.array.Array.convert").parent.name
	'ArrayTypeChange'
	"""
	path_parts = object_path.split(PATH_SEPARATOR)
	found_object = package
	for path_part in path_parts:
		members = found_object.all_members if isinstance(found_object, griffe.Class) else found_object.members
		if path_part not in members:
			return None

		member = members[path_part]
		found_object = member.final_target if isinstance(member, griffe.Alias) else member

	return found_object


def find_source_lines(found_object: griffe.Object) -> SourceLines | None:
	"""
	Return the file and the lines defining an object.

	.. versionadded:: 0.2.0

	Parameters
	----------
	found_object
		An object of the package.

	Returns
	-------
	SourceLines or None
		Its lines, the docstring of an attribute included, or None when griffe knows no line.

	Examples
	--------
	>>> from source_links import find_object, find_source_lines, load_package
	>>> int8 = find_object(load_package(), "data_types.type.Type.INT8")
	>>> int8_lines = find_source_lines(int8)
	>>> int8_lines.file_path, int8_lines.last_line > int8_lines.first_line
	('src/numdaplot/data_types/type.py', True)
	"""
	first_line = found_object.lineno
	last_line = found_object.endlineno
	if first_line is None or last_line is None:
		return None

	docstring = found_object.docstring
	if docstring is not None and docstring.endlineno is not None:
		last_line = max(last_line, docstring.endlineno)

	relative_path = found_object.relative_filepath
	file_path = relative_path.as_posix()
	source_lines = SourceLines(file_path, first_line, last_line)

	return source_lines


def write_source_link(source_lines: SourceLines, object_name: str, source_site: SourceSite) -> str:
	"""
	Return the HTML link opening the lines of an object on GitHub.

	.. versionadded:: 0.2.0

	Parameters
	----------
	source_lines
		The file and the lines of the object.
	object_name
		The name of the object, shown in the title of the link.
	source_site
		The repository, the version tag and the icon.

	Returns
	-------
	str
		The link, with the GitHub icon and the word Source.

	Examples
	--------
	>>> from source_links import SourceLines, SourceSite, write_source_link
	>>> site = SourceSite("https://github.com/Ryieru/numdaplot", "v0.2.0", "<svg></svg>")
	>>> source_link = write_source_link(SourceLines("src/numdaplot/arrays/array.py", 23, 64), "Array", site)
	>>> "/blob/v0.2.0/src/numdaplot/arrays/array.py#L23-L64" in source_link
	True
	"""
	url = SOURCE_URL.format(
		repository_url=source_site.repository_url,
		tag=source_site.tag,
		file_path=source_lines.file_path,
		first_line=source_lines.first_line,
		last_line=source_lines.last_line,
	)
	source_link = SOURCE_LINK.format(url=url, name=object_name, icon=source_site.icon)

	return source_link


def link_heading(heading_match: re.Match[str], package: griffe.Object, source_site: SourceSite) -> str:
	"""
	Return a heading of an object with its source link placed before its permanent link.

	.. versionadded:: 0.2.0

	Parameters
	----------
	heading_match
		The match of the heading, up to its permanent link.
	package
		The numdaplot package.
	source_site
		The repository, the version tag and the icon.

	Returns
	-------
	str
		The heading with its source link, or unchanged when its path is not an object with lines.
	"""
	heading_text = heading_match.group(0)
	object_path = heading_match.group("path")
	found_object = find_object(package, object_path)
	if found_object is None:
		return heading_text

	source_lines = find_source_lines(found_object)
	if source_lines is None:
		return heading_text

	source_link = write_source_link(source_lines, found_object.name, source_site)
	heading = heading_match.group("heading")
	permalink = heading_match.group("permalink")
	linked_heading = heading + source_link + permalink

	return linked_heading


def add_source_links(html: str, package: griffe.Object, source_site: SourceSite) -> str:
	"""
	Return the HTML of a page with a source link in the heading of each documented object.

	.. versionadded:: 0.2.0

	Parameters
	----------
	html
		The HTML of an API page.
	package
		The numdaplot package.
	source_site
		The repository, the version tag and the icon.

	Returns
	-------
	str
		The HTML with its source links.
	"""
	heading_linker = partial(link_heading, package=package, source_site=source_site)
	linked_html = HEADING.sub(heading_linker, html)

	return linked_html


def on_page_content(html: str, page: Any, config: Any, **kwargs: Any) -> str:
	"""
	Link the objects of each API page to their source, called by MkDocs after rendering the page.

	.. versionadded:: 0.2.0

	Parameters
	----------
	html
		The HTML of the page.
	page
		The MkDocs page, whose source path tells whether it belongs to the API reference.
	config
		The MkDocs configuration, which gives the address of the repository.
	**kwargs
		The files MkDocs gives to its hooks, unused.

	Returns
	-------
	str
		The HTML with its source links, unchanged outside the API reference.
	"""
	source_path = page.file.src_uri
	is_api_page = source_path.startswith(API_FOLDER)
	if not is_api_page:
		return html

	repository_url = config[REPOSITORY_KEY]
	source_site = load_source_site(repository_url)
	package = load_package()
	linked_html = add_source_links(html, package, source_site)

	return linked_html
