from classes import AddressBook
from command_handling import handle_cmd
import functions as f


def main():
    # create address book (UserDict)
    contacts = AddressBook()  # AddressBook(pagination_size)

    while True:
        command = None
        # Check if command is not empty
        while not command:
            command = input('Enter command: ')

        func, result = handle_cmd(command, contacts)
        print(result)

        if func == f.exit_program:
            break
        print()


if __name__ == '__main__':
    main()
