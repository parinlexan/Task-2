import random
import string

def generate_email():
    random_string = ''.join(random.choices(string.ascii_lowercase, k=10))
    random_domain = ''.join(random.choices(string.ascii_lowercase, k=5))
    random_tld = random.choice(['com', 'net', 'org'])
    email = f"{random_string}@{random_domain}.{random_tld}"
    return email

def generate_password():
    password = ''.join(random.choices(string.ascii_lowercase, k=10))
    return password

def generate_name():
    login = ''.join(random.choices(string.ascii_lowercase, k=10))
    return login