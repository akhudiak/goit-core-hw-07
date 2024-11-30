from functools import wraps
from data_structure import AddressBook, Record
from errors import PhoneFormatError, BirthdayFormatError, InputFormatError, NameError, PhoneError


def input_error(func):
    @wraps(func)
    def inner(args, book):
        try:
            return func(args, book)
        except (PhoneFormatError, BirthdayFormatError, InputFormatError, NameError, PhoneError) as error:
            return error
    
    return inner


def parse_input(user_input: str):
    cmd, *args = user_input.split(" ")
    cmd = cmd.strip().lower()
    return cmd, args


@input_error
def add_contact(args, book: AddressBook):
    try:
        name, phone = args
    except ValueError:
        raise InputFormatError("Use format 'add [name] [phone]'")
    
    record = book.find(name)

    if record:
        record.add_phone(phone)
        message = "Contact updated"
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        message = "Contact added"

    return message


@input_error
def change_phone(args, book: AddressBook):
    try:
        name, old_phone, new_phone = args
    except ValueError:
        raise InputFormatError("Use format 'change [name] [old phone] [new phone]'")
    
    record = book.find(name)
    if not record:
        raise NameError(name)
    
    record.edit_phone(old_phone, new_phone)
    return "Contact updated"
    

@input_error
def show_phone(args, book: AddressBook):
    try:
        name = args[0]
    except IndexError:
        raise InputFormatError("Use format 'phone [name]'")
    
    record = book.find(name)
    if not record:
        raise NameError(name)
    
    return str(record)


@input_error
def show_all(args, book):
    return str(book)


@input_error
def add_birthday(args, book: AddressBook):
    try:
        name, birthday = args
    except ValueError:
        raise InputFormatError("User format 'add-birthday [name] [birthday]'")
    
    record = book.find(name)
    if not record:
        raise NameError(name)
    
    record.add_birthday(birthday)
    
    return "Birthday added"


@input_error
def show_birthday(args, book: AddressBook):
    try:
        name = args[0]
    except IndexError:
        raise InputFormatError("Use format 'show-birthday [name]'")
    
    record = book.find(name)
    if not record:
        raise NameError(name)
    
    return record.birthday.value


@input_error
def birthdays(args, book: AddressBook):
    return "\n".join(f'{u_b["name"]}: {u_b["birthday"]}' for u_b in book.get_upcoming_birthdays(days=7))


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input(">>> ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_phone(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(args, book))
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
