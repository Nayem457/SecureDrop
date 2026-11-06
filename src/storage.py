# enrypt contacts using AES-256-GCM
# saving the encrypted contacts to json file
# decrypt contacts when the user logs in
# detecting unauthorized modification

import json
import os
from pathlib import Path
import hashlib

from cryptography.hazmat.primitives.ciphers.aead import AESGCM  #

CONTACTS_DIR = Path("contacts_data")  # directory where the encrypted contacts will be stored

def get_contacts_path(email):
    user_id = hashlib.sha256( #this function generates a unique user ID based on the email address using SHA-256 hashing
        email.strip().lower().encode("utf-8")  #take the email, strip whitespace, convert to lowercase, encode to bytes and hash it using SHA-256
    ).hexdigest()

    return CONTACTS_DIR / f"{user_id}.json" 

def save_encrypted_contacts(email, contacts, key):
    CONTACTS_DIR.mkdir(parents=True, exist_ok=True)  # create the contacts directory if it doesn't exist

    path = get_contacts_path(email)  #get the path to the contacts file for this user

    plaintext = json.dumps(contacts).encode("utf-8")  #convert the contacts to a JSON string and encode it to bytes

    nonce = os.urandom(12)  #generate a random nonce for AES-GCM

    aesgcm = AESGCM(key) #encrypt and authenticate the contacts list using AES-256-GCM with the provided key and nonce

    ciphertext = aesgcm.encrypt( # encrypt the plaintext contacts using AES-GCM
        nonce,
        plaintext,
        email.strip().lower().encode("utf-8") 
    )

    # save the nonce and ciphertext to a JSON file
    data = {
        "nonce": nonce.hex(),
        "ciphertext": ciphertext.hex()
    }

    with path.open("w") as file:
        json.dump(data, file, indent=4)

# decrypt the contacts list using AES-256-GCM with the provided key and nonce
def load_encrypted_contacts(email, key):
    path = get_contacts_path(email)

    if not path.exists():
        return {}
    
    with path.open("r") as file:
        data = json.load(file)
    
    nonce = bytes.fromhex(data["nonce"])
    ciphertext = bytes.fromhex(data["ciphertext"])

    aesgcm = AESGCM(key)

    plaintext = aesgcm.decrypt(
        nonce,
        ciphertext,
        email.strip().lower().encode("utf-8")
    )

    return json.loads(plaintext.decode("utf-8"))  #decode the plaintext bytes to a JSON string and convert it back to a Python object


