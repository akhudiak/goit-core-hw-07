from collections import UserDict
from errors import PhoneFormatError


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



class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones: list[Phone] = []
    
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
            raise ValueError
        
        index = self.phones.index(phone)
        self.phones[index] = Phone(new_phone)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def delete(self, name: str):
        del self.data[name]

    def find(self, name: str):
        return self.data.get(name)

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
    

def main():
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    print(book)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")


if __name__ == "__main__":
    main()