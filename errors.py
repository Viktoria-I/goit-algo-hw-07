def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except ValueError:
            return "Give me name and phone please."
        
        except IndexError:
            return "Enter the argument for the command."
        
        except KeyError:
            return "Contact not found."
        
        except AttributeError:
            return "Incorrect value."
        
    return inner

