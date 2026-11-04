"""
Look every Plot is drawn with.

.. versionadded:: 0.1.0
"""

from typing import Any

BACKGROUND_COLOR = "#ffffff"
"""Background color of every Plot, behind and inside its axes.

.. versionadded:: 0.1.0
"""

THEME = dict[str, Any](
	{
		"font.size": 11,
		"axes.titlesize": 13,
		"axes.titlepad": 12,
		"axes.labelsize": 11,
		"axes.labelcolor": "#333333",
		"axes.edgecolor": "#555555",
		"axes.facecolor": BACKGROUND_COLOR,
		"axes.spines.top": False,
		"axes.spines.right": False,
		"axes.axisbelow": True,
		"xtick.color": "#555555",
		"ytick.color": "#555555",
		"grid.color": "#e3e3e3",
		"grid.linewidth": 0.8,
		"legend.frameon": False,
		"lines.linewidth": 2.0,
		"lines.markersize": 6.0,
	}
)
"""matplotlib settings applied while a Plot is drawn, never to the global matplotlib settings.

.. versionadded:: 0.1.0
"""
