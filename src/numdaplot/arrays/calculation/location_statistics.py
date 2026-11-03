"""
Statistics locating or summing the values of an Array: sum, mean, median, deviation, quantile, min, max.

Each function ignores missing values and reduces the whole Array when ``axis`` is ``None``.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
from numpy.typing import NDArray

from numdaplot.statistics.quantile import Quantile
from numdaplot.statistics.statistic import Statistic

MISSING_AWARE_KINDS = frozenset({"f", "M", "m"})
POPULATION_DEGREES_OF_FREEDOM = 0


def compute_sum(values: NDArray[Any], axis: int | None, statistic: Statistic) -> Any:
	"""
	Return the sum of the present values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a number or boolean Array.
	axis
		The numpy axis to reduce, or ``None`` for the whole Array.
	statistic
		The ``Sum`` statistic.

	Returns
	-------
	Any
		A single value, or one value per reduced slice.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.location_statistics import compute_sum
	>>> compute_sum(numpy.array([1.0, numpy.nan, 2.0]), None, ndp.Sum())
	np.float64(3.0)
	"""
	total = numpy.nansum(values, axis=axis)

	return total


def compute_mean(values: NDArray[Any], axis: int | None, statistic: Statistic) -> Any:
	"""
	Return the mean of the present values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a number or boolean Array, at least one present value per slice.
	axis
		The numpy axis to reduce, or ``None`` for the whole Array.
	statistic
		The ``Mean`` statistic.

	Returns
	-------
	Any
		A single value, or one value per reduced slice.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.location_statistics import compute_mean
	>>> compute_mean(numpy.array([1.0, numpy.nan, 3.0]), None, ndp.Mean())
	np.float64(2.0)
	"""
	mean = numpy.nanmean(values, axis=axis)

	return mean


def compute_median(values: NDArray[Any], axis: int | None, statistic: Statistic) -> Any:
	"""
	Return the median of the present values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a number Array, at least one present value per slice.
	axis
		The numpy axis to reduce, or ``None`` for the whole Array.
	statistic
		The ``Median`` statistic.

	Returns
	-------
	Any
		A single value, or one value per reduced slice.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.location_statistics import compute_median
	>>> compute_median(numpy.array([1, 9, 2]), None, ndp.Median())
	np.float64(2.0)
	"""
	median = numpy.nanmedian(values, axis=axis)

	return median


def compute_standard_deviation(values: NDArray[Any], axis: int | None, statistic: Statistic) -> Any:
	"""
	Return the population standard deviation of the present values, divided by their number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a number Array, at least one present value per slice.
	axis
		The numpy axis to reduce, or ``None`` for the whole Array.
	statistic
		The ``StandardDeviation`` statistic.

	Returns
	-------
	Any
		A single value, or one value per reduced slice.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.location_statistics import compute_standard_deviation
	>>> compute_standard_deviation(numpy.array([2, 4]), None, ndp.StandardDeviation())
	np.float64(1.0)
	"""
	deviation = numpy.nanstd(values, axis=axis, ddof=POPULATION_DEGREES_OF_FREEDOM)

	return deviation


def compute_quantile(values: NDArray[Any], axis: int | None, statistic: Statistic) -> Any:
	"""
	Return the value below which a fraction of the present values lies.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a number Array, at least one present value per slice.
	axis
		The numpy axis to reduce, or ``None`` for the whole Array.
	statistic
		The ``Quantile`` statistic, holding the fraction.

	Returns
	-------
	Any
		A single value, or one value per reduced slice.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.location_statistics import compute_quantile
	>>> compute_quantile(numpy.array([0, 10]), None, ndp.Quantile(0.9))
	np.float64(9.0)
	"""
	quantile = cast(Quantile, statistic)
	quantile_values = numpy.nanquantile(values, quantile.fraction, axis=axis)

	return quantile_values


def compute_minimum(values: NDArray[Any], axis: int | None, statistic: Statistic) -> Any:
	"""
	Return the lowest present value: the smallest number, the first text in alphabetical order, the earliest date.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array, at least one present value per slice.
	axis
		The numpy axis to reduce, or ``None`` for the whole Array.
	statistic
		The ``Min`` statistic.

	Returns
	-------
	Any
		A single value, or one value per reduced slice.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.location_statistics import compute_minimum
	>>> compute_minimum(numpy.array([3.0, numpy.nan, 1.0]), None, ndp.Min())
	np.float64(1.0)
	"""
	if values.dtype.kind in MISSING_AWARE_KINDS:
		present_minimum = numpy.nanmin(values, axis=axis)
		return present_minimum

	minimum = numpy.min(values, axis=axis)

	return minimum


def compute_maximum(values: NDArray[Any], axis: int | None, statistic: Statistic) -> Any:
	"""
	Return the highest present value: the largest number, the last text in alphabetical order, the latest date.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array, at least one present value per slice.
	axis
		The numpy axis to reduce, or ``None`` for the whole Array.
	statistic
		The ``Max`` statistic.

	Returns
	-------
	Any
		A single value, or one value per reduced slice.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.location_statistics import compute_maximum
	>>> compute_maximum(numpy.array(["b", "c", "a"], dtype="T"), None, ndp.Max())
	'c'
	"""
	if values.dtype.kind in MISSING_AWARE_KINDS:
		present_maximum = numpy.nanmax(values, axis=axis)
		return present_maximum

	maximum = numpy.max(values, axis=axis)

	return maximum
