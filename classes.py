from collections import UserDict
from datetime import datetime
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
    def __init__(self, value):
        super().__init__(value)
        if not self.validate():
            raise ValueError("Invalid name")
        
    def validate(self):
        return len(self.value) > 0

class Phone(Field):
    # реалізація класу
    def __init__(self, value):
        super().__init__(value)
        if not self.validate():
            raise ValueError("Invalid phone number")
        
    # перевірка на правильність введення номеру телефону
    def validate(self):
        return len(self.value) == 10 and self.value.isdigit()

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break
        else:
            raise ValueError(f"Phone number {phone} not found")

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                if Phone(new_phone).validate():
                    phone.value = new_phone
                    break
                else:
                    raise ValueError("Invalid new phone number")
        else:
            raise ValueError(f"Phone number {old_phone} not found")   

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            value = datetime.strptime(value, "%d.%m.%Y")
            if value > datetime.now():
                raise ValueError
        except ValueError:
            raise ValueError("Invalid date format or date in the future")
        self.value = value
        
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")    

class AddressBook(UserDict):
    # реалізація класу
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
        else:
            raise KeyError(f"'{name}' not found")

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        current_year = datetime.now().year

        for name, record in self.data.items():

            if record.birthday:

                b_day = record.birthday
                b_day_str = b_day.__str__()
                current_year = datetime.now().year
                b_date = datetime.strptime(b_day_str, "%d.%m.%Y")
                b_date = b_date.replace(year=current_year)
                b_date = b_date.date()
                if b_date < datetime.now().date():
                    b_date = b_date.replace(year=current_year + 1)

                if b_date.weekday() == 5:
                    congratulation_date = b_date + timedelta(days=2)
                elif b_date.weekday() == 6:
                    congratulation_date = b_date + timedelta(days=1)
                else:
                    congratulation_date = b_date

                if congratulation_date - datetime.now().date() <= timedelta(days=7):
                    upcoming_birthdays.append({"name": name, "congratulation_date": congratulation_date.strftime("%d.%m.%Y")})

        return upcoming_birthdays