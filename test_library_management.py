import pytest
from datetime import datetime, timedelta
from main import Library, main

def test_successful_checkout():
    library = Library()
    selections = [{'book_index': 0, 'quantity': 2}]
    total_late_fees = library.checkout_books(selections)
    assert total_late_fees == 0
    assert library.books[0].quantity == 10
    assert len(library.checked_out_books) == 1
    assert library.checked_out_books[0]['quantity'] == 2