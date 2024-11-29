from functools import wraps


def input_error(func):
    @wraps(func)
    def inner(args, contacts):
        try:
            return func(args, contacts)
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Enter user name"
        except KeyError:
            return "Contact is not exists"
    
    return inner


def parse_input(user_input: str):
    cmd, *args = user_input.split(" ")
    cmd = cmd.strip().lower()
    return cmd, args


@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added"


@input_error
def change_contact(args, contacts):
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated"
    

@input_error
def show_phone(args, contacts):
    name = args[0]
    return contacts[name]
    

def show_all(args, contacts):
    return ";\n".join([f"{name}: {phone}" for name, phone in contacts.items()])


def main():
    contacts = {}
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
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(args, contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
