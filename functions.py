from datetime import datetime
from classes import AddressBook, Phone, Birthday, Name, Record, FieldException


# This decorator handles the correct number of arguments that are passed into the function
def func_arg_error(func):
    def wrapper(*args):
        try:
            result = func(*args)
            return result
        except TypeError:
            f_name = func.__name__
            if f_name in ('exit_program', 'hello', 'show_all_phones'):
                return "ERROR: This command has to be written without arguments!"
            if f_name in ('show_phone', 'days_to_birthday', 'find_contacts'):
                return "ERROR: This command needs 1 arguments: "\
                        f"'{'search_word' if f_name == 'find_contacts' else 'name'}' separated by 1 space! "
            if f_name in ('add_contact',):
                return "ERROR: This command needs 1 obligatory argument 'name' and 2 supplementary " \
                       "'phone' and 'birthday' separated by 1 space!"
            if f_name in ('edit_birthday',):
                return "ERROR: This command needs 2 arguments: 'name' and 'birthday' separated by 1 space!"
            if f_name in ('remove_phone',):
                return "ERROR: This command needs 2 arguments: 'name' and 'phone' separated by 1 space!"
            if f_name in ('edit_phone',):
                return "ERROR: This command needs 3 arguments: 'name', 'phone' and 'new_phone' separated by 1 space!"
            return "Some unhandled error occurred!"

    return wrapper


@func_arg_error
def hello() -> str:
    return "Hello! How can I help you?"


@func_arg_error
def add_contact(contacts: AddressBook, name: str, phone: str = '', birthday: str = '') -> str:
    try:
        n = Name(name)
        p = Phone(phone) if phone else None
        b = Birthday(birthday) if birthday else None
    except ValueError as err:
        return f"ERROR: {err}"

    if name in contacts.data.keys():
        if not phone and not birthday:
            return "ERROR: The contact with this name is already created! Try to update it!"
        if phone:
            try:
                contacts.data[name].add_phone(p)
            except FieldException as msg:
                return str(msg)
        if birthday:
            try:
                contacts.data[name].add_birthday(b)
            except FieldException as msg:
                return str(msg)
        return "Contact was updated successfully!"
    else:
        contact_record = Record(n)
        if phone:
            contact_record.add_phone(p)
        if birthday:
            contact_record.add_birthday(b)
        contacts.add_record(name, contact_record)
        return f"Contact was created successfully!"


@func_arg_error
def edit_phone(contacts: AddressBook, name: str, phone: str, new_phone: str) -> str:
    if name not in contacts.data.keys():
        return f"There is no contact with name '{name}'"

    try:
        p = Phone(phone)
        new_p = Phone(new_phone)
    except ValueError as err:
        return f"ERROR: {err}"

    result = contacts.data.get(name).edit_phone(p, new_p)
    return result


@func_arg_error
def edit_birthday(contacts: AddressBook, name: str, new_birthday: str) -> str:
    if name not in contacts.data.keys():
        return f"There is no contact with name '{name}'"

    try:
        b = Birthday(new_birthday)
    except ValueError as err:
        return f"ERROR: {err}"

    result = contacts.data.get(name).edit_birthday(b)
    return result


@func_arg_error
def remove_phone(contacts: AddressBook, name: str, phone: str) -> str:
    """
    Remove phone number from the contact. But doesn't remove contact itself if it has no phone numbers.
    """
    if name not in contacts.data.keys():
        return f"There is no contact with name '{name}'"

    try:
        p = Phone(phone)
    except ValueError as err:
        return f"ERROR: {err}"
    result = contacts.data.get(name).remove_phone(p)
    return result


@func_arg_error
def show_phone(contacts: AddressBook, name: str) -> str:
    if name not in contacts.data.keys():
        return f"There is no contact with name '{name}'"

    return contacts.get(name).get_phones()


@func_arg_error
def show_all_phones(contacts: AddressBook) -> str:
    if not contacts.data:
        return "There are no contacts to show yet..."
    result = ''
    for page in contacts:
        result += page
    return result


@func_arg_error
def days_to_birthday(contacts: AddressBook, name: str) -> str:
    if name not in contacts.data.keys():
        return f"There is no contact with name '{name}'"

    if contacts[name].birthday is None:
        return "This contact has no birthday field!"
    now = datetime.now()
    birthday = datetime(now.year, contacts[name].birthday.get_month(), contacts[name].birthday.get_day())
    if birthday < now:
        birthday = birthday.replace(year=now.year + 1)
    days = (birthday - now).days + 1
    return f"{days} day(s) to {contacts[name].name.get_name()}'s birthday!"


@func_arg_error
def exit_program():
    return "Good bye!"


@func_arg_error
def save_contacts(contacts: AddressBook, filename: str = 'database/contacts_db') -> str:
    result = contacts.save_to(filename)
    return result


@func_arg_error
def load_contacts(contacts: AddressBook, filename: str = 'database/contacts_db') -> str:
    data, result = contacts.load_from(filename)
    if not (data is None):
        contacts.data = data
    return result


@func_arg_error
def find_contacts(contacts: AddressBook, search_string: str) -> str:
    result = contacts.find(search_string)
    return result
