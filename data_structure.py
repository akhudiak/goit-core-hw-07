from collections import UserDict
from datetime import datetime, date, timedelta
from enum import Enum
from errors import PhoneFormatError, BirthdayFormatError, PhoneError


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self.__check_format(value)
        super().__init__(value)

    def __check_format(self, value: str):

        if len(value) != 10:
            raise PhoneFormatError("The phone number must be 10 digits long")
        
        if not value.isdigit():
            raise PhoneFormatError("The phone number must contain only digits")


class Birthday(Field):
    def __init__(self, value):
        self.__check_format(value)
        super().__init__(value)

    def __check_format(self, value: str):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise BirthdayFormatError()


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday = None
    
    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
            
    def remove_phone(self, phone: str):
        phone = self.find_phone(phone)
        self.phones.remove(phone)
            
    def edit_phone(self, old_phone: str, new_phone: str):
        
        phone = self.find_phone(old_phone)
        if not phone:
            raise PhoneError(self.name.value, old_phone)
        
        index = self.phones.index(phone)
        self.phones[index] = Phone(new_phone)

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class Day(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def delete(self, name: str):
        del self.data[name]

    def find(self, name: str) -> Record:
        return self.data.get(name)
    
    @staticmethod
    def date_to_string(date: date):
        return date.strftime("%d.%m.%Y")
    
    @staticmethod
    def find_next_weekday(start_date: date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    @staticmethod
    def adjust_for_weekend(birthday: date):
        if birthday.weekday() >= Day.SATURDAY.value:
            return AddressBook.find_next_weekday(birthday, Day.MONDAY.value)
        return birthday
    
    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()

        for contact in self.data.values():

            if not contact.birthday:
                continue
            
            birthday = datetime.strptime(contact.birthday.value, "%d.%m.%Y").date()

            next_birthday = birthday.replace(year=today.year)

            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year+1)

            if 0 <= (next_birthday - today).days <= days:

                next_birthday = self.adjust_for_weekend(next_birthday)

                congratulation_date_str = self.date_to_string(next_birthday)
                upcoming_birthdays.append({"name": contact.name.value, "birthday": congratulation_date_str})

        return upcoming_birthdays

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
    

def main():
    address_book = AddressBook()

    # Додаємо контакти з днями народження
    record1 = Record("Alice")
    record1.add_birthday("30.11.2003")
    address_book.add_record(record1)

    record2 = Record("Bob")
    record2.add_birthday("03.12.1995")
    address_book.add_record(record2)

    record3 = Record("Charlie")
    record3.add_birthday("08.12.2000")
    address_book.add_record(record3)

    record4 = Record("Diana")
    record4.add_birthday("29.11.1990")
    address_book.add_record(record4)

    record5 = Record("Eve")
    record5.add_birthday("07.12.1988")
    address_book.add_record(record5)

    
    # Викликаємо метод з параметром 7 днів
    upcoming_birthdays = "\n".join(f'{birthday["name"]}: {birthday["birthday"]}' for birthday in address_book.get_upcoming_birthdays(days=7))
    print(upcoming_birthdays)

if __name__ == "__main__":
    main()