# for rising custom errors in 'add_contact' function
import re
from collections import UserDict
from datetime import datetime
from typing import Union


class FieldException(Exception):
    pass


class Field:
    def __init__(self, value: str) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        self.__value = value


class Name(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value: str) -> None:
        if value.isalpha():
            Field.value.fset(self, value)
        else:
            raise ValueError("Name must be a single alphabetic string \n" +
                             "Example: 'Abc', 'abc'")

    def get_name(self) -> str:
        return self.value


class Phone(Field):
    def __init__(self, value: str = '') -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value: str) -> None:
        pattern = r'(?:\+\d{12,13}\b)|(?:\b(?<!\+)\d{10,11}\b)|(?:\b\d{2}(?!\W)\b)'
        if re.match(pattern, value):
            Field.value.fset(self, value)
        else:
            raise ValueError("Phone must be a single numeric string\n" +
                             "Example: '+[12-13 digits]' or '[10-11 digits]'\n" +
                             "Or for DEBUG: just '[2 digits]")

    def get_phone(self) -> str:
        return self.value


class Birthday(Field):
    def __init__(self, value: str = '') -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value: str) -> None:
        try:
            Field.value.fset(self, datetime.strptime(value, "%d.%m.%Y"))
        except ValueError:
            raise ValueError("Birthday must be a single date string in format dd.mm.yyyy\n" +
                             "Example: '01.01.1970'")

    def birthday_date(self) -> str:
        date = self.value.strftime("%d.%m.%Y")
        return date

    def get_month(self) -> str:
        return self.value.month

    def get_day(self) -> str:
        return self.value.day


class Record:
    def __init__(self, name: Name) -> None:
        self.name: Name = name
        self.phone_list: list[Phone] = []
        self.birthday: Union[Birthday, None] = None

    # return f"Name '{self.name}' is already in contacts!\n" \
    #        "Try another name or change existing contact"

    def add_phone(self, phone: Phone) -> str:
        if phone.get_phone() in [phone.get_phone() for phone in self.phone_list]:
            raise FieldException("This phone number is already in the list of the contact!")
        self.phone_list.append(phone)
        return "Contact was updated successfully!"

    def get_phones(self) -> str:  # return phones in one string
        if not self.phone_list:
            return '-'
        return ', '.join([phone.get_phone() for phone in self.phone_list])

    def remove_phone(self, phone: Phone) -> str:
        if phone.get_phone() not in [el.get_phone() for el in self.phone_list]:
            return "Phone can't be removed: it's not in the list of the contact!"
        for el in self.phone_list:
            if el.get_phone() == phone.get_phone():
                self.phone_list.remove(el)
        return "Phone was removed successfully!"

    def edit_phone(self, phone: Phone, new_phone: Phone) -> str:
        if phone.get_phone() not in [el.get_phone() for el in self.phone_list]:
            return "Phone can't be changed: it's not in the list of the contact!"
        for el in self.phone_list:
            if el.get_phone() == phone.get_phone():
                self.phone_list.remove(el)
                self.phone_list.append(new_phone)
                return f"Phone number was changed successfully!"

    def add_birthday(self, birthday: Birthday) -> None:
        if self.birthday is not None:
            raise FieldException("Birthday field of this contact is already filled!")
        self.birthday = birthday

    def get_birthday(self) -> str:
        if self.birthday is None:
            return '-'
        return self.birthday.birthday_date()

    def edit_birthday(self, new_birthday: Birthday) -> str:
        if self.birthday is None:
            return "Birthday field of this contact is empty: fill it!"
        self.birthday = new_birthday
        return f"Birthday was changed successfully!"


class AddressBook(UserDict):
    def __init__(self, pagination: int = 2) -> None:
        super().__init__()
        self.pagination = pagination
        self.current_index = 0
        self.current_page = 0  # for showing page number in terminal

    def add_record(self, name: str, record: Record) -> None:
        self.data[name] = record

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index >= len(self.data):
            self.current_index = 0
            self.current_page = 0
            raise StopIteration

        result = []

        page_end = f"\n{'--end--' : ^20}"  # at the end of the data
        for i in range(self.current_index, self.current_index + self.pagination):
            if i >= len(self.data):
                break
            name = list(self.data.keys())[i]
            result.append(f"{self.data.get(name).name.get_name()}:\t{self.data.get(name).get_phones()}" +
                          f"\t{self.data.get(name).get_birthday()}")
            self.current_index += 1
        else:
            if self.current_index < len(self.data):
                self.current_page += 1
                page_end = f"\n{'--' + str(self.current_page) + '--' : ^20}\n"  # at the end of each page

        result = '\n'.join(result) + page_end
        return result
