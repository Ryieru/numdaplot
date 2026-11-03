"""
numdaplot: a simpler, explicit API over numpy, pandas and matplotlib.

Import it as ``ndp``; every public name is available directly under it.

.. versionadded:: 0.1.0

Examples
--------
>>> import numdaplot as ndp
>>> ndp.Between(low=10, high=20)
Between(low=10, high=20, bounds=<Bounds.INCLUDED: 1>)
"""

from numdaplot.data_types.type import Type
from numdaplot.errors.broadcast_warning import BroadcastWarning
from numdaplot.errors.empty_text_error import EmptyTextError
from numdaplot.errors.empty_values_error import EmptyValuesError
from numdaplot.errors.invalid_bounds_error import InvalidBoundsError
from numdaplot.errors.invalid_fraction_error import InvalidFractionError
from numdaplot.errors.invalid_step_error import InvalidStepError
from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.unsupported_type_error import UnsupportedTypeError
from numdaplot.ordering.missing_position import MissingPosition
from numdaplot.ordering.order import Order
from numdaplot.positions.axis import Axis
from numdaplot.positions.index import Index
from numdaplot.positions.range import Range
from numdaplot.positions.region import Region
from numdaplot.rules.between import Between
from numdaplot.rules.bounds import Bounds
from numdaplot.rules.case import Case
from numdaplot.rules.contains import Contains
from numdaplot.rules.equal import Equal
from numdaplot.rules.greater import Greater
from numdaplot.rules.greater_or_equal import GreaterOrEqual
from numdaplot.rules.is_in import IsIn
from numdaplot.rules.is_missing import IsMissing
from numdaplot.rules.is_present import IsPresent
from numdaplot.rules.less import Less
from numdaplot.rules.less_or_equal import LessOrEqual
from numdaplot.rules.not_equal import NotEqual
from numdaplot.rules.rule import Rule
from numdaplot.statistics.count import Count
from numdaplot.statistics.count_distinct import CountDistinct
from numdaplot.statistics.maximum import Max
from numdaplot.statistics.mean import Mean
from numdaplot.statistics.median import Median
from numdaplot.statistics.minimum import Min
from numdaplot.statistics.most_frequent import MostFrequent
from numdaplot.statistics.most_frequent_count import MostFrequentCount
from numdaplot.statistics.quantile import Quantile
from numdaplot.statistics.standard_deviation import StandardDeviation
from numdaplot.statistics.statistic import Statistic
from numdaplot.statistics.sum import Sum

__all__ = [
	"Axis",
	"Between",
	"Bounds",
	"BroadcastWarning",
	"Case",
	"Contains",
	"Count",
	"CountDistinct",
	"EmptyTextError",
	"EmptyValuesError",
	"Equal",
	"Greater",
	"GreaterOrEqual",
	"Index",
	"InvalidBoundsError",
	"InvalidFractionError",
	"InvalidStepError",
	"IsIn",
	"IsMissing",
	"IsPresent",
	"Less",
	"LessOrEqual",
	"Max",
	"Mean",
	"Median",
	"Min",
	"MissingPosition",
	"MostFrequent",
	"MostFrequentCount",
	"NotEqual",
	"NumdaplotError",
	"Order",
	"Quantile",
	"Range",
	"Region",
	"Rule",
	"StandardDeviation",
	"Statistic",
	"Sum",
	"Type",
	"UnsupportedTypeError",
]
