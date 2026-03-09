# Handler functions for each command
from colorama import Fore # type: ignore
from functools import wraps
import pickle
import os
from ..address_book.models.address_book_library import AddressBook, Record


ADDRESS_BOOK_FILE = "addressbook.pkl"
ADDRESS_BOOK_AUTOLOAD = True
ADDRESS_BOOK_AUTOSAVE = True
book = None


def init():
    global book
    book = AddressBook()


# Decorator to handle input errors for command functions
def input_error(func):
    @wraps(func)
    def inner(*args):
        try:
            if func.__name__ in ["add_contact", "change_contact"] and len(args[0]) < 2:
                raise ValueError()

            if len(args[0]) < 1:
                raise Exception('Format error')

            return func(*args)

        except ValueError:
            print(f"{Fore.RED}Please enter input params properly.{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Fore.RESET} ")
    return inner


def hello():
    print("How can I help you?")


def show_all_contacts():
    for name, record in book.data.items():
        print(f"{record}")


def dump():
    try:
        with open(ADDRESS_BOOK_FILE, "wb") as file:
            pickle.dump(book, file)
        print(f"{Fore.GREEN}Address book was saved to {ADDRESS_BOOK_FILE}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Error saving address book: {e}{Fore.RESET}")


def load():
    global book
    try:
        if not os.path.exists(ADDRESS_BOOK_FILE):
            print(f"{Fore.YELLOW}Address book was not found at {ADDRESS_BOOK_FILE}{Fore.RESET}")
            return
        with open(ADDRESS_BOOK_FILE, "rb") as file:
            book = pickle.load(file)
        print(f"{Fore.GREEN}Address book loaded from {ADDRESS_BOOK_FILE}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Error loading address book: {e}{Fore.RESET}")


@input_error
def add_contact(args):
    name = " ".join(args[:len(args)-1])
    phone = args[len(args)-1]
    record = book.find(name)
    if not record:
        record = Record(name)    
        record.add_phone(phone)
        book.add_record(record)
    else:
        record.add_phone(phone)
    print(f"Added contact {Fore.GREEN}{name}{Fore.RESET} with phone: {Fore.GREEN}{phone}{Fore.RESET}")


@input_error
def change_contact(args):
    name = " ".join(args[:len(args)-2])
    old_phone = args[len(args)-2]
    new_phone = args[len(args)-1]
    record = book.find(name)
    if not record:
        print(f"Contact not found: {Fore.RED}{name}{Fore.RESET}")
        return;
    if record.edit_phone(old_phone, new_phone):
        print(f"Changed contact {Fore.GREEN}{name}{Fore.RESET} to phone: {Fore.GREEN}{phone}{Fore.RESET}")


@input_error
def delete_contact(args):
    if not args:
        print("Usage: delete_contact <name>")
        return
    name = " ".join(args)
    deleted = book.delete(name)
    if not deleted:
        print(f"Contact not found: {Fore.RED}{name}{Fore.RESET}")
        return;
    print(f"Deleted contact: {Fore.GREEN}{name}{Fore.RESET}")


@input_error
def show_contact(args):
    if not args:
        print("Usage: phone [name]")
        return
    name = " ".join(args)
    record = book.find(name)
    if not record:
        print(f"Contact not found: {Fore.RED}{name}{Fore.RESET}")
    else:
        print(f"{record}")


@input_error
def add_birthday(args):
    name = " ".join(args[:len(args)-1])
    birthday = args[len(args)-1]
    record = book.find(name)
    if not record:
        print(f"Contact not found: {Fore.RED}{name}{Fore.RESET}")
        return
    record.add_birthday(birthday)
    print(f"Added contact birthday {Fore.GREEN}{name} {birthday}{Fore.RESET}")


@input_error
def show_birthday(args):
    name = " ".join(args)
    record = book.find(name)
    if not record:
        print(f"Contact not found: {Fore.RED}{name}{Fore.RESET}")
        return
    print(f"Contact {record.name} {record.birthday}")


def birthdays():
    list = book.get_upcoming_birthdays()
    for r in list:
        print(f"Contact {Fore.GREEN}{r['name']}{Fore.RESET} with birthday {r['birthday']} will selebrate {Fore.GREEN}{r['congratulation_date']}{Fore.RESET}")
