# this class checks if the user is registered and if so, it will start the shell for the user to interact with the secure drop system
import json
from pathlib import Path 
from src.registration import register_user
from src.login import login_user, start_shell

def main(): 

    print("Welcome to SecureDrop!")

    users_file = Path("users.json")

    has_users = False # check if there are any users registered

    if users_file.exists():
        try:
            with users_file.open("r") as file:
                users = json.load(file)
            
            has_users = len(users) > 0 
        
        except (OSError, json.JSONDecodeError) as error:
            print("Unable to read users accounts:", error)
            return
    
    # first time setup: if no users are registered, prompt for registration
    if not has_users:
        print("No users are registered with this client")

        choice = input(
            "Do you want to register a new user? (y/n): "
        ).strip().lower()

        if choice == "y":
            register_user()
        
        print("Exiting SecureDrop.")
        return

    session = login_user() #
    
    if session:
            start_shell(session)

if __name__ == "__main__":
    main()