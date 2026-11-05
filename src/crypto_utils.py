import json
import os

from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes


class User:
    key_len = 32
    n = 2 ** 14
    r = 8
    p = 1

    def __init__(self, name, email, password):
        self.name = name
        self.email = email.strip().lower()

        self.salt = get_random_bytes(16)

        self.password_hash = scrypt(
            password,
            self.salt,
            self.key_len,
            self.n,  
            self.r,
            self.p
        )

    def save_user(self):
        filename = "users.json"

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                users = json.load(file)
        else:
            users = []

        for user in users:
            if user["email"].lower() == self.email:
                print("Email already registered!")
                return False

        new_user = {
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash.hex(),
            "salt": self.salt.hex(),
        }

        users.append(new_user)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4)

        print("User registered successfully!")
        return True
    





