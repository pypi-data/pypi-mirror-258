from datetime import datetime
import collections
from classes.exceptions import WrongInfoException, WrongDate, NoValue, NoPhones


def wrong_input_handling(function):
    def handling(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except WrongInfoException as err:
            return err
        except WrongDate as err:
            return err.args[0]
        except NoValue as err:
            return err.args[0]
        except NoPhones as err:
            return err.args[0]
        except AttributeError as err:
            return err.args[0]
        except KeyError as err:
            return err.args[0]
        except ValueError as err:
            return err.args[0]
        except TypeError as err:
            return err.args[0]
        except Exception as err:
            return err.args[0]

    return handling


def get_contact(book, name):
    try:
        contact = book.data[name]
        return contact
    except KeyError:
        raise KeyError(f"The contacts book doesn't have a contact named {name}")


def check_args(args, exc: Exception):
    if isinstance(exc, WrongInfoException):
        if len(args) == 1:
            raise WrongInfoException("Please provide both a name and a phone number.")

        elif len(args) < 1:
            raise WrongInfoException(
                "Neither name nor phone number provided. Please try again."
            )

    elif isinstance(exc, WrongDate):
        if len(args) == 1:
            raise WrongDate("Please provide both a name and a date.")

        elif len(args) < 1:
            raise WrongDate("Neither name nor date was provided. Please try again.")

    elif isinstance(exc, NoValue):
        if len(args) != 1:
            raise NoValue("Please provide a contact name.")

    elif isinstance(exc, ValueError):
        if len(args) == 2:
            raise ValueError("Please provide both old and new phone numbers.")

        elif len(args) < 2:
            raise ValueError(
                "Neither old nor new phone number provided. Please try again."
            )


def parser(user_input):
    if user_input == "":
        return None, None, "Please start with a valid command."

    command, *args = user_input.split()
    command = command.lower().strip()
    return command, *args, None


def get_birthdays_per_week(users: list[any]):
    bds_seven_days = collections.defaultdict(list)
    current_date = datetime.today().date()
    birthdays = []

    for user in users:
        if user.birthday:
            user_bd = user.birthday.birthday.date()
            bd_this_year = user_bd.replace(year=current_date.year)
        else:
            continue

        if bd_this_year < current_date:
            bd_this_year = bd_this_year.replace(year=current_date.year + 1)

        days_delta = (bd_this_year - current_date).days

        if days_delta < 7:
            day_to_congrats = bd_this_year.strftime("%A")

            ## if the function is run on Sunday and the BD is in 6 days
            if days_delta == 6 and day_to_congrats in ["Saturday", "Sunday"]:
                day_to_congrats = "Next Monday"
            elif day_to_congrats in ["Saturday", "Sunday"]:
                day_to_congrats = "Monday"

            bds_seven_days[day_to_congrats].append(user.name.name)

    if len(bds_seven_days) > 0:
        ## print out the list of names per day for the next seven days
        for day, names in bds_seven_days.items():
            birthdays.append("{:<15}{:<5}{}".format(day, ":", ", ".join(names)))
    else:
        birthdays.append("No birthdays next week.")

    ## in case the list is needed elsewhere
    return birthdays


## test the function
if __name__ == "__main__":
    test_date = datetime.today()

    users = [
        {
            "name": "Bill Gates",
            "birthday": test_date.replace(
                month=test_date.month - 1
            ),  ## BD this year last month
        },
        {
            "name": "Bill States",
            "birthday": test_date.replace(month=12),  ## BD this year end of year
        },
        {
            "name": "Bill Mates",
            "birthday": test_date.replace(day=test_date.day - 1),  ## BD yesterday
        },
        {
            "name": "Bill Rates",
            "birthday": test_date.replace(day=test_date.day + 1),  ## BD tomorrow
        },
        {"name": "Bill Wates", "birthday": test_date},  ## BD today
        {
            "name": "Bill Spades",
            "birthday": test_date.replace(
                day=test_date.day + 6
            ),  ## BD weekend; needs adjusting
        },
        {
            "name": "Bill Dates",
            "birthday": test_date.replace(day=test_date.day + 7),  ## BD in a week
        },
    ]
    print(users[0])
    get_birthdays_per_week(users)
