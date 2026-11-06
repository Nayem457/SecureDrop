# create certificate authority class that will be used to create and manage certificates for users

from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography import x509 # x509 is a module that provides classes and functions for working with X.509 certificates
from cryptography.hazmat.primitives import hashes, serialization # serialization is used to convert the certificate and keys to bytes so they can be saved to files
from cryptography.hazmat.primitives.asymmetric import rsa # rsa is a module that provides classes and functions for working with RSA keys
from cryptography.x509.oid import NameOID # NameOID is a module that provides classes and functions for working with X.509 distinguished names

CA_DIR = Path("ca") # directory where the CA's private key and certificate will be stored
CA_KEY_PATH = CA_DIR / "ca_key.pem" # file where the CA's private key will be stored
CA_CERT_PATH = CA_DIR / "ca_cert.pem" # file where the CA's certificate will be stored

def create_ca():
    CA_DIR.mkdir(exist_ok=True) # create the CA directory if it doesn't exist

    if CA_KEY_PATH.exists() or CA_CERT_PATH.exists():
        print("CA files already exists. Not overwriting.")
        return
    
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )

    subject = x509.Name([
        x509.NameAttribute(
            NameOID.COMMON_NAME,
            "SecureDrop Certificate CA"
        )
    ])

    now = datetime.now(timezone.utc)

    certificate = (
        x509.CertificateBuilder() # create a new certificate builder object
        .subject_name(subject) # set the subject name of the certificate to the CA's distinguished name
        .issuer_name(subject) # set the issuer name of the certificate to the CA's distinguished name (self-signed)
        .public_key(private_key.public_key()) # set the public key of the certificate to the CA's public key
        .serial_number(x509.random_serial_number()) # set the serial number of the certificate to a random value
        .not_valid_before(now) # set the not valid before date of the certificate to the current time
        .not_valid_after(now + timedelta(days=3650)) # set the not valid after date of the certificate to 10 years from now
        .add_extension( # add an extension to the certificate
            x509.BasicConstraints(ca=True, path_length=0), 
            critical=True
        )
        .add_extension( # add a key usage extension to the certificate
            x509.KeyUsage( # key_usage extension specifies the purpose of the key contained in the certificate
                digital_signature=True, # the key can be used for digital signatures
                key_encipherment=True, # the key can be used for key encipherment
                key_cert_sign=True, # the key can be used for signing other certificates
                crl_sign=True, # the key can be used for signing certificate revocation lists
                key_agreement=False, # the key cannot be used for key agreement
                content_commitment=False, # the key cannot be used for content commitment
                data_encipherment=False, # the key cannot be used for data encipherment
                encipher_only=False, # the key cannot be used for enciphering only
                decipher_only=False # the key cannot be used for deciphering only
            ),
            critical=True
        )
        .sign(private_key, hashes.SHA256()) # sign the certificate with the CA's private key using SHA-256
        
    )

    key_bytes = private_key.private_bytes( # serialize the private key to bytes
        encoding=serialization.Encoding.PEM, # the format in which the key will be serialized PEM is a common format for storing cryptographic keys
        format=serialization.PrivateFormat.PKCS8, # the format in which the private key will be serialized PKCS8 is a standard format for storing private keys
        encryption_algorithm=serialization.NoEncryption() # the private key will not be encrypted when serialized
    )

    with CA_KEY_PATH.open("xb") as file:
        file.write(key_bytes)
    
    CA_KEY_PATH.chmod(0o600) # set the permissions of the private key file to be readable and writable only by the owner

    cert_bytes = certificate.public_bytes(
    serialization.Encoding.PEM
)
    with CA_CERT_PATH.open("xb") as file:
        file.write(cert_bytes)
    
    
    
    print("SecureDrop CA created successfully!")
    print("CA certificate: ", CA_CERT_PATH)
    print("CA private key: ", CA_KEY_PATH)


if __name__== "__main__":
    create_ca()





