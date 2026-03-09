from collections import UserDict
from datetime import datetime, timedelta
import re


DEFAULT_GREETING_PERIOD_DAYS = 7
DEFAULT_DATE_FORMAT = "%d.%m.%Y"


class PhoneException(Exception):
    pass


class RecordException(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        self.value = value


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise PhoneException(f"Phone number {value} must be a 10-digit string")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str | None):
        self.value = None
        if value is None:
            return
        if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", value):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        try:
            self.value = datetime.strptime(value, DEFAULT_DATE_FORMAT).date()
        except:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        if self.value:
            return f"birthday: {self.value.strftime(DEFAULT_DATE_FORMAT)}"
        return "";
        


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        if not self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        return f"Contact name: {self.name.value}, {self.birthday}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: str):
        if not any(p.value == phone for p in self.phones):
            self.phones.append(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str):
        for index, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[index] = Phone(new_phone)
                return
        raise PhoneException(f"Phone number {old_phone} not found")

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None
    
    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if not self.birthday or not self.birthday.value:
            return None
        return self.birthday.value.strftime(DEFAULT_DATE_FORMAT)


class AddressBook(UserDict):
    def add_record(self, record: Record):
        if not self.find(record.name.value):
            self.data[record.name.value] = record        
    
    def find(self, search: str):
        return self.data.get(search)
    
    def delete(self, name):
        if self.find(name):
            del self.data[name]
            return True
        return False

    def get_upcoming_birthdays(self) -> list[dict]:
        result = []
        current_year = datetime.now().year
        today = datetime.now().date()
        for user in self.data.values():
            if not user.birthday or not user.birthday.value:
                continue
            birthday = user.birthday.value
            upcoming_birthday = None
            try:
                upcoming_birthday = birthday.replace(year=current_year)
            except ValueError:
                upcoming_birthday = birthday.replace(year=current_year, day=28)
            upcoming_birthday_days = (upcoming_birthday - today).days
            if upcoming_birthday_days < 0:
                try:
                    upcoming_birthday = birthday.replace(year=current_year + 1)
                except ValueError:
                    upcoming_birthday = birthday.replace(year=current_year + 1, day=28)
                upcoming_birthday_days = (upcoming_birthday - today).days
            if 0 <= upcoming_birthday_days < DEFAULT_GREETING_PERIOD_DAYS:
                if upcoming_birthday.weekday() == 5: # Saturday
                    upcoming_birthday = upcoming_birthday + timedelta(days=2)
                elif upcoming_birthday.weekday() == 6: # Sunday
                    upcoming_birthday = upcoming_birthday + timedelta(days=1)
                result.append({
                    "name": user.name.value,
                    "birthday": user.birthday.value.strftime(DEFAULT_DATE_FORMAT),
                    "congratulation_date": upcoming_birthday.strftime(DEFAULT_DATE_FORMAT)
                })
        result.sort(key=lambda x: x["congratulation_date"])
        return result
