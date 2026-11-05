import json
import hmac  #allows comparison of hashes
from getpass import getpass #to hide password input
from Crypto.Protocol.KDF import scrypt
from src.session import create_session, close_session

def login_user():
    email = input("Enter your email: ").strip().lower()
    password = getpass("Enter your password: ")  #use getpass later

    with open ("users.json", "r") as file:
        users = json.load(file)

    for user in users:
        if user["email"].lower() == email:

            salt = bytes.fromhex(user["salt"]) #take the salt from the user data and convert it to bytes
            stored_hash = bytes.fromhex(user["password_hash"]) #convert the stored hash to bytes

            calculated_hash = scrypt(  #hash the entered password with the same salt and parameters
                password,
                salt,
                len(stored_hash),
                N=user.get("scrypt_n", 2**14),
                r=user.get("scrypt_r", 8),
                p=user.get("scrypt_p", 1)
            )

            if hmac.compare_digest(calculated_hash, stored_hash): #compare the calculated hash with the stored hash
                import hashlib #use a seprate stable salt for the contact encryption

                contact_salt = hashlib.sha256( 
                    b"SecureDrop-contacts-v1" + salt
                ).digest()[:16]  #take the first 16 bytes of the hash as the contact salt

                contact_key = scrypt( #derive a seprate key for encrypting contacts
                    password,
                    contact_salt,
                    32,
                    N=user.get("scrypt_n", 2**14),
                    r=user.get("scrypt_r", 8),
                    p=user.get("scrypt_p", 1)
                ) 

                #create a session for the authenticated user
                session = create_session(email, contact_key)

                print("Login successful!")
                return session  
            
            else:
                print("Invalid email or password!")
                return False
    
    print("Invalid email or password!")
    return False

def start_shell(session):
    print("\nWelcome to SecureDrop!")
    print("Type 'help' to see available commands.\n")

    try: #handle user input in a loop until they logout or exit
        while session.authenticated:
            command = input(("secure_drop> ")).strip().lower()

            if command == "help":
                print("Available commands: help, logout, whoami, logout")
            
            elif command == "whoami":
                print("Logged in as:", session.email)
            
            elif command in("logout", "exit", "quit"):
                print("Logging out.....")
                break
            elif command == "":
                continue
            else:
                print("Unknown command. Type 'help'.")
    
    except (KeyboardInterrupt, EOFError): #handle Ctrl+C or Ctrl+D 
        print("\nLogging out.....")

    finally:
        close_session(session)
        print("Logged out successfully!")

if __name__ == "__main__":
    session = login_user()

    if session:
        start_shell(session)
