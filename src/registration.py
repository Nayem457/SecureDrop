import json
import shutil
from pathlib import Path
from getpass import getpass

from src.crypto_utils import User
from src.certificates import save_user_identity


def register_user():
    name = input("Enter your full name: ").strip()
    email = input("Enter your email: ").strip().lower()
    password = getpass("Enter your password: ")
    confirm_password = getpass("Confirm your password: ")

    if not name or not email or not password:
        print("Name, email, and password cannot be empty!")
        return False

    if password != confirm_password:
        print("Passwords do not match!")
        return False

    users_file = Path("users.json")

    try:
        # check for an existing account
        if users_file.exists():
            with users_file.open("r") as file:
                existing_users = json.load(file)

            if any(
                existing["email"].lower() == email
                for existing in existing_users
            ):
                print("Email already registered!")
                return False

        # generate encrypted private key and CA-signed certificate
        identity_dir = save_user_identity(email, password)

        try:
            # save user account
            user = User(name, email, password)

            if not user.save_user():
                raise RuntimeError("Failed to save user account.")

            print("Registration completed successfully!")
            return True

        except Exception as error:
            # remove identity files if saving the account fails
            shutil.rmtree(identity_dir)
            print("Registration failed:", error)
            return False

    except (OSError, ValueError, json.JSONDecodeError) as error:
        print("Registration failed:", error)
        return False


if __name__ == "__main__":
    register_user()