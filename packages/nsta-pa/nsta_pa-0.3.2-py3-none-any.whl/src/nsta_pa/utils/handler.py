import random
from classes.classes import (
    AddressBook,
    Record,
)
from classes.exceptions import WrongInfoException, WrongDate, NoValue
from .utils import check_args, wrong_input_handling, get_contact


def greeting():
    ## select and play a greeting reaction
    prompt = random.choice(["Hello!", "Hi!", "Greetings!"])
    return prompt


@wrong_input_handling
def add_contact(book: AddressBook, args):
    check_args(args, WrongInfoException())

    name = args[0]
    phone = args[-1]
    confirm = None

    if name in list(book.data.keys()):

        book_entry = book.data[name]
        try:
            if book_entry.find_phone(phone):
                return "This phone number is already associated with this contact."
        except:
            pass

        confirm = input("A contact with this name found. Update it? yes / no: ")
        confirm.lower()
        if confirm in ["yes", "1", "affirmative", "y"]:
            book_entry.add_phone(args[-1])
        else:
            return "Canelling contact addition."

    else:
        contact = Record(name)
        contact.add_phone(args[-1])
        book.add_record(contact)

    return "Contact added."


@wrong_input_handling
def change_contact(book: AddressBook, args):
    check_args(args, ValueError())

    contact = get_contact(book, args[0])
    contact.edit_phone(args[1], args[-1])
    return "Contact updated."


@wrong_input_handling
def show_phone(book, args):
    contact = get_contact(book, args[0])
    found_phones = contact.list_str_rep(contact.phones)
    found_phones = "; ".join(found_phones)
    return f"{args[0]}'s phone numbers: {found_phones}"


@wrong_input_handling
def show_all(book):
    names = list(book.keys())
    add_phone_message = 'Enter "add <name> <number>" to add a contact.'
    if not names:
        yield "No contacts found. " + add_phone_message

    for i in range(len(book.keys())):
        contact = get_contact(book, names[i])
        found_phones = contact.list_str_rep(contact.phones)

        if not found_phones:
            yield "{:>2}. | {:^20}\n".format(i + 1, names[i]) + add_phone_message
            continue

        message = "{:>2}. | {:^20} | {:>10}".format(i + 1, names[i], found_phones[0])

        if len(found_phones) > 1:
            formatted_phones = "".join(
                ["\n{:>39}".format(phone) for phone in found_phones[1:]]
            )
            yield message + formatted_phones
        elif len(found_phones) == 1:
            yield message


@wrong_input_handling
def add_bd(book, args):
    check_args(args, WrongDate())
    contact = get_contact(book, args[0])
    contact.add_birthday(args[1])
    return "Birthday date added."


@wrong_input_handling
def show_birthday(book, args):
    check_args(args, NoValue())
    contact = get_contact(book, args[0])
    bd = contact.birthday
    if bd:
        bd = str(bd)
        return f"{args[0]}'s birthday: {bd}"
    return "No associated birthday date found."


@wrong_input_handling
def birthdays_next_week(book):
    return book.birthdays_per_week()


@wrong_input_handling
def remove_number(book, args):
    check_args(args, WrongInfoException())
    contact = get_contact(book, args[0])
    contact.remove_phone(args[-1])
    return f"The number was deleted from {args[0]}'s list of phone numbers."


@wrong_input_handling
def del_contact(book, args):
    check_args(args, NoValue())
    book.delete(args[0])
    return "The contact was deleted."


@wrong_input_handling
def num_records(book):
    message = f"The address book has {book.records} entries. "
    if not book.records:
        return message + 'Enter "add <name> <number>" to add a contact.'
    else:
        return message + 'Type "all" to list all of them.'
