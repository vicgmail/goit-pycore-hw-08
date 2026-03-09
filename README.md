# Classes

## Structure

```
homework4/
├── main.py
├── modules/
│   ├── address_book/
│   │   └── models/
│   │       └── address_book_library.py
│   └── console_bot/
│       ├── command_parser.py
│       ├── console_bot.py
│       └── handlers.py
```

### Task

```bash
python3 -m modules.console_bot.console_bot
```

### Available commands:

add: [name] [phone] - Add a new contact
change: [name] [old_phone] [new_phone] - Change an existing contact
phone: [name] - Show a specific contact
all: Show all contacts
add-birthday: [name] [birthday] - Add for a specific contact
show-birthday: [name] - Show birthday for contact
birthdays: Show upcoming birthdays for a week
dump: Store address book in file
load: Load address book from file
help: Show available commands
close: Close the application
hello: Greet the user

## Required

- Python 3.9+

## Author

Vic Lymar
victorlymar@gmail.com
@MIT
