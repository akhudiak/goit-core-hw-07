class PhoneFormatError(Exception):
    def __init__(self, message):
        super().__init__(message)


class BirthdayFormatError(Exception):
    def __init__(self, message="Invalid date format. Use DD.MM.YYYY"):
        super().__init__(message)


class InputFormatError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NameError(Exception):
    def __init__(self, name):
        self.message = f"There is no contact with name: '{name}'"
        super().__init__(self.message)

    
class PhoneError(Exception):
    def __init__(self, name, phone):
        self.message = f"{name} doesn't have a phone number: '{phone}'"
        super().__init__(self.message)