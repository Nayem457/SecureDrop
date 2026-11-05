
SecureDrop is a Python based peer-to-peer file transfer application designed to allow users to securely share files over a local network.

The project focuses on user authentication, encryption, contact management, and secure file transfers.

Course: COMP 2300 — Introduction to Computer Security
Project: Secure File Transfer Tool
Status: In Development

Features

Currently Implemented

* User registration with email and password
* Password hashing using scrypt
* Persistent user account storage using JSON
* Login authentication
* Secure password verification
* User session management
* Contact encryption key derivation
* Interactive command-line interface
* Logout functionality

Planned Features

* Encrypted contact management
* Contact discovery over a local network
* Mutual authentication between users
* Secure encrypted file transfers
* File integrity verification
* Replay attack protection

Requirements

* Python 3.9 or newer
* pip
* PyCryptodome

The project is intended to support macOS, Windows, and Linux.

Installation

1. Clone the Repository

git clone https://github.com/Nayem457/SecureDrop.git
cd SecureDrop

2. Install Dependencies

macOS / Linux:

python3 -m pip install -r requirements.txt

Windows:

py -m pip install -r requirements.txt

Make sure requirements.txt includes:

pycryptodome

Running SecureDrop

Run the following commands from the project’s root directory.

1. Register a New User

macOS / Linux:

python3 -m src.registration

Windows:

py -m src.registration

You will be prompted to enter:

Enter your full name:
Enter your email:
Enter your password:
Confirm your password:

After successful registration:

User registered successfully!

User information is stored locally in users.json.

Passwords are not stored in plaintext. SecureDrop stores a password hash and a randomly generated salt.

2. Log In

macOS / Linux:

python3 -m src.login

Windows:

py -m src.login

Enter your registered email and password.

Example:

Enter your email: test@gmail.com
Enter your password:
Login successful!
Welcome to SecureDrop!
Type 'help' to see available commands.

3. Use the Command Interface

After successful login, the following prompt appears:

secure_drop>

Available commands:

Command	Description
help	Display available commands
whoami	Display the authenticated user’s email
logout	End the session
exit	Exit the application
quit	Exit the application

Example:

secure_drop> help
Available commands: help, whoami, logout
secure_drop> whoami
Logged in as: test@gmail.com
secure_drop> logout
Logging out...

4. Incorrect Login Credentials

If the email or password is incorrect:

Invalid email or password.

The command interface will not start.

Security

Password Protection

SecureDrop uses the scrypt key derivation function to protect user passwords.

The current implementation uses:

* N = 16384
* r = 8
* p = 1
* Hash length = 32 bytes
* Random salt = 16 bytes

Session Management

After successful authentication, SecureDrop creates a session containing the user’s email and a separate 32-byte key derived for contact encryption.

When the user logs out, the session is marked inactive and its reference to the encryption key is cleared.

Local Data

The users.json file contains local account information, password hashes, and salts.

It should not be committed to GitHub.

Add the following entry to .gitignore:

users.json

Project Structure

SecureDrop/
├── src/
│   ├── __init__.py
│   ├── crypto_utils.py
│   ├── registration.py
│   ├── login.py
│   ├── session.py
│   ├── contacts.py
│   └── storage.py
├── tests/
├── secure_drop.py
├── requirements.txt
├── .gitignore
└── README.md

Some modules are still under development.

Development Status

SecureDrop is being developed as a team project.

The current implementation provides registration, login, and session management.

Encrypted contacts, peer discovery, and secure file transfers will be integrated in later development stages.

Troubleshooting

Problem: ModuleNotFoundError: No module named 'Crypto'

Install PyCryptodome:

python3 -m pip install pycryptodome

On Windows:

py -m pip install pycryptodome

Problem: FileNotFoundError: users.json

Register a user before attempting to log in. Run all commands from the SecureDrop project root directory.

Problem: Invalid email or password

Check that the email is registered and the password matches the one used during registration.

Team Collaboration

The project uses GitHub for version control.

Developers should work on separate feature branches and submit pull requests for review before merging changes into main.