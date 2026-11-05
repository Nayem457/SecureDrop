from getpass import getpass
from src.crypto_utils import User


name = input("Enter your full name: ").strip()
email = input("Enter your email: ").strip().lower()
password = getpass("Enter your password: ")
confirm_password = input("Confirm your password: ")

if name == "" or email == "" or password == "":
    print("Name, email, and password cannot be empty!")
    exit(1)

elif password != confirm_password:
    print("Passwords do not match!")
    exit(1)

user = User(name, email, password)
user.save_user()