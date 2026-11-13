"""Public names added or removed since the last release: their version notes, their changelog entries, their pages."""

import importlib
import inspect
import re
from dataclasses import dataclass
from pathlib import Path

from changed_files import run_git
from check_report import CheckResult, Severity
from configurations import SITE_CONFIGURATION

PACKAGE_NAME = "numdaplot"
PACKAGE_INIT = "src/numdaplot/__init__.py"
PACKAGE_INIT_PATH = Path(PACKAGE_INIT)
CHANGELOG_PATH = Path("CHANGELOG.md")
PUSH_SITE_API_PATH = SITE_CONFIGURATION.folder / "site" / "api"
CI_SITE_API_PATH = Path("site", "api")
RELEASE_TAG_PATTERN = "v*"
CANDIDATE_TAG_PATTERN = "*rc*"
TAG_PREFIX = "v"
RELEASE_TITLE = "## [{version}]"
PUBLIC_NAME_ENTRY = re.compile(r'^\t"(\w+)",$', re.MULTILINE)
VERSION_ADDED = re.compile(r"\.\. versionadded:: ([\d.]+)")
RENAMED_FROM = re.compile(r"Renamed from ``(\w+)``")
CODE_SPAN = re.compile(r"`([^`]+)`")
CAMEL_BOUNDARY = re.compile(r"(?<!^)(?=[A-Z])")
WORD_SEPARATOR = "_"
VERSION_CHECK_NAME = "version note of each public name added since the last release"
CHANGELOG_CHECK_NAME = "changelog entry of each public name added or removed since the last release"
PAGE_CHECK_NAME = "documentation page of each public name added since the last release"
NO_VERSION_PROBLEM = "{name}: no versionadded in its docstring"
OLD_VERSION_PROBLEM = "{name}: versionadded {added}, not newer than the release {released}"
ADDED_ENTRY_PROBLEM = "{name}: added, but not named in the changelog above [{released}]"
REMOVED_ENTRY_PROBLEM = "{name}: removed, but not named in the changelog above [{released}]"
NO_PAGE_PROBLEM = "{name}: no page {page_name}/index.html under {site_path}"


@dataclass(frozen=True)
class PublicNameChanges:
	"""
	The public names of ``ndp`` added and removed since the last release.

	Parameters
	----------
	released_version
		The version of the latest final release, read in its tag.
	added_names
		The names exported now and not in the release.
	removed_names
		The names of the release no longer exported.
	"""

	released_version: str
	added_names: list[str]
	removed_names: list[str]


def find_release_tag() -> str:
	"""
	Return the tag of the latest final release before the current commit, release candidates left out.

	The version of pyproject.toml is not used: it already names the next version while a release is prepared.

	Returns
	-------
	str
		A tag such as ``v0.1.2``.

	Raises
	------
	GitCommandError
		When no release tag exists before the current commit.
	"""
	tag_arguments = [
		"describe",
		"--tags",
		"--abbrev=0",
		"--match",
		RELEASE_TAG_PATTERN,
		"--exclude",
		CANDIDATE_TAG_PATTERN,
	]
	described_tag = run_git(tag_arguments)
	release_tag = described_tag.strip()

	return release_tag


def read_public_name_changes() -> PublicNameChanges:
	"""
	Return the public names added and removed since the latest final release.

	Returns
	-------
	PublicNameChanges
		The released version and the names, sorted.

	Raises
	------
	GitCommandError
		When the release tag or its package file cannot be read.
	"""
	release_tag = find_release_tag()
	released_version = release_tag.removeprefix(TAG_PREFIX)
	released_init = run_git(["show", f"{release_tag}:{PACKAGE_INIT}"])
	current_init = PACKAGE_INIT_PATH.read_text()
	released_entries = PUBLIC_NAME_ENTRY.findall(released_init)
	released_names = set(released_entries)
	current_entries = PUBLIC_NAME_ENTRY.findall(current_init)
	current_names = set(current_entries)
	added_names = sorted(current_names - released_names)
	removed_names = sorted(released_names - current_names)
	changes = PublicNameChanges(released_version, added_names, removed_names)

	return changes


def parse_version(version: str) -> tuple[int, ...]:
	"""
	Return the numbers of a version, to compare versions.

	Parameters
	----------
	version
		A version such as ``"0.2.0"``.

	Returns
	-------
	tuple[int, ...]
		Its numbers.

	Examples
	--------
	>>> parse_version("0.10.1") > parse_version("0.2.0")
	True
	"""
	parts = version.split(".")
	numbers = tuple(int(part) for part in parts)

	return numbers


def check_version_notes(changes: PublicNameChanges) -> CheckResult:
	"""
	Return the added names whose docstring has no ``versionadded``, or one not newer than the last release.

	A name renamed from a removed name keeps the version of the old name, and tells the rename in its docstring.

	Parameters
	----------
	changes
		The added names and the released version.

	Returns
	-------
	CheckResult
		One problem per name with a missing or old version note.
	"""
	package = importlib.import_module(PACKAGE_NAME)
	released_numbers = parse_version(changes.released_version)
	problems = list[str]()

	for name in changes.added_names:
		public_object = getattr(package, name)
		docstring = inspect.getdoc(public_object) or ""
		match = VERSION_ADDED.search(docstring)
		if match is None:
			version_problem = NO_VERSION_PROBLEM.format(name=name)
			problems.append(version_problem)
			continue

		added_version = match.group(1)
		added_numbers = parse_version(added_version)
		renamed_entries = RENAMED_FROM.findall(docstring)
		renamed_names = set(renamed_entries)
		removed_names = set(changes.removed_names)
		is_rename = bool(renamed_names & removed_names)
		if added_numbers <= released_numbers and not is_rename:
			old_problem = OLD_VERSION_PROBLEM.format(name=name, added=added_version, released=changes.released_version)
			problems.append(old_problem)

	result = CheckResult(VERSION_CHECK_NAME, Severity.BLOCKING, problems)

	return result


def read_changelog_since(released_version: str) -> str:
	"""
	Return the part of the changelog above the section of a release: ``[Unreleased]``, or the section being released.

	Parameters
	----------
	released_version
		The version of the latest final release, such as ``0.1.2``.

	Returns
	-------
	str
		The text before the title of that release, or the whole changelog when the title is missing.
	"""
	changelog_text = CHANGELOG_PATH.read_text()
	release_title = RELEASE_TITLE.format(version=released_version)
	end = changelog_text.find(release_title)
	if end == -1:
		return changelog_text

	changelog_part = changelog_text[:end]

	return changelog_part


def is_named(name: str, text: str) -> bool:
	"""
	Return whether a text names a public name in code style, as a whole word between backticks.

	Parameters
	----------
	name
		The public name.
	text
		The text of the changelog.

	Returns
	-------
	bool
		True when a code span holds the name, such as ``Share`` or ``BarChart(value_labels=ValueLabels())``.

	Examples
	--------
	>>> is_named("Share", "- `Share` gives the fraction"), is_named("Share", "- `Shared` values")
	(True, False)
	>>> is_named("ValueLabels", "- `BarChart(value_labels=ValueLabels(decimals=2))` writes")
	True
	"""
	word = re.compile(rf"\b{re.escape(name)}\b")
	code_spans = CODE_SPAN.findall(text)
	matching_spans = [code_span for code_span in code_spans if word.search(code_span) is not None]
	is_found = bool(matching_spans)

	return is_found


def check_changelog_entries(changes: PublicNameChanges) -> CheckResult:
	"""
	Return the added or removed names that the changelog does not name above the section of the latest release.

	Parameters
	----------
	changes
		The added and removed names.

	Returns
	-------
	CheckResult
		One problem per name missing from the changelog.
	"""
	changelog_part = read_changelog_since(changes.released_version)
	problems = list[str]()

	for name in changes.added_names:
		is_added_entry = is_named(name, changelog_part)
		if not is_added_entry:
			added_problem = ADDED_ENTRY_PROBLEM.format(name=name, released=changes.released_version)
			problems.append(added_problem)

	for name in changes.removed_names:
		is_removed_entry = is_named(name, changelog_part)
		if not is_removed_entry:
			removed_problem = REMOVED_ENTRY_PROBLEM.format(name=name, released=changes.released_version)
			problems.append(removed_problem)

	result = CheckResult(CHANGELOG_CHECK_NAME, Severity.BLOCKING, problems)

	return result


def check_pages(changes: PublicNameChanges, site_api_path: Path) -> CheckResult:
	"""
	Return the added names without a page in a site built by mkdocs.

	The page of a name is named after its file, which holds one notion named like it.

	Parameters
	----------
	changes
		The added names.
	site_api_path
		The API folder of the built site: ``PUSH_SITE_API_PATH`` before a push, ``CI_SITE_API_PATH`` in the CI.

	Returns
	-------
	CheckResult
		One problem per name without page.
	"""
	built_pages = {page.parent.name for page in site_api_path.rglob("index.html")}
	problems = list[str]()

	for name in changes.added_names:
		snake_name = CAMEL_BOUNDARY.sub(WORD_SEPARATOR, name)
		page_name = snake_name.lower()
		if page_name not in built_pages:
			page_problem = NO_PAGE_PROBLEM.format(name=name, page_name=page_name, site_path=site_api_path)
			problems.append(page_problem)

	result = CheckResult(PAGE_CHECK_NAME, Severity.BLOCKING, problems)

	return result
