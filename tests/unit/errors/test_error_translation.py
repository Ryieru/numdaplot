"""
Unit tests of the base class of the blocks translating the errors raised inside them.

.. versionadded:: 0.2.0
"""

import pytest

from numdaplot.errors.error_translation import ErrorTranslation

BLOCK_MESSAGE = "wrong value"


class RecordedTranslation(ErrorTranslation):
	"""
	Block keeping the errors it is given to translate, and letting them go on.

	.. versionadded:: 0.2.0
	"""

	def __init__(self) -> None:
		"""
		Start without error.

		.. versionadded:: 0.2.0
		"""
		self.errors = list[BaseException]()

	def translate_error(self, error: BaseException) -> None:
		"""
		Keep the error, which then goes on unchanged.

		.. versionadded:: 0.2.0

		Parameters
		----------
		error
			The error raised by the block.
		"""
		self.errors.append(error)


def test_error_translation_hands_the_error_of_the_block() -> None:
	"""
	Check that an error raised in the block goes to translate_error, then goes on.

	.. versionadded:: 0.2.0
	"""
	translation = RecordedTranslation()

	with pytest.raises(ValueError) as error_info, translation:
		raise ValueError(BLOCK_MESSAGE)

	assert translation.errors == [error_info.value]


def test_error_translation_leaves_a_block_without_error() -> None:
	"""
	Check that a block ending without error translates nothing.

	.. versionadded:: 0.2.0
	"""
	translation = RecordedTranslation()

	with translation:
		block_result = BLOCK_MESSAGE

	assert block_result == BLOCK_MESSAGE
	assert translation.errors == []


def test_error_translation_leaves_the_translation_to_each_block() -> None:
	"""
	Check that the base class has no translation of its own.

	.. versionadded:: 0.2.0
	"""
	base_translation = ErrorTranslation()
	block_error = ValueError(BLOCK_MESSAGE)

	with pytest.raises(NotImplementedError):
		base_translation.translate_error(block_error)
