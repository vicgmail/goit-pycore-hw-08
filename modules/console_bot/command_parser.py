from colorama import Fore # type: ignore
from . import handlers


AVAILABLE_COMMANDS = {
    "add": "[name] [phone] - Add a new contact", 
    "change": "[name] [old_phone] [new_phone] - Change an existing contact",
    "delete": "[name] - Delete a contact",
    "phone": "[name] - Show a specific contact",
    "all": "Show all contacts",
    "add-birthday": "[name] [birthday] - Add for a specific contact",
    "show-birthday": "[name] - Show birthday for contact",
    "birthdays": "Show upcoming birthdays for a week",
    "dump": "Store address book in file",
    "load": "Load address book from file",
    "help": "Show available commands",
    "close": "Close the application",
    "hello": "Greet the user"
}
ADDRESS_BOOK_AUTOLOAD = True
ADDRESS_BOOK_AUTOSAVE = True


def bot_init():
    handlers.init()
    if (ADDRESS_BOOK_AUTOLOAD):
        handlers.load()


def bot_exit():
    if (ADDRESS_BOOK_AUTOSAVE):
        handlers.dump()


# Parse entered commands and execute corresponding actions
def command_parser(input_command: str) -> None:
    if not input_command.strip():
        return

    command_parts = input_command.split()
    command = command_parts[0].lower()
    args = command_parts[1:] if len(command_parts) > 1 else []

    if command not in AVAILABLE_COMMANDS:
        print(f"Invalid command: {Fore.RED}{command}{Fore.RESET}. Type 'help' for available commands.")
        return
    
    if command == "add":
        handlers.add_contact(args)
    elif command == "change":
        handlers.change_contact(args)
    elif command == "delete":
        handlers.delete_contact(args)
    elif command == "all":
        handlers.show_all_contacts()
    elif command == "phone":
        handlers.show_contact(args)
    elif command == "add-birthday":
        handlers.add_birthday(args)
    elif command == "show-birthday":
        handlers.show_birthday(args)
    elif command == "birthdays" or command == "b":
        handlers.birthdays()
    elif command == "dump":
        handlers.dump()
    elif command == "load":
        handlers.load()
    elif command == "hello":
        handlers.hello()
    elif command == "help":
        print("Available commands:")
        for c, d in AVAILABLE_COMMANDS.items():
            print(f"  {Fore.GREEN}{c}{Fore.RESET}: {d}")
    
    return True
