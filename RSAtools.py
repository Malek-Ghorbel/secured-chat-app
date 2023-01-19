from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

#generating keys
def generate_private_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return (private_key)

def get_public_key(private_key):
    return(private_key.public_key())

#formatting in pem 
def write_keys_to_disk(private_key):
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    pem_public_key = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    #writing to disk
    private_key_file = open("private.pem", "w")
    private_key_file.write(pem_private_key.decode())
    private_key_file.close()

    public_key_file = open("pub.pem", "w")
    public_key_file.write(pem_public_key.decode())
    public_key_file.close()

#serializing key to be sent
def serialize_key(public_key):
    public_key_data = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return(public_key_data)

def desrialize_key(public_key_data):
    public_key = serialization.load_pem_public_key(public_key_data)
    return(public_key)

#encryptig-decrypting
def encrypt_message(public_key , message) :
    message = message.encode()
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return(ciphertext)

def decrypt_message(private_key , ciphertext):
    try:
        #test to see if the entered text is encrypted or not
        #if it can be decoded then it's not encrypted 
        #if it throws an exception then it's encrypted and needs decryption
        ciphertext.decode('utf-8')
        return ciphertext.decode('utf-8')
    except:
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return(plaintext.decode())

#signing-verifying
def sign_message(private_key , message ):
    message = message.encode()
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    #print(signature)
    return(signature)

def verify_signature(public_key , signature, message):
    return (public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    ))
