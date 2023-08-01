from classes import AddressBook, Name, Phone, Record, Birthday

address_book = AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Я не знайшов контакт"
        except ValueError:
            return "Неправильний формат вводу"
        except IndexError:
            return "Ти вказав неправильний формат команди. Будь ласка, спробуй ще раз або введи info для допомоги"
    return wrapper


@input_error
def info_command(*args):
    info_text = '''Доступні команди:
hello -- я привітаюсь.
info -- інформація про доступні команди.
add Ім'я номер_телефону -- додам до списку контакт з номером телефону.Не використовуйте пробіли у імені та номері телефону.
change Ім'я старий_номер_телефону новий_номер_телефону -- зміню номер телефону для контакту.
phone Ім'я -- покажу номер/-и телефону контакту.
search що_шукати -- спробую знайти те, що тобі потрібно.
delete Ім'я -- видалю запис.
show all -- покажу всі збережені контакти з номерами телефонів.
good bye або close або exit -- закінчу роботу
    '''
    return info_text


@input_error
def hello_command(*args):
    return "Чим можу допомогти?"


@input_error
def add_contact_command(*args):
    if len(args) == 2:
        name = Name(args[0])
        print("name:", name)
        phone = Phone(args[1])
        print("type(address_book):", type(address_book))
        rec = address_book.get(str(name))
        print(rec)
        print("address_book.data:", address_book.data)
        record = address_book.data.get(str(name))
        print("record:", record)
        record_1 = address_book.get(str(name))
        print("record_1:", record_1)
        if record:
            return record.add_phone(phone)
        record = Record(name, phone)
        return address_book.add_record(record)
    elif len(args) == 3:
        name = Name(args[0])
        # print("name:", type(name), name)
        phone = Phone(args[1])
        # print("phone:", type(phone), phone)
        birthday = Birthday(args[2])
        # print("birthday:", type(birthday), birthday)
        record = address_book.data.get(str(name))
        if record:
            return record.add_phone(phone), record.add_birthday(birthday)
        record = Record(name, phone, birthday)
        return address_book.add_record(record)
   

@input_error
def contact_change_command(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    record = address_book.data.get(str(name))
    if record:
        return record.change_phone(old_phone, new_phone)
    return f'Книга контактів не містить контакт {name}'


@input_error
def phone_command(*args):
    name = args[0]
    record = address_book.get(str(name))
    if record:
        phones_x = address_book.data.get(str(name)).phones
        p_list = []
        for p in phones_x:
            p_list.append(str(p))
        phones_x_list = " ".join(p_list)
        return f"Номер/-и телефону/-ів для контакту {name}: {phones_x_list}"
    return f'Книга контактів не містить контакт {name}'


@input_error
def search_command(*args):
    if args:
        search_query = str(args[0])
    if search_query:
        return address_book.search_info(search_query)
    return "Будь ласка, напиши, що треба шукати"


@input_error
def delete_command(*args):
    if len(args) != 1:
        return "Будь ласка, введи команду для видалення у правильному форматі"
    name = args[0]
    record = address_book.data.get(str(name))
    if record:
        address_book.delete_record(str(name))
        return f"Я видалив запис {name}"
    return f"У адресній книзі немає контакту {name}"


def add_birthday_command(*args):
    print("Enter to the add birthday function")
    if len(args) != 2:
        return "Будь ласка, введи команду для додавання дня народження у правильному форматі"
    name = Name(args[0])
    birthday_date = Birthday(args[1])
    record = address_book.data.get(str(name))
    print("record:", record)
    if record:
        # birthday_date = Birthday(args[1])
        return record.add_birthday(birthday_date)
    record = Record(name, birthday=birthday_date)
    return address_book.add_record(record)


def birthday_change_command(*args):
    print("Enter to the birthday change function")
    if len(args) != 2:
        return "Будь ласка, введи команду для зміни дня народження у правильному форматі"
    # name = Name(args[0])
    # new_birthday = Birthday(args[1])
    # print(address_book)
    # rec = address_book.get(str(name))
    # print("rec:", rec)
    # if rec:
    #     return rec.change_birthday(new_birthday)
    # return f'Книга контактів не містить контакт {name}'
    
    name = Name(args[0])
    print("name:", name)
    print("type(name):", type(name))
    new_birthday = Birthday(args[1])
    print("new_birthday:", new_birthday)
    print("type(new_birthday):", type(new_birthday))
    # record = address_book.data.get(str(name))
    record = address_book.data.get(str(name))
    print("record:", record)
    print("type(record):", type(record))
    # record = address_book.data.get("Ivan")
    # print("record:", record)
    print(address_book)
    if record:
        return record.change_birthday(new_birthday)
    return f'Книга контактів не містить контакт {name}'


@input_error
def birthday_command(*args):
    name = Name(args[0])
    record: Record = address_book.data.get(str(name))
    if record:
        return record.days_to_birthday(name)


@input_error
def show_all_contacts_command():
    return address_book.show_all_contacts()


@input_error
def bad_command(*args):
    return "Я не впізнав команду. Будь ласка, спробуй ще раз або введи info для допомоги"


@input_error
def exit_command(*args):
    return "Good bye!"


@input_error
def input_parser(user_input):
    for command, arguments in COMMANDS.items():
        for argument in arguments:
            if user_input.lower().startswith(argument):
                if user_input[:len(argument)] != argument:
                    user_input = argument + user_input[len(argument):]
                return command(*user_input.replace(argument, "").strip().split())
    return bad_command()


COMMANDS = {
        info_command: ["info"],
        hello_command: ["hello"],
        add_contact_command: ["add"],
        contact_change_command: ["change"],
        phone_command: ["phone"],
        search_command: ["search"],
        delete_command: ["delete"],
        birthday_command: ['birthday'],
        add_birthday_command: ['bdadd'],
        birthday_change_command: ['bdchange'],
        # birthday_delete_command: ['deletebd'],
        show_all_contacts_command: ["show all"],
        exit_command: ["good bye", "close", "exit"]
        }
    

def main():
    print("Вітаю! Я бот-помічник.")
    while True:
        user_input = input('\nВведи команду ("info" для допомоги) >>> ')
        result = input_parser(user_input)
        if isinstance(result, str):
            print(result)
        elif isinstance(result, tuple):
            print(*result, sep=".\n")
        if result == "Good bye!":
            break
    
if __name__ == "__main__":
    main()