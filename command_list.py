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
    name, old_phone, new_phone = args
    record = book.find(name)

    if not record:
        return "Contact not found."
    for phone in record.phones:
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."


@input_error
def show_phone(args, book):

    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    
    return f"{name}: {', '.join(p.value for p in record.phones)}"
    

@input_error
def show_all(book):
    
    print("Your contacts:")
    for record in book.data.values(): 
        print(f"{record.name.value}: {', '.join(p.value for p in record.phones)}, Birthday: {record.birthday}")


@input_error
def add_birthday(args, book):
    
    name, b_date = args

    record = book.get(name)
    if record:
        try:
            record.add_birthday(b_date)
            return "Birthday added."
        except ValueError:
            return "Invalid date format or date in the future"
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
