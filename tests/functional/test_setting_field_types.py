"""
Functional test giving a value of the wrong type to every field of every setting object of the public API.

A new setting object without the check, or an annotation that cannot be read, makes this test fail.

.. versionadded:: 0.1.0
"""

import dataclasses
import inspect
from dataclasses import dataclass
from typing import Any, cast

import pytest

import numdaplot as ndp

CASE_ID = "{class_name}.{field_name}"
SUM_CALCULATION = ndp.Calculation(column="a", function=ndp.Sum())
ONE_PART = ndp.Array.from_list([1])
JOINED_TABLE = ndp.Table.from_arrays({"a": ONE_PART})
REQUIRED_SETTINGS = dict[str, dict[str, object]](
	{
		"Aggregation": {"calculations": [SUM_CALCULATION]},
		"ArrayConversion": {"dtype": ndp.Type.TEXT},
		"Between": {"low": 1, "high": 2},
		"BinCount": {"count": 1},
		"BinWidth": {"width": 1.0},
		"Brackets": {"limits": [0, 1]},
		"Calculation": {"column": "a", "function": ndp.Sum()},
		"Cell": {"row": 0, "column": 0},
		"ColumnChoice": {"columns": ["a"]},
		"Condition": {"rule": ndp.IsMissing()},
		"Contains": {"text": "a"},
		"CustomColor": {"code": "#ff8800"},
		"CustomDateFormat": {"pattern": "%d"},
		"DatePart": {"unit": ndp.DatePartUnit.MONTH},
		"DateParts": {"year": ONE_PART, "month": ONE_PART, "day": ONE_PART},
		"DatePeriod": {"unit": ndp.PeriodUnit.MONTH},
		"DurationIn": {"unit": ndp.DurationUnit.DAY},
		"Equal": {"value": 1},
		"Equality": {"other": ndp.Array.from_list([1])},
		"Filter": {"conditions": [ndp.Condition(rule=ndp.IsMissing())]},
		"Greater": {"value": 1},
		"GreaterOrEqual": {"value": 1},
		"Index": {"position": 0},
		"IsIn": {"values": [1]},
		"Join": {"other": JOINED_TABLE, "keys": ["a"]},
		"JoinSuffixes": {"left": "_a", "right": "_b"},
		"Layout": {"rows": 1, "columns": 1},
		"Less": {"value": 1},
		"LessOrEqual": {"value": 1},
		"MissingRatio": {"ratio": 0.5},
		"NameChange": {"old_name": "a", "new_name": "b"},
		"NewColumn": {"name": "a", "values": ndp.Array.from_list([1])},
		"Normal": {"mean": 0, "deviation": 1},
		"NotEqual": {"value": 1},
		"PieChart": {"labels": "a", "values": "b"},
		"PivotTable": {"rows": ["a"], "columns": "b", "calculation": SUM_CALCULATION},
		"Quantile": {"fraction": 0.5},
		"RandomIntegers": {"low": 0, "high": 1},
		"Range": {"start": 0, "stop": 1},
		"Region": {"rows": ndp.Index(0)},
		"Renaming": {"changes": [ndp.NameChange(old_name="a", new_name="b")]},
		"Replacement": {"region": ndp.Region(rows=ndp.Index(0)), "value": 1},
		"Shape": {"dimensions": [1]},
		"SortKey": {"column": "a"},
		"Spacing": {"start": 0, "stop": 1, "count": 2},
		"TableConversion": {"column": "a", "dtype": ndp.Type.TEXT},
		"TableSorting": {"keys": [ndp.SortKey(column="a")]},
		"TimeZone": {"name": "UTC"},
		"TimeZoneChange": {"mode": ndp.TimeZoneMode.REMOVE},
		"ToDuration": {"unit": ndp.DurationUnit.DAY},
		"Uniform": {"low": 0, "high": 1},
		"ValueChange": {"old_value": 1, "new_value": "a"},
		"ValueCount": {"column": "a"},
		"ValueMapping": {"changes": [ndp.ValueChange(1, "a")]},
	}
)


class WrongValue:
	"""
	A value no setting accepts.

	.. versionadded:: 0.1.0
	"""


@dataclass(frozen=True)
class FieldCase:
	"""
	One field of a setting object of the public API.

	.. versionadded:: 0.1.0

	Parameters
	----------
	setting_class
		The class of the setting object.
	field_name
		The name of the field.
	"""

	setting_class: type
	field_name: str


def list_field_cases() -> list[FieldCase]:
	"""
	Return every field of every dataclass numdaplot exports, its errors left out.

	.. versionadded:: 0.1.0

	Returns
	-------
	list[FieldCase]
		One case per field.
	"""
	cases = list[FieldCase]()

	for name in ndp.__all__:
		exported = getattr(ndp, name)
		is_setting = inspect.isclass(exported) and dataclasses.is_dataclass(exported)
		if not is_setting:
			continue

		setting_class = cast(Any, exported)

		for field in dataclasses.fields(setting_class):
			case = FieldCase(setting_class, field.name)
			cases.append(case)

	return cases


FIELD_CASES = list_field_cases()
FIELD_CASE_IDS = [
	CASE_ID.format(class_name=case.setting_class.__name__, field_name=case.field_name) for case in FIELD_CASES
]


@pytest.mark.parametrize("case", FIELD_CASES, ids=FIELD_CASE_IDS)
def test_every_field_refuses_a_value_of_the_wrong_type(case: FieldCase) -> None:
	"""
	Check that a value of the wrong type raises InvalidTypeError when the setting object is created.

	.. versionadded:: 0.1.0

	Parameters
	----------
	case
		The field given the wrong value.
	"""
	class_name = case.setting_class.__name__
	required_settings = REQUIRED_SETTINGS.get(class_name, {})
	settings = required_settings | {case.field_name: WrongValue()}

	with pytest.raises(ndp.InvalidTypeError):
		case.setting_class(**settings)


def test_every_setting_object_is_found() -> None:
	"""
	Check that the search finds the settings, such as the count of Preview.

	.. versionadded:: 0.1.0
	"""
	assert "Preview.count" in FIELD_CASE_IDS
