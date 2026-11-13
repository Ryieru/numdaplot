"""The checks run before each git action: the fast ones before a commit, every one before a push, some in the CI."""

from changed_files import CheckScope, GitAction, GitCommandError, read_scope
from check_report import CheckResult, count_blocking_failures, write_annotation, write_result, write_summary
from configurations import check_configurations
from duplicate_checks import check_identical_blocks, check_identical_bodies
from public_name_checks import (
	CI_SITE_API_PATH,
	PUSH_SITE_API_PATH,
	check_changelog_entries,
	check_pages,
	check_version_notes,
	read_public_name_changes,
)
from structure_checks import check_file_sizes, check_functions
from style_checks import check_example_words, check_history_words, check_nested_calls
from tool_checks import list_fast_tool_runs, list_full_tool_runs, run_tool
from tool_logs import LOG_HEADER, build_log_name

STOP_EXIT_CODE = 1
GO_EXIT_CODE = 0
GIT_FAILURE = "[FAILED] the checks cannot run: {error}"
HEADER = "numdaplot checks before {action} ({file_count} changed Python files, compared with {base_ref})"


def run_tool_checks(scope: CheckScope, log_name: str) -> list[CheckResult]:
	"""
	Return the results of the tools: ruff and pyright before a commit, ruff and every CI configuration before a push.

	The CI runs none of them here: its other jobs already do.

	Parameters
	----------
	scope
		The git action and its changed files.
	log_name
		The name of the log files of this run of the checks.

	Returns
	-------
	list[CheckResult]
		One result per tool command.
	"""
	if scope.action == GitAction.CI:
		return []

	tool_runs = list_fast_tool_runs(scope.python_files)
	if scope.action == GitAction.PUSH:
		tool_runs = list_full_tool_runs()

	results = [run_tool(tool_run, log_name) for tool_run in tool_runs]
	if scope.action == GitAction.PUSH:
		configuration_results = check_configurations(log_name)
		results.extend(configuration_results)

	return results


def run_code_checks(scope: CheckScope) -> list[CheckResult]:
	"""
	Return the results of the checks of the written code: sizes, repeated code and the rules of writing.

	Parameters
	----------
	scope
		The changed files and the added lines.

	Returns
	-------
	list[CheckResult]
		The size, duplicate and style checks.
	"""
	results = [
		check_file_sizes(scope.python_files),
		check_functions(scope.python_files),
		check_identical_bodies(scope.python_files),
		check_identical_blocks(scope.python_files),
		check_nested_calls(scope.python_files, scope.added_lines),
		check_history_words(scope.added_lines),
		check_example_words(scope.added_lines),
	]

	return results


def run_public_name_checks(scope: CheckScope) -> list[CheckResult]:
	"""
	Return the results of the checks of the public names, with their pages before a push and in the CI.

	Parameters
	----------
	scope
		The git action.

	Returns
	-------
	list[CheckResult]
		The version notes, the changelog entries and, before a push or in the CI, the pages.
	"""
	changes = read_public_name_changes()
	results = [check_version_notes(changes), check_changelog_entries(changes)]
	if scope.action == GitAction.PUSH:
		push_page_result = check_pages(changes, PUSH_SITE_API_PATH)
		results.append(push_page_result)

	if scope.action == GitAction.CI:
		ci_page_result = check_pages(changes, CI_SITE_API_PATH)
		results.append(ci_page_result)

	return results


def run_checks(scope: CheckScope, log_name: str) -> list[CheckResult]:
	"""
	Return the results of every check a git action needs, the tools first so that the docs are built for the pages.

	Parameters
	----------
	scope
		The git action, its changed files and its added lines.
	log_name
		The name of the log files of this run of the checks.

	Returns
	-------
	list[CheckResult]
		Every result, in the order of the report.
	"""
	tool_results = run_tool_checks(scope, log_name)
	code_results = run_code_checks(scope)
	name_results = run_public_name_checks(scope)
	results = [*tool_results, *code_results, *name_results]

	return results


def run_action_checks(action: GitAction, given_base_ref: str) -> list[CheckResult]:
	"""
	Read what a git action brings, print the header of the report, and run every check of the action.

	Parameters
	----------
	action
		The git action about to happen.
	given_base_ref
		The commit a CI run is compared with, unused by the other actions.

	Returns
	-------
	list[CheckResult]
		Every result, in the order of the report.

	Raises
	------
	GitCommandError
		When a git command the checks need fails.
	"""
	scope = read_scope(action, given_base_ref)
	file_count = len(scope.python_files)
	header = HEADER.format(action=action.value, file_count=file_count, base_ref=scope.base_ref)
	print(header)
	log_name = build_log_name(action.value)
	if action != GitAction.CI:
		log_header = LOG_HEADER.format(log_name=log_name)
		print(log_header, flush=True)

	results = run_checks(scope, log_name)

	return results


def write_annotations(results: list[CheckResult]) -> list[str]:
	"""
	Return the GitHub workflow commands showing every problem of the checks on the lines of the commits.

	Parameters
	----------
	results
		Every result of the checks.

	Returns
	-------
	list[str]
		One command per problem.
	"""
	annotations = list[str]()

	for result in results:
		result_annotations = [write_annotation(result, problem) for problem in result.problems]
		annotations.extend(result_annotations)

	return annotations


def report_checks(action: GitAction, given_base_ref: str) -> int:
	"""
	Run the checks of a git action, print their report, and return whether git may go on.

	Parameters
	----------
	action
		The git action about to happen.
	given_base_ref
		The commit a CI run is compared with, unused by the other actions.

	Returns
	-------
	int
		1 when a blocking check failed or a git command failed, which stops the git action, else 0.
	"""
	try:
		results = run_action_checks(action, given_base_ref)
	except GitCommandError as error:
		failure_line = GIT_FAILURE.format(error=error)
		print(failure_line)
		return STOP_EXIT_CODE

	for result in results:
		result_lines = write_result(result)
		result_text = "\n".join(result_lines)
		print(result_text)

	if action == GitAction.CI:
		annotations = write_annotations(results)
		annotation_text = "\n".join(annotations)
		print(annotation_text)

	summary_lines = write_summary(results)
	summary_text = "\n".join(summary_lines)
	print(summary_text)
	failure_count = count_blocking_failures(results)
	exit_code = STOP_EXIT_CODE if failure_count > 0 else GO_EXIT_CODE

	return exit_code
