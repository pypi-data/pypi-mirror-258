import argparse
import os
from library.object_models.book import Book
from library.utils.helpers.dummy import DummyData
import library.app as app
from time import perf_counter


dummy_data_file_path = "dummy.txt"


""" Loads dummy data to the file. File path is optional. Size is required.
After the process checks if file is created succesfully."""


def load_dummy_data(size, path=dummy_data_file_path):
    print(f"Loading {size} dummy Book data")
    data = DummyData(size)
    data.write_to_file(path)
    if path in os.path.abspath(path):
        print(f"{size} Data loaded to {path} Successfully")
    else:
        print(
            "Error occurred while writing to file. Check the file path or file permissions. And try again."
        )


""" Monitor the performance of the application. 
It is not a best practice to use the time module for performance monitoring. 
But better than nothing. (info: I did not delete the loggers from the app.py file.)
"""


def monitor():
    if not os.path.exists(dummy_data_file_path):
        print(
            f"File '{dummy_data_file_path}' not found. Do you want to create dummy data first? (y/n)"
        )
        user_input = input("-> ")
        if user_input == "y":
            print("How many dummy data do you want to create?")
            size = int(input("-> "))
            # It is not best practice to not validate the user input. But for the sake of simplicity, I did not validate it properly.
            load_dummy_data(size)

        else:
            print("Exiting...")

    lib = app.Library(dummy_data_file_path)

    while True:
        menu_options = {
            "1": "List Books",
            "2": "Add Book",
            "3": "Remove Book",
            "4": "Exit",
        }
        for key, value in menu_options.items():
            print(f"{key} -> {value}")

        choice = input("Enter your choice: ")
        if choice not in menu_options.keys():
            print("Invalid choice")
            continue

        if choice == "1":
            start = perf_counter()
            lib.list_books()
            end = perf_counter()
            print(f"List Books: executed in {end - start:.5f} seconds")
        elif choice == "2":
            ask_for = ["Title", "Author", "Release Date", "Number of Pages"]
            title, author, release_date, num_of_pages = [
                input(f"Enter {item}: ") for item in ask_for
            ]
            start = perf_counter()
            lib.add_book(Book(title, author, release_date, num_of_pages))
            end = perf_counter()
            print(f"Add Book: executed in {end - start:.5f} seconds")
        elif choice == "3":
            title = input("Enter title: ")
            start = perf_counter()
            lib.remove_book(title)
            end = perf_counter()
            print(f"Remove Book: executed in {end - start:.5f} seconds")
        elif choice == "4":
            if os.path.exists(dummy_data_file_path):
                ask_for_delete = input(
                    "Do you want to delete the dummy data file? (y/n)"
                )
                if ask_for_delete == "y":
                    os.remove(dummy_data_file_path)
                    print(f"File '{dummy_data_file_path}' deleted.")
                    break
                else:
                    print("Exiting...")
                    break
            break


""" Main function to run the application"""


def run():
    app.main()


""" Command Line Interface entry point"""


def cli_entry_point():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")
    parser_run = subparser.add_parser("run", help="Runs the application")
    perf_monitor = subparser.add_parser("monitor", help="Perf Monitor")

    args = parser.parse_args()

    if args.command == "monitor":
        monitor()
    elif args.command == "run":
        run()
    else:
        parser.print_help()
