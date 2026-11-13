"""
Unit tests of the exact reading of decimals written as texts.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

from numdaplot.column_storage import pandas_decimals
from numdaplot.column_storage.pandas_decimals import (
	find_exact_csv_settings,
	reads_exact_decimals,
	restore_exact_decimals,
)

NOISY_SUM = 0.1 + 0.2
NOISY_TEXT = "0.30000000000000004"
READ_NUMBER = 0.3
ROUND_TRIP_SETTINGS = {"float_precision": "round_trip"}
EXACT_FLAG = "READS_EXACT_DECIMALS"
OBJECT_DTYPE = numpy.dtype(object)
SINGLE_DTYPE = "float32"


@pytest.mark.parametrize("version", ["2.3.0", "2.3.3", "3.0.0", "3.0.3"])
def test_reads_exact_decimals_is_false_before_3_1(version: str) -> None:
	"""
	Check the versions measured as inexact.

	.. versionadded:: 0.1.0
	"""
	is_exact = reads_exact_decimals(version)

	assert is_exact is False


@pytest.mark.parametrize("version", ["3.1.0", "3.1.0rc0", "3.10.0", "4.0.0"])
def test_reads_exact_decimals_is_true_from_3_1(version: str) -> None:
	"""
	Check later versions, a minor number of two digits and a release candidate.

	.. versionadded:: 0.1.0
	"""
	is_exact = reads_exact_decimals(version)

	assert is_exact is True


def test_find_exact_csv_settings_asks_for_the_exact_reading_before_3_1(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check an older pandas.

	.. versionadded:: 0.1.0
	"""
	monkeypatch.setattr(pandas_decimals, EXACT_FLAG, False)

	settings = find_exact_csv_settings()

	assert settings == ROUND_TRIP_SETTINGS


def test_find_exact_csv_settings_gives_nothing_from_3_1(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check a pandas where the setting is deprecated.

	.. versionadded:: 0.1.0
	"""
	monkeypatch.setattr(pandas_decimals, EXACT_FLAG, True)

	settings = find_exact_csv_settings()

	assert settings == {}


def test_restore_exact_decimals_reads_the_texts_before_3_1(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check a decimal pandas read inexactly.

	.. versionadded:: 0.1.0
	"""
	monkeypatch.setattr(pandas_decimals, EXACT_FLAG, False)
	texts = numpy.array([NOISY_TEXT], dtype=OBJECT_DTYPE)
	numbers = numpy.array([READ_NUMBER])

	exact_numbers = restore_exact_decimals(texts, numbers)

	exact_list = exact_numbers.tolist()
	assert exact_list == [NOISY_SUM]


def test_restore_exact_decimals_keeps_the_type_of_the_numbers(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check the type of the result.

	.. versionadded:: 0.1.0
	"""
	monkeypatch.setattr(pandas_decimals, EXACT_FLAG, False)
	texts = numpy.array([NOISY_TEXT], dtype=OBJECT_DTYPE)
	numbers = numpy.array([READ_NUMBER], dtype=SINGLE_DTYPE)

	exact_numbers = restore_exact_decimals(texts, numbers)

	assert exact_numbers.dtype == numbers.dtype


def test_restore_exact_decimals_leaves_the_numbers_from_3_1(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the texts are not read twice.

	.. versionadded:: 0.1.0
	"""
	monkeypatch.setattr(pandas_decimals, EXACT_FLAG, True)
	texts = numpy.array([NOISY_TEXT], dtype=OBJECT_DTYPE)
	numbers = numpy.array([READ_NUMBER])

	exact_numbers = restore_exact_decimals(texts, numbers)

	assert exact_numbers is numbers


def test_restore_exact_decimals_leaves_integers(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check numbers read as integers, which are already exact.

	.. versionadded:: 0.1.0
	"""
	monkeypatch.setattr(pandas_decimals, EXACT_FLAG, False)
	texts = numpy.array(["2"], dtype=OBJECT_DTYPE)
	numbers = numpy.array([2])

	exact_numbers = restore_exact_decimals(texts, numbers)

	assert exact_numbers is numbers
