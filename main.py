from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, quantity):
        self.title = title
        self.author = author
        self.quantity = quantity
        self.due_date = None

class Library:
    def __init__(self):
        self.books = [
            Book("Book1", "Author1", 5),
            Book("Book2", "Author2", 3),
            # Add more books as needed
        ]
        self.checked_out_books = []

    def display_catalog(self):
        print("Catalog:")
        for idx, book in enumerate(self.books):
            print(f"{idx + 1}. {book.title} by {book.author} - Available: {book.quantity}")

    def checkout_books(self, selections):
        total_late_fees = 0

        for selection in selections:
            book = self.books[selection['book_index']]

            if book.quantity >= selection['quantity']:
                book.quantity -= selection['quantity']

                due_date = datetime.now() + timedelta(days=14)
                book.due_date = due_date.strftime("%Y-%m-%d")

                self.checked_out_books.append({
                    'title': book.title,
                    'quantity': selection['quantity'],
                    'due_date': book.due_date,
                    'late_fees': 0
                })
            else:
                print(f"Error: {book.title} does not have enough copies available.")

        return total_late_fees

    def return_books(self, return_details):
        total_late_fees = 0

        for return_detail in return_details:
            book_title = return_detail['title']
            quantity_returned = return_detail['quantity']

            for checked_out_book in self.checked_out_books:
                if checked_out_book['title'] == book_title:
                    late_fee = self.calculate_late_fee(checked_out_book['due_date'])
                    total_late_fees += late_fee

                    checked_out_book['quantity'] -= quantity_returned
                    checked_out_book['late_fees'] += late_fee

                    if checked_out_book['quantity'] == 0:
                        self.checked_out_books.remove(checked_out_book)

        return total_late_fees

    def calculate_late_fee(self, due_date):
        due_date = datetime.strptime(due_date, "%Y-%m-%d")
        days_overdue = max((datetime.now() - due_date).days, 0)
        return days_overdue

def main():
    library = Library()

    while True:
        print("\n1. Display Catalog")
        print("2. Checkout Books")
        print("3. Return Books")
        print("4. Quit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            library.display_catalog()
        elif choice == '2':
            selections = get_checkout_input(library)
            total_late_fees = library.checkout_books(selections)
            print_checkout_confirmation(selections, total_late_fees)
        elif choice == '3':
            return_details = get_return_input(library)
            total_late_fees = library.return_books(return_details)
            print_return_confirmation(return_details, total_late_fees)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

def get_checkout_input(library):
    selections = []

    while True:
        library.display_catalog()
        book_index = int(input("Enter the index of the book to checkout (0 to cancel): ")) - 1

        if book_index == -1:
            break

        if 0 <= book_index < len(library.books):
            quantity = int(input("Enter the quantity to checkout: "))
            if quantity > 0:
                selections.append({'book_index': book_index, 'quantity': quantity})
            else:
                print("Invalid quantity. Please enter a positive integer greater than zero.")
        else:
            print("Invalid book index. Please enter a valid index.")

    return selections

def print_checkout_confirmation(selections, total_late_fees):
    print("\nCheckout Confirmation:")
    for selection in selections:
        print(f"{selection['quantity']} copies of {selection['book_title']} due on {selection['due_date']}")
    print(f"Total Late Fees: ${total_late_fees}")

def get_return_input(library):
    return_details = []

    while True:
        book_title = input("Enter the title of the book to return (or '0' to finish): ")

        if book_title == '0':
            break

        quantity_returned = int(input("Enter the quantity to return: "))
        if quantity_returned > 0:
            return_details.append({'title': book_title, 'quantity': quantity_returned})
        else:
            print("Invalid quantity. Please enter a positive integer greater than zero.")

    return return_details

def print_return_confirmation(return_details, total_late_fees):
    print("\nReturn Confirmation:")
    for return_detail in return_details:
        print(f"{return_detail['quantity']} copies of {return_detail['title']} returned")
    print(f"Total Late Fees: ${total_late_fees}")

if __name__ == "__main__":
    main()
