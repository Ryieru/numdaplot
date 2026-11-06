"""
Exact reading of decimals written as texts, which pandas only gives by default from version 3.1.

.. versionadded:: 0.1.0
"""

import re
from typing import Any, cast

import numpy
import pandas
from numpy.typing import NDArray

VERSION_PATTERN = r"(\d+)\.(\d+)"
FIRST_EXACT_VERSION = (3, 1)
FLOAT_PRECISION_SETTING = "float_precision"
ROUND_TRIP_PRECISION = "round_trip"
DECIMAL_KIND = "f"


def reads_exact_decimals(pandas_version: str) -> bool:
	"""
	Return whether a version of pandas reads the exact value of a decimal written as a text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	pandas_version
		The version, such as ``"3.1.0"``.

	Returns
	-------
	bool
		True from version 3.1.

	Examples
	--------
	>>> from numdaplot.tables.frames.pandas_decimals import reads_exact_decimals
	>>> reads_exact_decimals("2.3.0"), reads_exact_decimals("3.1.0rc0")
	(False, True)
	"""
	version_match = cast(re.Match[str], re.match(VERSION_PATTERN, pandas_version))
	major_text, minor_text = version_match.groups()
	major = int(major_text)
	minor = int(minor_text)
	is_exact = (major, minor) >= FIRST_EXACT_VERSION

	return is_exact


READS_EXACT_DECIMALS = reads_exact_decimals(pandas.__version__)


def find_exact_csv_settings() -> dict[str, str]:
	"""
	Return the settings ``pandas.read_csv`` needs to read the exact value of each decimal.

	.. versionadded:: 0.1.0

	Returns
	-------
	dict[str, str]
		The precision of the slower exact reading before pandas 3.1, nothing from then on as the setting is
		deprecated there.

	Examples
	--------
	>>> from numdaplot.tables.frames.pandas_decimals import find_exact_csv_settings
	>>> settings = find_exact_csv_settings()
	>>> settings in ({}, {"float_precision": "round_trip"})
	True
	"""
	if READS_EXACT_DECIMALS:
		return {}

	return {FLOAT_PRECISION_SETTING: ROUND_TRIP_PRECISION}


def restore_exact_decimals(texts: NDArray[Any], numbers: NDArray[Any]) -> NDArray[Any]:
	"""
	Return numbers read by ``pandas.to_numeric``, with the exact value of their texts before pandas 3.1.

	.. versionadded:: 0.1.0

	Parameters
	----------
	texts
		The texts holding the numbers, each one read by pandas without failure.
	numbers
		The numbers pandas read.

	Returns
	-------
	NDArray
		The exact decimals, or the numbers themselves when pandas read them exactly or read integers.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.frames.pandas_decimals import restore_exact_decimals
	>>> texts = numpy.array(["0.5"], dtype=object)
	>>> restore_exact_decimals(texts, numpy.array([0.5]))
	array([0.5])
	"""
	if READS_EXACT_DECIMALS or numbers.dtype.kind != DECIMAL_KIND:
		return numbers

	text_list = cast(list[str], texts.tolist())
	exact_list = [float(text) for text in text_list]
	exact_numbers = numpy.array(exact_list, dtype=numbers.dtype)

	return exact_numbers
