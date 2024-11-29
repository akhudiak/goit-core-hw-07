class PhoneFormatError(Exception):
    def __init__(self, message):
        super().__init__(message)


class BirthdayFormatError(Exception):
    def __init__(self, message="Invalid date format. Use DD.MM.YYYY"):
        super().__init__(message)