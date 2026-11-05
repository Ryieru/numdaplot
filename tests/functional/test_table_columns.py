"""
Functional tests of the column operations of a Table.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

import numdaplot as ndp

CITIES = ["Paris", "Lyon"]
PRICES = [10.0, 20.0]
ZIP_CODES = ["06000", "75001"]
EXPECTED_ZIP_NUMBERS = [6000, 75001]
WRONG_ZIP_CODES = ["06000", "Nice"]
EXPECTED_CONVERSION_MESSAGE = "Cannot store the TEXT value 'Nice' as INT32 without losing information."
TAX_RATE = 1.2
EXPECTED_TAXED_PRICES = [12.0, 24.0]
EXPECTED_ADDED_NAMES = ["city", "price", "zip_code", "taxed_price"]
EXPECTED_KEPT_NAMES = ["price", "city"]
EXPECTED_SWAPPED_NAMES = ["price", "city", "zip_code"]
EXPECTED_PRICE_TEXTS = ["10.0", "20.0"]
MISSPELLED_COLUMN = "prise"


def build_shops() -> ndp.Table:
	"""
	Return a Table of two shops.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Table
		The shops.
	"""
	cities = ndp.Array.from_list(CITIES)
	prices = ndp.Array.from_list(PRICES)
	zip_codes = ndp.Array.from_list(ZIP_CODES)
	shops = ndp.Table.from_arrays({"city": cities, "price": prices, "zip_code": zip_codes})

	return shops


def test_columns_are_kept_in_the_order_of_the_choice() -> None:
	"""
	Check that KEEP orders the columns as listed.

	.. versionadded:: 0.1.0
	"""
	shops = build_shops()

	chosen_shops = shops.choose_columns(ndp.ColumnChoice(columns=["price", "city"]))

	assert chosen_shops.column_names == EXPECTED_KEPT_NAMES


def test_two_columns_swap_their_names_in_one_call() -> None:
	"""
	Check that city and price swap their names.

	.. versionadded:: 0.1.0
	"""
	shops = build_shops()
	swap = [ndp.NameChange(old_name="city", new_name="price"), ndp.NameChange(old_name="price", new_name="city")]

	renamed_shops = shops.rename(ndp.Renaming(changes=swap))

	assert renamed_shops.column_names == EXPECTED_SWAPPED_NAMES


def test_zip_codes_written_as_texts_become_numbers() -> None:
	"""
	Check that texts of numbers convert to INT32.

	.. versionadded:: 0.1.0
	"""
	shops = build_shops()

	converted_shops = shops.convert(ndp.Conversion(column="zip_code", dtype=ndp.Type.INT32))

	zip_numbers = converted_shops.column("zip_code")
	zip_list = zip_numbers.to_list()
	assert zip_list == EXPECTED_ZIP_NUMBERS


def test_a_text_that_is_not_a_number_is_named_in_the_error() -> None:
	"""
	Check the message naming the first wrong text.

	.. versionadded:: 0.1.0
	"""
	cities = ndp.Array.from_list(CITIES)
	wrong_codes = ndp.Array.from_list(WRONG_ZIP_CODES)
	shops = ndp.Table.from_arrays({"city": cities, "zip_code": wrong_codes})

	with pytest.raises(ndp.ValueConversionError) as error_info:
		shops.convert(ndp.Conversion(column="zip_code", dtype=ndp.Type.INT32))

	error_text = str(error_info.value)
	assert error_text == EXPECTED_CONVERSION_MESSAGE


def test_numbers_become_texts() -> None:
	"""
	Check the texts of the prices.

	.. versionadded:: 0.1.0
	"""
	shops = build_shops()

	text_shops = shops.convert(ndp.Conversion(column="price", dtype=ndp.Type.TEXT))

	price_texts = text_shops.column("price")
	text_list = price_texts.to_list()
	assert text_list == EXPECTED_PRICE_TEXTS


def test_a_column_computed_from_another_one_is_added_last() -> None:
	"""
	Check that taxed prices are computed with an Array and added as a new column.

	.. versionadded:: 0.1.0
	"""
	shops = build_shops()
	prices = shops.column("price")
	taxed_prices = prices * TAX_RATE

	taxed_shops = shops.add_column(ndp.NewColumn(name="taxed_price", values=taxed_prices))

	taxed_column = taxed_shops.column("taxed_price")
	taxed_list = taxed_column.to_list()
	assert taxed_shops.column_names == EXPECTED_ADDED_NAMES
	are_close = numpy.allclose(taxed_list, EXPECTED_TAXED_PRICES)
	assert are_close


def test_an_existing_column_is_replaced_only_when_asked() -> None:
	"""
	Check that an existing name raises DuplicateColumnError, and REPLACE keeps the column at its place.

	.. versionadded:: 0.1.0
	"""
	shops = build_shops()
	prices = shops.column("price")
	taxed_prices = prices * TAX_RATE

	with pytest.raises(ndp.DuplicateColumnError):
		shops.add_column(ndp.NewColumn(name="price", values=taxed_prices))

	replacing_column = ndp.NewColumn(name="price", values=taxed_prices, on_conflict=ndp.Conflict.REPLACE)
	replaced = shops.add_column(replacing_column)
	assert replaced.column_names == shops.column_names


def test_an_unknown_column_is_named_in_the_error() -> None:
	"""
	Check that a misspelled column raises ColumnNotFoundError with its name.

	.. versionadded:: 0.1.0
	"""
	shops = build_shops()

	with pytest.raises(ndp.ColumnNotFoundError) as error_info:
		shops.column(MISSPELLED_COLUMN)

	error = error_info.value
	assert error.column_name == MISSPELLED_COLUMN
