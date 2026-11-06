# add contact 
from src.storage import (
    load_encrypted_contacts,
    save_encrypted_contacts,
)

def add_contact(session):
    if not session.authenticated:
        print("You must be logged in to add contacts.")
        return
    
    name = input("Enter contact's name: ").strip()
    email = input("Enter contact's email: ").strip().lower()

    if not name or not email:
        print("Name and email cannot be empty!")
        return
    
    if "@" not in email or "." not in email.split("@")[-1]:
        print("Invalid email adress.")
        return
    
    if email == session.email.strip().lower():
        print("You cannot add yourself as a contact.")
        return
    
    try: 
        # load the current user's encrypted contacts
        contacts = load_encrypted_contacts(
            session.email,
            session.contact_key
        )

        # add or update the contact
        contacts[email] = {
            "name": name,
            "email": email
        }
        
        # encrypt and save the updated list
        save_encrypted_contacts(
            session.email,
            contacts,
            session.contact_key
        )

        print("Contact Added.")
    
    except Exception as error:
        print("Unable to add contact:", error)
    