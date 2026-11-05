"""
Unit tests of the griffe extension showing a public base class in the place of a hidden one.

.. versionadded:: 0.1.0
"""

import griffe
from public_bases import PublicBases, replace_hidden_bases

PACKAGE_NAME = "sales"
PACKAGE_FILES = {
	"__init__.py": "",
	"rule.py": "class Rule: ...\nclass Other: ...\n",
	"value_rule.py": "from sales.rule import Rule\nclass ValueRule[Value](Rule): ...\n",
	"greater.py": (
		"from sales.rule import Other\n"
		"from sales.value_rule import ValueRule\n"
		"class Greater(ValueRule[int]): ...\n"
		"class Mixed(Other, ValueRule[int]): ...\n"
		"class Plain(Other): ...\n"
	),
}
HIDDEN_BASES = {"sales.value_rule.ValueRule": "sales.rule.Rule"}
RULE_PATH = "sales.rule.Rule"
OTHER_PATH = "sales.rule.Other"


def load_package() -> tuple[griffe.Module, griffe.GriffeLoader]:
	"""
	Return a small package with a rule built on a hidden base class, and a loader that knows it.

	.. versionadded:: 0.1.0

	Returns
	-------
	tuple[griffe.Module, griffe.GriffeLoader]
		The package and its loader.
	"""
	loader = griffe.GriffeLoader()
	with griffe.temporary_visited_package(PACKAGE_NAME, PACKAGE_FILES) as package:
		loader.modules_collection.set_member(package.path, package)

	return package, loader


def test_replace_hidden_bases_shows_the_public_class() -> None:
	"""
	Check that ValueRule[int] becomes Rule.

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package()
	greater = package["greater.Greater"]

	replace_hidden_bases(greater, HIDDEN_BASES, loader)

	assert [base.canonical_path for base in greater.bases] == [RULE_PATH]


def test_replace_hidden_bases_keeps_the_other_bases_in_their_order() -> None:
	"""
	Check a class with a public base and a hidden one.

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package()
	mixed = package["greater.Mixed"]

	replace_hidden_bases(mixed, HIDDEN_BASES, loader)

	assert [base.canonical_path for base in mixed.bases] == [OTHER_PATH, RULE_PATH]


def test_public_bases_leaves_a_class_without_hidden_base() -> None:
	"""
	Check that the extension does not change a class with public bases only.

	.. versionadded:: 0.1.0
	"""
	package, loader = load_package()
	extension = PublicBases()

	extension.on_package(pkg=package, loader=loader)

	plain = package["greater.Plain"]
	assert [base.canonical_path for base in plain.bases] == [OTHER_PATH]
