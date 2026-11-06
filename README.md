SecureDrop

SecureDrop is a Python-based application for securely sharing files over a local network.

This project is developed for COMP 2300 — Introduction to Computer Security at UMass Lowell.

Features

Completed (Milestones 1–3)

* User registration and login
* Secure password hashing using scrypt
* RSA key generation and digital certificates
* User session management
* Add and update contacts
* AES-256-GCM encrypted contact storage
* Contact integrity protection

Upcoming (Milestones 4–5)

* Online contact discovery
* Mutual authentication
* Secure file transfers

Requirements

* Python 3.9+
* PyCryptodome
* cryptography

Installation

Clone the repository:

git clone https://github.com/Nayem457/SecureDrop.git
cd SecureDrop

Install dependencies:

python3 -m pip install -r requirements.txt

Running SecureDrop

First, initialize the development certificate authority:

python3 -m src.ca

Then start SecureDrop:

python3 secure_drop.py

If no user is registered, the application will prompt you to create an account.

Otherwise, log in with your registered email and password.

Commands

Command	Description
help	Show available commands
add	Add or update a contact
whoami	Show current user
exit	Log out and exit
logout	Log out
quit	Exit SecureDrop

Security

* Passwords are protected using scrypt.
* User private keys are encrypted.
* Contacts are encrypted using AES-256-GCM.
* Modified encrypted contact data is detected during decryption.
* User sessions are closed after logout.

Note: The development CA private key must never be uploaded to GitHub or shared with other clients.

Project Status

Milestone	Status
1 — User Registration	Completed
2 — User Login	Completed
3 — Adding Contacts	Completed
4 — Listing Contacts	In Progress
5 — Secure File Transfer	Not Started