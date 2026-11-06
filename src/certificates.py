# we need to create a certificate class that will be used to create and manage certificates for users
# this class will handle the creation, validation, and revocation of certificates

import os
import hashlib
from datetime import datetime, timedelta, timezone
from pathlib import Path
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

def generate_key_pair(password):
    # generate a 3072-bit RSA private key
    private_key = rsa.generate_private_key( #generates a new RSA private key
        public_exponent=65537, # public exponent is a small prime number that is used in the key generation process
        key_size=3072 # the size of the key in bits larger keys are more secure but slower to generate and use
    )

    public_key = private_key.public_key() # extract the public key from the private key

    encrypted_private_key = private_key.private_bytes( # serialize the private key to bytes and encrypt it with the provided password
        encoding=serialization.Encoding.PEM, # the format in which the key will be serialized PEM is a common format for storing cryptographic keys
        format=serialization.PrivateFormat.PKCS8, # the format in which the private key will be serialized PKCS8 is a standard format for storing private keys
        encryption_algorithm=serialization.BestAvailableEncryption( #encrypts the private key using the user’s password
            password.encode("utf-8") # the password used to encrypt the private key must be provided as bytes
        )
    )

    public_key_bytes = public_key.public_bytes( # serialize the public key to bytes
        encoding=serialization.Encoding.PEM, # the format in which the key will be serialized PEM is a common format for storing cryptographic keys
        format=serialization.PublicFormat.SubjectPublicKeyInfo # the format in which the public key will be serialized SubjectPublicKeyInfo is a standard format for storing public keys
    )

    return encrypted_private_key, public_key_bytes # return the encrypted private key and the public key as bytes

def generate_user_certificate(email, public_key_pem):

    #load the CA's private key from the PEM file
    ca_private_key = serialization.load_pem_private_key(
        Path("ca/ca_key.pem").read_bytes(),
        password=None
    )

    #load the CA's certificate from the PEM file
    ca_certificate = x509.load_pem_x509_certificate(
        Path("ca/ca_cert.pem").read_bytes()
    )

    #load the user's public key from the PEM file
    public_key = serialization.load_pem_public_key(public_key_pem)

    #identity of the user based on their email address
    subject = x509.Name([
        x509.NameAttribute(NameOID.EMAIL_ADDRESS, email)
    ])

    now = datetime.now(timezone.utc)

    #create a new certificate for the user
    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_certificate.subject)
        .public_key(public_key)
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=365))
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None),
            critical=True
        )

        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False
            ),
            critical=True
        )
        .sign(ca_private_key, hashes.SHA256())

    )

    return certificate.public_bytes(
        serialization.Encoding.PEM
    )

def verify_user_certificate(cert_pem, expected_email):
    try:
        # load the user's certificate
        user_cert = x509.load_pem_x509_certificate(cert_pem)

        # load our trusted CA certificate
        ca_cert = x509.load_pem_x509_certificate(
            Path("ca/ca_cert.pem").read_bytes()
        )

        # verify that the certificate was issued by our CA
        if user_cert.issuer != ca_cert.subject:
            return False

        # verify the CA's digital signature
        ca_cert.public_key().verify(
            user_cert.signature,
            user_cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            user_cert.signature_hash_algorithm
        )

        # verify the certificate has not expired
        now = datetime.now(timezone.utc)

        if not (
            user_cert.not_valid_before_utc
            <= now
            <= user_cert.not_valid_after_utc
        ):
            return False

        # verify the certificate belongs to the expected email
        emails = user_cert.subject.get_attributes_for_oid(
            NameOID.EMAIL_ADDRESS
        )

        if len(emails) != 1:
            return False

        if emails[0].value.lower() != expected_email.lower():
            return False

        # Ensure this is a user certificate, not a CA certificate
        constraints = user_cert.extensions.get_extension_for_class(
            x509.BasicConstraints
        ).value

        if constraints.ca:
            return False

        return True

    except (InvalidSignature, ValueError, TypeError, x509.ExtensionNotFound):
        return False

def save_user_identity(email, password):
    # create a unique directory name based on the email
    user_id = hashlib.sha256(
        email.strip().lower().encode("utf-8")
    ).hexdigest()

    identity_dir = Path("identities") / user_id

    # prevent overwriting an existing identity
    if identity_dir.exists():
        raise FileExistsError("User identity already exists.")

    # generate the user's RSA key pair
    encrypted_private_key, public_key_pem = generate_key_pair(password)

    # generate a CA signed certificate
    certificate_pem = generate_user_certificate(
        email,
        public_key_pem
    )

    # verify the certificate before saving
    if not verify_user_certificate(certificate_pem, email):
        raise ValueError("Certificate verification failed.")

    # create a private directory for this user
    identity_dir.mkdir(parents=True, mode=0o700)

    # save the encrypted private key
    private_key_path = identity_dir / "private_key.pem"

    with private_key_path.open("xb") as file:
        file.write(encrypted_private_key)

    private_key_path.chmod(0o600)

    # save the user's public certificate
    certificate_path = identity_dir / "certificate.pem"

    with certificate_path.open("xb") as file:
        file.write(certificate_pem)

    print("User identity created successfully!")

    return identity_dir
     
     