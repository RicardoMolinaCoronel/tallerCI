from datetime import datetime, timedelta


class Book:
    def __init__(self, title, author, quantity):
        self.title = title
        self.author = author
        self.quantity = quantity
        # self.due_date = None


class Library:
    def __init__(self):
        self.books = [
            Book("100 años de soledad", "Author1", 11),
            Book("1984", "Author2", 11),
            # Add more books as needed
        ]
        self.checked_out_books = []
        self.checked_out_books_tmp = []

    def display_catalog(self):
        print("Catalog:")
        for idx, book in enumerate(self.books):
            print(f"{idx + 1}. {book.title} by {book.author} - Available: {book.quantity}")

    def checkout_books(self, selections):
        total_late_fees = 0
        count = 1
        self.checked_out_books_tmp = []
        for selection in selections:

            book = self.books[selection['book_index']]

            if book.quantity >= selection['quantity']:
                book.quantity -= selection['quantity']

                due_date = (datetime.now() + timedelta(days=14))
                # book.due_date = due_date.strftime("%Y-%m-%d")

                self.checked_out_books_tmp.append({
                    'index': selection['book_index'],
                    'title': book.title,
                    'quantity': selection['quantity'],
                    'due_date': due_date,
                    'late_fees': 0
                })
                print(f"Selection {count}: {book.title} have enough copies available: {selection['quantity']}.")

            else:
                print(
                    f"Selection {count}: Error: {book.title} does not have enough copies available: {selection['quantity']}.")
            count += 1
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
        days_overdue = max((datetime.now() - due_date).days, 0)
        return days_overdue


def main():
    library = Library()

    while True:
        print("\n1. Display Catalog")
        print("2. Checkout Books")
        print("3. Return Books")
        print("4. Calculate fees")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            library.display_catalog()
        elif choice == '2':
            selections = get_checkout_input(library)
        elif choice == '3':
            if len(library.checked_out_books) > 0:
                total_late_fees = get_return_input(library)
                print_return_confirmation(total_late_fees)
            else:
                print("There aren't any loans")
        elif choice == '4':
            total = 0
            for checked_out in library.checked_out_books:
                day = library.calculate_late_fee(checked_out["due_date"])
                if day > 0:
                    total += day * checked_out["quantity"]
            print(f"The sum of your total lates fees is: {total}$")

        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def get_checkout_input(library):
    selections = []
    totalQuantity = 0
    no_confirmar = True
    while no_confirmar:
        while True:
            library.display_catalog()
            try:
                book_index = int(input("Enter the index of the book to checkout (0 to finish): ")) - 1
                if book_index == -1:
                    break

                if 0 <= book_index < len(library.books):
                    quantity = int(input("Enter the quantity to checkout: "))
                    totalQuantity += quantity
                    if quantity > 0:
                        if quantity <= library.books[book_index].quantity:
                            if totalQuantity <= 10:
                                selections.append({'book_index': book_index, 'quantity': quantity})
                            else:
                                totalQuantity -= quantity
                                print("You cannot borrow more than 10 books.")
                        else:
                            print("Invalid quantity. There aren't enough copies available.")
                    else:
                        print("Invalid quantity. Please enter a positive integer greater than zero.")

                else:
                    print("Invalid book index. Please enter a valid index.")
            except ValueError:
                print("Please enter an integer")
        try:
            print("\nCheckout Confirmation:")
            for i in range(len(library.checked_out_books_tmp)):
                print(
                    f"{library.checked_out_books_tmp[i]['quantity']} copies of {library.checked_out_books_tmp[i]['title']} due on {library.checked_out_books_tmp[i]['due_date'].strftime('%Y-%m-%d')}")
            total = 0
            for checked_out in selections:
                total += checked_out["quantity"]
            print(
                f"You have 14 days to deliver the books before you have to pay {total}$ for each day late, because 1$ per book is applied.")
            choice = input("Confirm the loan? 1 for yes and other value for cancel and make changes: ")
            if choice == '1':
                library.checkout_books(selections)
                for book in library.checked_out_books_tmp:
                    library.checked_out_books.append(book)
                print("Confirmed loan")
                library.checked_out_books_tmp = []
                no_confirmar = False
            else:
                print("Canceled loan")

        except:
            no_confirmar = True
            print("Canceled loan")
    return selections


def print_checkout_confirmation(selections, total_late_fees, library):
    print("\nCheckout Confirmation:")
    for i in range(len(library.checked_out_books_tmp)):
        print(
            f"{library.checked_out_books_tmp[i]['quantity']} copies of {library.checked_out_books_tmp[i]['title']} due on {library.checked_out_books_tmp[i]['due_date'].strftime('%Y-%m-%d')}")
    print(f"Total Late Fees: ${total_late_fees}")
    choice = input("Confirm the loan? 1 for yes and other value for no: ")
    try:
        if choice == '1':
            for book in library.checked_out_books_tmp:
                library.checked_out_books.append(book)
            print("Confirmed loan")
        else:
            print("Loan canceled")
    except ValueError:
        print("Loan canceled")


def return_books_checkout(index, library, quantity_returned, total_fees):
    if quantity_returned != -1 and 0 < quantity_returned <= library.checked_out_books[index - 1]['quantity']:
        days = library.calculate_late_fee(library.checked_out_books[index - 1]['due_date'])
        quantityBooks = library.checked_out_books[index - 1]['quantity']
        library.checked_out_books[index - 1]['quantity'] -= quantity_returned
        library.books[library.checked_out_books[index - 1]['index']].quantity += quantity_returned
        if days > 0:
            total_fees += days * quantityBooks
        if library.checked_out_books[index - 1]['quantity'] <= 0:
            del library.checked_out_books[index - 1]
        return total_fees
    else:
        print("Invalid quantity. Please enter a valid quantity.")
        return 0

def get_return_input(library):
    total_fees = 0
    print("Those are your loans: ")
    for i in range(len(library.checked_out_books)):
        print(f"{i + 1}: {library.checked_out_books[i]['title']}, quantity: {library.checked_out_books[i]['quantity']}")

    index = int(input("Select a loan option: "))
    if index != -1 and 0 < index <= len(library.checked_out_books):
        quantity_returned = int(input("Enter the quantity to return: "))
        return_books_checkout(index, library, quantity_returned, total_fees)
    else:
        print("Invalid option. Please enter one of the options that are available.")

    return total_fees


def print_return_confirmation(total_late_fees):
    print("\nReturn details:")
    print(f"Total Late Fees: ${total_late_fees}")


if __name__ == "__main__":
    main()
