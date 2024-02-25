import os
from library.utils.visualizer import CLITable
from library.object_models.book import Book
from library.logger import log_info


class Library:
    def __init__(self, filename):
        self.file = open(filename, mode="a+")

    def __del__(self):
        self.file.close()

    """ This method compares the size of the file before and after the operation."""

    @staticmethod
    def compare_file_size(file_name: str) -> int:
        return os.stat(file_name).st_size

    """ This method lists all the books in the file. It returns list. (Theoretically , Project prerequisite)"""

    def list_books(self) -> list:
        self.file.seek(0)
        return [(Book(*line.strip().split(",")) for line in self.file.readlines())]

    @log_info
    def add_book(self, book: Book):
        if not book.is_valid():
            print("(X) -> Invalid book. Please try again with valid details.")
            return

        try:
            self.file.write(str(book) + "\n")
            self.file.flush()
            print(f"-> Book with Title: {book.title} added successfully")
        except Exception as e:
            print("(X) -> ", e)

    """ This method removes the book from the file. It takes title as an argument. I tried to handle with the non Pythonic file handling.
    With stick to the project prerequisites.
    """

    @log_info
    def remove_book(self, title):
        before_file_stats = self.compare_file_size(self.file.name)

        updated_books = [(book for book in self.list_books()[0] if book.title != title)]
        self.confirm(updated_books)
        self.__del__()

        after_file_stats = self.compare_file_size(self.file.name)
        self.file = open(self.file.name, mode="a+")
        if after_file_stats == before_file_stats:
            print(f"(X) -> Book with title: '{title}' not found")
        else:
            print(f"-> Book with Title: {title} removed successfully")

    """ This method cencores the author from the file. It takes author as an argument. But I did not finalize the method. Little joke."""

    def cencore_author(self, author):
        while True:
            is_sure = input("Are you sure? (y/n): ")
            if is_sure == "y":
                break
        # updated_books = [(book for book in self.list_books()[0] if book.author != author)]
        # self.confirm(updated_books)
        print("-> All books removed successfully")

    """ This method removes the books from the file by release date. It takes release date as an argument. 
        But I did not implemented to the main function. I just wanted to show the method."""

    def remove_books_by_release_date(self, release_date):
        updated_books = [
            (book for book in self.list_books()[0] if book.release_date != release_date)
        ]
        self.confirm(updated_books)

    # Writes updated books to the file
    def confirm(self, books: list) -> bool:
        try:
            self.file.seek(0)
            self.file.truncate()
            for book in books[0]:
                self.file.write(str(book) + "\n")
            self.file.flush()
            return True
        except Exception as e:
            print(e)
            return False


""" Main function to run the application wit If Else statements related to the project prerequisites."""

lib = Library("books.txt")


def main():

    while True:
        awesome_gui = CLITable("Main Menu", columns=["Options", "Methods"])
        menu_options = ["List Books", "Add Book", "Remove Book", "Exit"]

        for index, item in enumerate(menu_options):
            awesome_gui.table.add_row(str(index + 1), item)
        awesome_gui.show()
        choice = int(input("Enter your choice: "))

        if choice not in range(1, len(menu_options) + 1):
            print("(X) -> Invalid choice")
            continue

        if choice == 1:
            all_books = lib.list_books()
            cli_visualizer = CLITable(
                "Books",
                columns=["Title", "Author"],
                rows=[[book.title, book.author] for book in all_books[0]],
            )
            cli_visualizer.show()

        elif choice == 2:

            ask_for = ["Title", "Author", "Release Date", "Number of Pages"]
            title, author, release_date, num_of_pages = [
                input(f"Enter {item}: ") for item in ask_for
            ]
            book = Book(title, author, release_date, num_of_pages)
            lib.add_book(book)

        elif choice == 3:
            title = input("Enter title: ")
            print(f"-> Removing book with title: {title} .....")
            lib.remove_book(title)
        elif choice == 4:
            break
        else:
            print("(X) -> Invalid choice")


if __name__ == "__main__":
    main()
