"""
Functional tests of ndp.Type, as a user reads its members.

.. versionadded:: 0.1.0
"""

import numdaplot as ndp

EXPECTED_TYPE_NAMES = [
	"INT8",
	"INT16",
	"INT32",
	"INT64",
	"UINT8",
	"UINT16",
	"UINT32",
	"UINT64",
	"FLOAT32",
	"FLOAT64",
	"BOOL",
	"TEXT",
	"CATEGORY",
	"DATE",
	"DATETIME",
	"DURATION",
	"TIME",
]


def test_type_offers_every_validated_type() -> None:
	"""
	Check that ndp.Type has exactly the validated members, in order.

	.. versionadded:: 0.1.0
	"""
	type_names = [data_type.name for data_type in ndp.Type]

	assert type_names == EXPECTED_TYPE_NAMES
