"""
Functional tests of the numdaplot errors, as a user catches them.

.. versionadded:: 0.1.0
"""

import warnings

import pytest

import numdaplot as ndp

PRECISE_ERRORS = [
	ndp.CellOutOfRangeError,
	ndp.ColumnNotFoundError,
	ndp.ConflictingSettingsError,
	ndp.DimensionError,
	ndp.DuplicateColumnError,
	ndp.DuplicateLabelError,
	ndp.DuplicateValueError,
	ndp.EmptyArrayError,
	ndp.EmptyListError,
	ndp.EmptyTextError,
	ndp.EmptyTotalError,
	ndp.EmptyValuesError,
	ndp.FileAccessError,
	ndp.FileExistsError,
	ndp.FileNotFoundError,
	ndp.IncompatibleChartsError,
	ndp.IncompatibleTypesError,
	ndp.InvalidBaseError,
	ndp.InvalidBinWidthError,
	ndp.InvalidBoundsError,
	ndp.InvalidChartDataError,
	ndp.InvalidColorCountError,
	ndp.InvalidColorError,
	ndp.InvalidColumnNameError,
	ndp.InvalidConversionError,
	ndp.InvalidCountError,
	ndp.InvalidDateFormatError,
	ndp.InvalidDeviationError,
	ndp.InvalidFractionError,
	ndp.InvalidLabelCountError,
	ndp.InvalidLimitsError,
	ndp.InvalidOpacityError,
	ndp.InvalidPointSizeError,
	ndp.InvalidPositionError,
	ndp.InvalidResolutionError,
	ndp.InvalidSeedError,
	ndp.InvalidSeparatorError,
	ndp.InvalidShapeError,
	ndp.InvalidRotationError,
	ndp.InvalidSizeError,
	ndp.InvalidStepError,
	ndp.InvalidSuffixesError,
	ndp.InvalidTimeZoneChangeError,
	ndp.IntegerOverflowError,
	ndp.IrregularListError,
	ndp.MissingDependencyError,
	ndp.MissingTypeError,
	ndp.MissingValueError,
	ndp.NotSingleValueError,
	ndp.OccupiedCellError,
	ndp.OutOfDomainError,
	ndp.RefusedOperationError,
	ndp.RefusedSettingError,
	ndp.ShapeMismatchError,
	ndp.TimeOverflowError,
	ndp.TimeZoneMismatchError,
	ndp.UnmatchedValueError,
	ndp.UnknownTimeZoneError,
	ndp.UnsupportedImageFormatError,
	ndp.UnsupportedIndexError,
	ndp.UnsupportedMissingError,
	ndp.UnsupportedTypeError,
	ndp.ValueConversionError,
]
PRECISE_WARNINGS = [
	ndp.BroadcastWarning,
	ndp.CalculationWarning,
	ndp.ReadabilityWarning,
]
REJECTED_FRACTION = 2.0
ZERO_DISTANCES = [0.0, 3.0]
ZERO_HOURS = [0.0, 2.0]


@pytest.mark.parametrize("error_class", PRECISE_ERRORS)
def test_every_precise_error_is_caught_by_numdaplot_error(error_class: type[Exception]) -> None:
	"""
	Check that each precise error exposed by ndp inherits NumdaplotError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	error_class
		A precise numdaplot error.
	"""
	assert issubclass(error_class, ndp.NumdaplotError)


def test_an_invalid_setting_is_caught_by_numdaplot_error() -> None:
	"""
	Check that a user catching NumdaplotError catches an invalid setting.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.NumdaplotError):
		ndp.Quantile(REJECTED_FRACTION)


@pytest.mark.parametrize("warning_class", PRECISE_WARNINGS)
def test_every_precise_warning_is_caught_by_numdaplot_warning(warning_class: type[Warning]) -> None:
	"""
	Check that each precise warning exposed by ndp inherits NumdaplotWarning.

	.. versionadded:: 0.1.0

	Parameters
	----------
	warning_class
		A precise numdaplot warning.
	"""
	assert issubclass(warning_class, ndp.NumdaplotWarning)


def test_a_filter_on_numdaplot_warning_silences_a_precise_warning() -> None:
	"""
	Check that a user ignoring NumdaplotWarning no longer receives a CalculationWarning.

	.. versionadded:: 0.1.0
	"""
	distances = ndp.Array.from_list(ZERO_DISTANCES)
	hours = ndp.Array.from_list(ZERO_HOURS)

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		warnings.simplefilter("ignore", ndp.NumdaplotWarning)
		_ = distances / hours

	assert caught_warnings == []
