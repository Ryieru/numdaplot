"""
Unit tests of ShownObject.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.plots.output.shown_object import ShownObject


@pytest.mark.parametrize(
	("shown_object", "class_name"),
	[(ShownObject.PLOT, "Plot"), (ShownObject.FIGURE, "Figure")],
)
def test_shown_object_value_is_the_class_name(shown_object: ShownObject, class_name: str) -> None:
	"""
	Check that each kind of shown object gives the name of its class.

	.. versionadded:: 0.1.0

	Parameters
	----------
	shown_object
		The kind of shown object.
	class_name
		The expected class name.
	"""
	assert shown_object.value == class_name
