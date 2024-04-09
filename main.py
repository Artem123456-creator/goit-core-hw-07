from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not isinstance(value, str) or not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            date_format = "%d.%m.%Y"
            datetime.strptime(value, date_format)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        if not isinstance(phone_number, str) or not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Invalid phone number format")
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_phone_number, new_phone_number):
        if not isinstance(new_phone_number, str) or not new_phone_number.isdigit() or len(new_phone_number) != 10:
            raise ValueError("Invalid new phone number format")
    
        found = False
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                found = True
                break
        else:
            raise ValueError(f"Phone number {old_phone_number} not found in the record")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming_week = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                if record.birthday.value.month == today.month and \
                        today.day <= record.birthday.value.day <= upcoming_week.day:
                    upcoming_birthdays.append(record)

        return upcoming_birthdays

def add_birthday(args, book):
    name, birthday_str = args
    record = book.find(name)
    if record:
        record.birthday = Birthday(birthday_str)
        return f"Birthday added for {name}"
    else:
        return f"Contact {name} not found"

def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday.value}"
    else:
        return f"Birthday not found for {name}"

def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join([f"{record.name.value}'s birthday: {record.birthday.value}" for record in upcoming_birthdays])
    else:
        return "No upcoming birthdays"

def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

def change_contact(args, book):
    name, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(record.phones[0].value, new_phone)
        return f"Phone number updated for {name}"
    else:
        return f"Contact {name} not found"

def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.phones:
        return f"Phone number for {name}: {record.phones[0].value}"
    else:
        return f"Phone number not found for {name}"

def show_all_contacts(book):
    if book.data:
        return "\n".join([f"{record.name.value}: {', '.join([str(phone) for phone in record.phones])}" for record in book.data.values()])
    else:
        return "No contacts found"

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
