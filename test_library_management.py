from unittest import mock

import pytest
from datetime import datetime, timedelta
from main import Library, main, return_books_checkout

def test_successful_checkout():
    library = Library()
    selections = [{'book_index': 0, 'quantity': 2}]
    total_late_fees = library.checkout_books(selections)
    assert total_late_fees == 0
    assert library.books[0].quantity == 8
    assert len(library.checked_out_books_tmp) == 1
    assert library.checked_out_books_tmp[0]['quantity'] == 2

def test_checkout_unavailable_book():
    library = Library()
    selections = [{'book_index': 0, 'quantity': 12}]
    total_late_fees = library.checkout_books(selections)
    assert total_late_fees == 0
    assert library.books[0].quantity == 11
    assert len(library.checked_out_books_tmp) == 0

def test_max_books_per_checkout():
    library = Library()
    selections = [{'book_index': 1, 'quantity': 6}, {'book_index': 1, 'quantity': 5}]
    total_late_fees = library.checkout_books(selections)
    assert total_late_fees == 0
    assert all(book.quantity == 11 for book in library.books)  # Verifica que el inventario no se ve afectado
    assert len(library.checked_out_books_tmp) == 0  # Verifica que no se prestó ningún libro

def test_return_no_late_fee():
    library = Library()
    library.checked_out_books = [{'index': 1,'title': '1984', 'quantity': 1, 'due_date': datetime.now() - timedelta(days=15), 'late_fees': 0}]
    total_late_fees = main().return_books_checkout(0,library,1,0)
    assert total_late_fees == 0
    assert library.books[0].quantity == 12
    assert len(library.checked_out_books) == 0
def test_return_late_fee():
    library = Library()
    library.checked_out_books = [{'index':1, 'title': '1984', 'quantity': 1, 'due_date': datetime.now() - timedelta(days=15), 'late_fees': 0}]
    total_late_fees = return_books_checkout(0,library,1,0)
    assert total_late_fees == 1  # Se espera un cargo por retraso de $1
    assert library.books[0].quantity == 12  # Verifica que se incrementó el inventario
    assert len(library.checked_out_books) == 0  # Verifica que el libro fue devuelto

def test_invalid_book_index_checkout():
    library = Library()
    selections = [{'book_index': len(library.books), 'quantity': 1}]
    total_late_fees = library.checkout_books(selections)
    assert total_late_fees == 0
    assert all(book.quantity == 11 for book in library.books)  # Verifica que el inventario no se ve afectado
    assert len(library.checked_out_books_tmp) == 0  # Verifica que no se prestó ningún libro

def test_invalid_quantity_return():
    library = Library()
    library.checked_out_books = [{'index':1,'title': '1984', 'quantity': 2, 'due_date': '2023-01-01', 'late_fees': 0}]
    total_late_fees = return_books_checkout(1,library,-1,0)
    assert total_late_fees == 0
    assert library.books[0].quantity == 11  # Verifica que el inventario no se ve afectado
    assert len(library.checked_out_books) == 1  # Verifica que el libro no fue devuelto

def test_invalid_menu_choice():
    library = Library()
    with pytest.raises(SystemExit):
        with mock.patch('builtins.input', return_value='7'):
            main()
    assert all(book.quantity == 11 for book in library.books)
    assert len(library.checked_out_books) == 0

def test_accumulated_late_fees():
    library = Library()
    library.checked_out_books = [{'index':0,'title': '1984', 'quantity': 2, 'due_date': datetime.now() - timedelta(days=15), 'late_fees': 0},{'index':1,'title': '1984', 'quantity': 2, 'due_date': datetime.now() - timedelta(days=15), 'late_fees': 0}]
    total_late_fees = return_books_checkout(0,library,2,0) + return_books_checkout(1,library,2,0)
    assert total_late_fees == 4