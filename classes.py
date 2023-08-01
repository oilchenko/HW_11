from collections import UserDict
import re
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)


class Name(Field):
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value_to_check):
        if len(value_to_check) <= 20:
            self._value = value_to_check
        else:
            print("Будь ласка, вкажіть ім'я коротше 20 знаків")
            raise ValueError


class Phone(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value_to_check):
        regex = "^[0-9\+\-\(\)]+$"
        result = re.fullmatch(regex, value_to_check)
        if result:
            if len(value_to_check) <= 40:
                self.__value = value_to_check
            else:
                print('Помилка у номері. Номер має не має бути довший 40 символів')
                raise ValueError
        else:
            print('Помилка у номері. Номер має складатися з цифр, знаків "+", "-", "(" та ")"')
            raise ValueError


class Birthday:
    def __init__(self, value):
        self._value = None
        self.value = value
    
    @property
    def value(self):
        return self._value
        
    @value.setter
    def value(self, value):
        try:
            self._value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            print('День народження вказаний у неправильному форматі. Будь ласка, вкажіть у форматі ДД.ММ.РРРР')
            # raise BirthdayError()
            raise ValueError
    
    def __str__(self):
        return self._value.strftime("%d.%m.%Y")
    
    def __repr__(self):
        return self._value.strftime("%d.%m.%Y")


class Record:
    def __init__(self,
                 name: Name,
                 phone: Phone = None,
                 birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone: Phone):
        ph_count = 0
        for phone_number in self.phones:
            if phone_number.value == phone.value:
                ph_count += 1
        if not ph_count:
            self.phones.append(phone)
            return f'Я додав номер {phone.value} до списку контактів у {self.name}'
        return f'Номер {phone.value} вже є у списку контактів у {self.name}'
    
    def change_phone(self, old_phone: Phone, new_phone: Phone):
        ph_count = 0
        for phone_number in self.phones:
            if phone_number.value == new_phone.value:
                ph_count += 1
        if ph_count:
            return f'Номер {new_phone.value}, який ти хочеш додати замість {old_phone.value}, вже є у списку контактів у {self.name}'
        for phone_number in self.phones:
            if phone_number.value == old_phone.value:
                phone_number.value = new_phone.value
                return f'Я замінив номер {old_phone.value} на {new_phone.value} у списку контактів у {self.name}'
        return f'Я не знайшов номер {old_phone.value} у списку контактів у {self.name}'

    def del_phone(self, phone: Phone):
        ph_count = 0
        for phone_number in self.phones:
            if phone_number.value == phone.value:
                ph_count += 1
        if ph_count:
            for i in range(len(self.phones)):
                if self.phones[i].value == phone.value:
                    self.phones.pop(i)
                    return f'Я видалив номер {phone} у {self.name}'
                else:
                    continue
            return f'Я не знайшов номер {phone} у {self.name}'
        else:
            return f'Номеру {phone.value}, який ти хочеш видалити, немає у списку контактів у {self.name}'
        
    def add_birthday(self, birthday: Birthday):
        # print("Enter to add_birthday function")
        # print(type(birthday))
        # print("birthday.value:", birthday.value)
        if self.birthday:
            # print(f'У {self.name} вже введений день народження {self.birthday}. Для зміни використайте команду "changebd"')
            return f'У {self.name} вже введений день народження {self.birthday.strftime("%d.%m.%Y")}. Для зміни використайте команду "changebd"'
        # self.birthday.value = birthday.value
        self.birthday = birthday
        # print(f'Я додав день народження {birthday.value} до списку контактів у {self.name}')
        return f'Я додав день народження {birthday.value.strftime("%d.%m.%Y")} до списку контактів у {self.name}'
    
    def change_birthday(self, new_birthday: Birthday):
        if self.birthday:
            old_birthday = str(self.birthday)
            return f'Я замінив день народження {old_birthday} на {new_birthday} у {self.name}'
        self.birthday.value = new_birthday.value
        return f'Я додав день народження {new_birthday} до списку контактів у {self.name}'
    
    def del_birthday(self, birthday: Birthday):
        if self.birthday:
            self.birthday.value = None
            return f'Я видалив {self.birthday} у {self.name}'
        return f'У {self.name} не введений день народження'
    
    def days_to_birthday(self, name: str):
        if self.birthday is None:
            return f'Для контакту {name} не вказаний день народження'
        else:
            today_date = datetime.now().date()
            birth_date = datetime.strptime(str(self.birthday), "%d.%m.%Y").date()
            
            next_birthday_date = datetime(today_date.year, birth_date.month, birth_date.day).date()
            if next_birthday_date < today_date:
                next_birthday_date = datetime(today_date.year + 1, birth_date.month, birth_date.day).date()
            timedelta = next_birthday_date - today_date
            if timedelta.days == 0:
                return f"Сьогодні день народження у {name}!"
            elif timedelta.days == 1:
                return f"Завтра день народження у {name}"
            elif timedelta.days == 2:
                return f"Післязавтра день народження у {name}"
            elif timedelta.days == 3:
                return f"Через {timedelta.days} дні день народження у {name}!"
            elif timedelta.days == 4:
                return f"Через {timedelta.days} дні день народження у {name}!"
            elif timedelta.days == -1:
                return f"Учора був день народження у {name}"
            else:
                return f"Через {timedelta.days} днів день народження у {name}!"
    
    def __str__(self):
        return f"{self.name}: {', '.join(str(phone) for phone in self.phones)}; birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        print("Enter to the AddressBook.add_record function")
        print("record.name:", record.name)
        if record.phones:
            print("record.phones:", record.phones)
        if record.birthday:
            print("record.birthday:", record.birthday)
        self.data[record.name] = record
        phones_print = ", ".join(str(phone_print) for phone_print in record.phones)
        # print(record.birthday)
        if record.birthday and record.phones:
            return f'Я додав контакт "{record.name}" з номером {phones_print} та днем народження {record.birthday} до книги контактів'
        if record.birthday and not record.phones:
            return f'Я додав контакт "{record.name}" з днем народження {record.birthday} до книги контактів'
                
        # if self.data[record.birthday]:
            # return f'Я додав контакт "{record.name}" з номером {phones_print} та днем народження {self.data[record.birthday]} до книги контактів'
        return f'Я додав контакт "{record.name}" з номером {phones_print} до книги контактів'
    
    def search_info(self, search_query):
        search_results = []
        for key_ab in self.data:
            record_name = str(self.data[key_ab].name)
            if search_query.lower() in record_name.lower():
                search_results.append(f'"{search_query}" знайдено у {record_name}')
                continue
            for phone in self.data[key_ab].phones:
                if search_query.lower() in str(phone).lower():
                    search_results.append(f'"{search_query}" знайдено у {record_name}: {str(phone).lower()}')
            if search_query in self.data[key_ab].birthday:
                search_results.append(f'"{search_query}" знайдено у {record_name}, день народження {self.data[key_ab].birthday}')
                continue
        if search_results:
            search_results = '\n'.join(search_results)
            return search_results
        return f'Я не зміг знайти нічого по запиту {search_query}'

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]
            return f'Я видалив запис {name}'
        return f'Я не зміг знайти запис {name}'

    def show_all_contacts(self):
        if self.values():
            return "\n".join(str(r) for r in self.values())
        else:
            return 'Книга контактів пуста'

    def __str__(self):
        return "\n" + "\n".join(str(record) for record in self.data.values())


# ==============================================
if __name__ == "__main__":
    name_1 = Name("Ivan")
    phone_1 = Phone("+380-50-448-99-99")
    birthday_1 = Birthday("01.01.2000")
    birthday_2 = Birthday("01.01.2001")
    record_1 = Record(name_1, phone_1, birthday_1)
    address_book_1 = AddressBook().add_record(record_1)
    print("address_book_1:", address_book_1)
    print("type(address_book_1):", type(address_book_1))
    # record_1.add_birthday(birthday_2)
    # print(address_book_1)
    record_request = address_book_1.data.get(str(name_1))
    print(record_request)