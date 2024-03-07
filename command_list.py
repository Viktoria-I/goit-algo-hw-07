from errors import input_error
from classes import AddressBook, Name, Phone, Record, Birthday
from datetime import datetime, timedelta


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone and phone not in record.phones:
        record.add_phone(phone)
    else:
        message = "Phone number already exists in the contact {name}."
    return message


@input_error
def change_contact(args, book):

    name, phone = args
    try:
        record = book.data[name]
    except KeyError:
        return "Contact not found."
    record.phones = [Phone(phone)]
    return "Phone number updated."


@input_error
def show_phone(args, book):

    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    return f"{name}: {record.phones[0].value}"


@input_error
def show_all(book):

    print("Your contacts:")
    for record in book.data.values():  
        print(f"{record.name.value}: {', '.join(p.value for p in record.phones)}")


@input_error
def add_birthday(args, book):
    
    name, b_date = args

    try:

        b_day = datetime.strptime(b_date, "%d.%m.%Y")
        if b_day.year < 1900 or b_day.year > (datetime.now() - timedelta(days=1830)).year:
            raise ValueError

    except ValueError as e:
        return "Invalid date format. Use DD.MM.YYYY. Year should be between 1900 and 2021."

    record = book.get(name)
    if record:
        try:
            record.add_birthday(b_date)
        except ValueError as e:
            return "Invalid date format. Use DD.MM.YYYY."
        
        return "Birthday added."
    else:
        return "Contact not found."
    

@input_error
def show_birthday(args, book):

    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    
    if record.birthday:
        return f"{name}: {record.birthday}"
    else:
        return "No birthday date."


# @input_error
def upcoming_birthdays(book):

    return book.get_upcoming_birthdays()
