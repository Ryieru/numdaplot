"""
Functional tests of the numdaplot errors, as a user catches them.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp

PRECISE_ERRORS = [
	ndp.ColumnNotFoundError,
	ndp.DimensionError,
	ndp.DuplicateColumnError,
	ndp.EmptyArrayError,
	ndp.EmptyListError,
	ndp.EmptyTextError,
	ndp.EmptyValuesError,
	ndp.FileExistsError,
	ndp.FileNotFoundError,
	ndp.IncompatibleTypesError,
	ndp.InvalidBaseError,
	ndp.InvalidBoundsError,
	ndp.InvalidColumnNameError,
	ndp.InvalidCountError,
	ndp.InvalidDeviationError,
	ndp.InvalidFractionError,
	ndp.InvalidPositionError,
	ndp.InvalidSeedError,
	ndp.InvalidSeparatorError,
	ndp.InvalidShapeError,
	ndp.InvalidStepError,
	ndp.IrregularListError,
	ndp.MissingDependencyError,
	ndp.MissingTypeError,
	ndp.NotSingleValueError,
	ndp.OutOfDomainError,
	ndp.RefusedOperationError,
	ndp.ShapeMismatchError,
	ndp.UnsupportedIndexError,
	ndp.UnsupportedMissingError,
	ndp.UnsupportedOperandError,
	ndp.UnsupportedTypeError,
	ndp.ValueConversionError,
]
REJECTED_FRACTION = 2.0


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
