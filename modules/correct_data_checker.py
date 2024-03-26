import re

def check_phone_number(phone_number: str):
    data = ""
    if re.match(r"^\d{3}-\d{3}-\d{4}$", phone_number) or re.match(r"^\d{3}\d{3}\d{4}$", phone_number):
        data =  phone_number
    elif re.match(r"^\d{3} \d{3} \d{4}$", phone_number):
        data =  "-".join(phone_number.split())
    else:
        data = 0
    return data

def check_email(email: str):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):  
        data = email
    else:
        data = 0
    return data
