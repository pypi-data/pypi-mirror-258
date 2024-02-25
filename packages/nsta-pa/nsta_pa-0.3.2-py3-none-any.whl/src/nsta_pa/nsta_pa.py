from utils.handler import (
    add_contact,
    show_all,
    change_contact,
    show_phone,
    add_bd,
    show_birthday,
    birthdays_next_week,
    remove_number,
    del_contact,
    num_records,
    greeting,
)
from utils.utils import parser
from classes.classes import AddressBook

import pathlib
import os

filepath = pathlib.Path(__file__).parents[-1]
add_book_loc = filepath.joinpath("AddressBook")
try:
    os.makedirs(add_book_loc)
except Exception:
    pass


def main():

    try:
        book = AddressBook().read_from_file(add_book_loc)
    except:
        book = AddressBook()

    print("Welcome to the assistant bot!")
    while True:

        user_input = input("How can I help you?\nEnter a command: ")
        command, *args, message = parser(user_input)
        if message:
            print(message)

        if command in ["exit", "close"]:
            print("Good bye!")
            book.write_to_file(add_book_loc)
            break

        elif command in ["hello", "hi", "greetings"]:
            print(greeting(), end=" ")

        elif command == "add":
            print(add_contact(book, args))

        elif command == "all":
            [print(c) for c in show_all(book)]

        elif command == "phone":
            print(show_phone(book, args))

        elif command == "change":
            print(change_contact(book, args))

        elif command == "remove-phone":
            print(remove_number(book, args))

        elif command == "add-birthday":
            print(add_bd(book, args))

        elif command == "show-birthday":
            print(show_birthday(book, args))

        elif command == "birthdays":
            [print(bd) for bd in birthdays_next_week(book)]

        elif command in ["delete", "remove"]:
            print(del_contact(book, args))

        elif command == "entries":
            print(num_records(book))
        elif not command:
            pass

        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
