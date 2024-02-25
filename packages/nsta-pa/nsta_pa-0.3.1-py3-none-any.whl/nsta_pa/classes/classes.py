from collections import UserDict
import re
import pickle
from datetime import datetime
from utils.utils import get_birthdays_per_week
from .exceptions import WrongDate, NoValue


class Field:
    def __init__(self, item):
        self.item = item

    def __str__(self):
        return str(self.item)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)
        self.name = name


class Phone(Field):
    def __init__(self, phone: str):
        super().__init__(phone)
        self.phone = re.match("^[0-9]{10}$", phone).group(0)


class Birthday(Field):
    def __init__(self, birthday: str):
        super().__init__(birthday)
        try:
            checked_birthday = re.match(
                "^[0-3]{1}[0-9]{1}\.[0-1]{1}[0-9]{1}\.[0-9]{4}$", birthday
            ).group(0)
        except AttributeError:
            raise WrongDate("The date must be of the DD.MM.YYYY format. Try again.")
        self.birthday = datetime.strptime(checked_birthday, "%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.item}, phones: {'; '.join(p.item for p in self.phones)}"

    def list_str_rep(self, lst: list):
        return [str(i) for i in lst]

    def error_handler(function):
        def handle(self, *args, **kwargs):
            try:
                return function(self, *args, **kwargs)
            except IndexError:
                raise IndexError(
                    "This phone number is not associated with this contact."
                )

            except NoValue as err:
                raise NoValue from err

            except TypeError:
                raise TypeError("The phone number(s) not provided. Try again.")

            except AttributeError:
                raise AttributeError(
                    "The phone number must be 10 digits long "
                    + "and contain only digits."
                )

            except WrongDate as err:
                raise WrongDate from err

            except ValueError:
                raise ValueError(
                    f"{args[0]} is not on the list of {self.name}'s phone numbers."
                )

            except:
                raise Exception("Something went wrong. Please try again.")

        return handle

    @error_handler
    def add_phone(self, phone=None):
        if not phone:
            raise NoValue("No phone number was provided.")
        phone_num = Phone(phone)
        self.phones.append(phone_num)

    @error_handler
    def edit_phone(self, old_phone, new_phone):
        old_phone_index = self.list_str_rep(self.phones).index(old_phone)
        self.phones[old_phone_index] = Phone(new_phone)

    @error_handler
    def find_phone(self, phone=None):
        if not phone:
            raise NoValue("No phone number was provided.")
        found_phone_index = self.list_str_rep(self.phones).index(phone)
        found_phone = self.phones[found_phone_index]
        return found_phone

    ## never used -_-
    @error_handler
    def remove_phone(self, phone=None):
        if not phone:
            raise NoValue("No phone number was provided.")
        found_phone_index = self.list_str_rep(self.phones).index(phone)
        self.phones.pop(found_phone_index)

    def add_birthday(self, birthday=None):
        if not birthday:
            raise NoValue("No birthday date was provided.")
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):

    def __init__(self):
        self.data = {}
        self.records = 0

    def error_handler(function):
        def handle(self, *args, **kwargs):
            try:
                return function(self, *args, **kwargs)
            except KeyError:
                raise KeyError(
                    f"The contacts book doesn't have a contact named {args[0]}"
                )
            except NoValue as err:
                raise NoValue from err
            except TypeError:
                raise TypeError("Record details not provided.")
            except:
                raise Exception("Something went wrong.")

        return handle

    @error_handler
    def add_record(self, record):
        self.data.update({str(record.name): record})
        self.records += 1

    @error_handler
    def find(self, name=None):
        if not name:
            raise NoValue("The name of a contact not provided.")
        return self.data[name]

    @error_handler
    def delete(self, name=None):
        if not name:
            raise NoValue("The name of a contact not provided.")
        self.data.pop(name)
        self.records -= 1

    @error_handler
    def birthdays_per_week(self):
        users = [user for user in self.data.values()]
        birthdays = get_birthdays_per_week(users)
        return birthdays

    def write_to_file(self, book_path):
        with open(book_path.joinpath("book.bin"), "wb") as file:
            pickle.dump(self, file)

    def read_from_file(self, book_path):
        with open(book_path.joinpath("book.bin"), "rb") as file:
            book = pickle.load(file)
            return book
