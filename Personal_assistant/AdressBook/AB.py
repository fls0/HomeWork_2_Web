from abc import ABC, abstractmethod
from collections import UserDict
from datetime import datetime, timedelta
from prompt_toolkit import prompt
from AdressBook.prompt_tool import Completer, RainbowLetter

import os
import dill as pickle
import re


class Field(ABC):
    def __init__(self, some_value):
        self._value = None
        self.value = some_value 

    @property
    @abstractmethod
    def value(self):
        return self._value
    
    @value.setter
    @abstractmethod
    def value(self, value):
        self._value = value

    def __str__(self):
        return f'{self.value}'


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        for i in value:
            if i.isdigit() or i in '+()':
                continue
            else:
                raise TypeError
        self._value = value


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = self.valid_date(value)

    def valid_date(self, value: str):
        try:
            # obj_datetime = parse(value)
            obj_datetime = datetime.strptime(value, '%Y-%m-%d')
            return obj_datetime.date()
        except KeyError:
            raise TypeError('Wrong data type. Try "yyyy-mm-dd"')


class Email(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: str):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex, value):
            self._value = value
        else:
            raise TypeError(f'Wrong email')


class Adress(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value


class Record:
    def __init__(self, name: Name, phone: Phone, birthday: Birthday, email: Email, adress=None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
            self.phone = phone
        self.birthday = birthday
        self.email = email
        if adress:
            self.adress = adress


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def update_record(self, record: Record):
        self.data[record.name.value] = record

    def delete_record(self, name):
        self.data.pop(name)

    def find_record(self, name):
        return self.data.get(name)

    def load(self):
        with open('AdressBook.bin', 'rb') as file:
            self.data = pickle.load(file)

contact_list = AddressBook()

class Saver(ABC):
    @abstractmethod
    def save():
        pass

class PickleSaver(Saver):
    def save(self, ab):
        with open('AdressBook.bin', 'wb') as file:
            pickle.dump(ab, file)

# class Loader(ABC):
#     @abstractmethod
#     def load():
#         pass

# class PickleLoader(Loader):
#     def __init__(self, ab: AddressBook):
#         self.ab = ab
#     def load(self):
#         with open('AdressBook.bin', 'rb') as file:
#             self.ab = pickle.load(file)



def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "ValueError. Try again"
        except IndexError:
            return "IndexError. Try again"
        except NameError:
            return "Invalid input. Name should contain only letters."
        except TypeError:
            return "Invalid input. Try again"
    return wrapper


class Display(ABC):
    @abstractmethod
    def show(self):
        pass


class ShowAll(Display):
    def __init__(self, data: AddressBook):
        self.data = data

    def show(self):
        if not self.data:
            return "Список контактів пустий."
        result = "Contacts:"
        print(result)
        print('------------------------------------------------------------------------------------------------------------------')
        print('Name          |     Number     |     Birthday     |            Email             |             Adress            |')
        for name, value in contact_list.items():
            print('--------------|----------------|------------------|------------------------------|-------------------------------|')
            print('{:<14}|{:^16}|{:^18}|{:^30}|{:^30} |'.format(name, value.phone.value, str(
                value.birthday.value), value.email.value, value.adress.value))
        print('------------------------------------------------------------------------------------------------------------------')


class ShowSearched(Display):
    def __init__(self, input_str: str):
        self.input_str = input_str

    @input_error
    def show(self):
        _, name = self.input_str.split()
        result = contact_list.find_record(name.title())
        return result.name.value, result.phone.value, str(result.birthday.value), result.email.value, result.adress.value


@input_error
def command_add():
    name = Name(input("Введіть ім'я: ").title())
    phone = Phone(input('Введіть номер: '))
    birthday = Birthday(input('Введіть дату народження: '))
    email = Email(input('Введіть email-пошту: '))
    adress = Adress(input('Введіть адрессу: '))
    contacts = Record(name, phone, birthday, email, adress)
    contact_list.add_record(contacts)
    return f"Contact {name} has been added."


@input_error
def command_delete(input_str):
    _, name = input_str.split()
    contact_list.delete_record(name.title())
    return f'Contact {name.title()} succefully deleted'


@input_error
def command_change():
    name = Name(input("Введіть ім'я: ").title())
    phone = Phone(input('Введіть номер: '))
    birthday = Birthday(input('Введіть дату народження: '))
    email = Email(input('Введіть email-пошту: '))
    adress = Adress(input('Введіть адрессу: '))
    update = Record(name, phone, birthday, email, adress)
    contact_list.update_record(update)
    return f"Contact {name} has been updated."


@input_error
def command_days_to_birthday(input_str):
    result = ''
    _, days = input_str.split()
    d_now = datetime.now().date()
    for key, value in contact_list.items():
        birthday = value.birthday.value
        birthday = birthday.replace(year=d_now.year)
        days_to_br = timedelta(days=int(days))
        days_to_br = d_now + days_to_br
        if d_now <= birthday <= days_to_br:
            result += f'{key} have birthday in next {days} days. {value.birthday}\n'
        else:
            continue
    return result.strip() if result else f'No birthdays in next {days} days'


def main():
    saver = PickleSaver()
    if os.path.exists('AdressBook.bin'):
        contact_list.load()
    print("Доступні команди:'hello','add','change', 'delete', 'search', 'birthday', 'show all','good bye','close','exit'")
    while True:
        input_str = prompt("Enter your command: ", completer=Completer, lexer=RainbowLetter())

        if input_str == "hello":
            print("How can I help you?")
        elif input_str.startswith("add"):
            print(command_add())
        elif input_str.startswith("change"):
            print(command_change())
        elif input_str.startswith("delete "):
            print(command_delete(input_str))
        elif input_str.startswith("search "):
            show_search = ShowSearched(input_str)
            print(show_search.show())
        elif input_str.startswith("birthday "):
            print(command_days_to_birthday(input_str))
        elif input_str == "show all":
            show_all = ShowAll(contact_list)
            show_all.show()
        elif input_str in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Невірно введена команда. Доступні команди:'hello','add','change','phone','show all','good bye','close','exit'")
        saver.save(contact_list)


if __name__ == "__main__":
    main()
