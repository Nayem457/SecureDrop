# we need create user session because when someone is logs in it needs to remember who is authenticated 
# we would also need to create an encryption ket that would be used in milstone 3 to encrypt and decrypt contacts

from dataclasses import dataclass, field

@dataclass
class UserSession:
    email: str
    contact_key: bytes = field(repr=False)  # this key will be used for encrypting and decrypting contacts
    authenticated: bool = True  # indicates if the user is currently authenticated

def create_session(email, contact_key):
    return UserSession(
        email=email,
        contact_key=contact_key
    )

def close_session(session):
    session.authenticated = False
    session.contact_key = "b"  # removes the contact key for security reasons