from src.login import login_user
from src.storage import load_encrypted_contacts
from src.session import close_session


def main():
    session = login_user()

    if not session:
        print("Login failed.")
        return

    try:
        contacts = load_encrypted_contacts(
            session.email,
            session.contact_key
        )

        print("\nDecrypted contacts:")
        for email, details in contacts.items():
            print(f"- {details['name']} <{email}>")

    finally:
        close_session(session)


if __name__ == "__main__":
    main()