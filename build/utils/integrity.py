'''
Validate incoming messages: Incoming MQTT messages should be validated to ensure that they come from a trusted source 
and that the contents of the message have not been tampered with.
'''
__all__ = (
    "keygen",
    "signMessage",
    "extract",
    "verifySignature",
    "verifyAndExtract"
)
import json, hashlib, binascii
from utils.conf import Conf
from datetime import datetime, timedelta
import warnings

#https://www.pyopenssl.org/en/stable/changelog.html#id37
# we don't use deprecated features. str for passphrase is no longer accepted, use bytes
warnings.filterwarnings("ignore", category=DeprecationWarning) 
from OpenSSL.crypto import (
    TYPE_RSA,
    FILETYPE_PEM,
    FILETYPE_ASN1,
    FILETYPE_TEXT,
    Error,
    PKey,
    dump_certificate,
    dump_privatekey,
    load_certificate,
    sign,
    verify,
    load_pkcs12,
    X509,
    X509Name,
    PKCS12,
    
)


config = Conf().config


def keygen():
    """Generate RSA 2048 public-private pair with keylength of 2048

    Returns:
        cert, PKey: public X509 certificate, PKCS12 Key
    """
    key = PKey()
    key.generate_key(TYPE_RSA, 2048)
    
    cert = X509()
    
    # https://stackoverflow.com/questions/33764285/python-openssl-how-to-create-an-x509name-object
    subject = X509Name(cert.get_subject())
    subject.CN = b"platform-info-display"
    cert.set_subject(subject)
    
    issuer = X509Name(cert.get_subject())
    issuer.CN = b"platform-info-display"
    cert.set_issuer(issuer)
    
    now = datetime.utcnow()
    expiry_date = now + timedelta(days=365)
    cert.set_notBefore(now.strftime("%Y%m%d%H%M%SZ").encode())
    cert.set_notAfter(expiry_date.strftime("%Y%m%d%H%M%SZ").encode())
    
    cert.set_pubkey(key)
    cert.sign(key, "sha256")
    
    return cert, key


def dump(key, cert, password, enc_file, config_file):
    """Dump the key to encrypted PKCS12 file and token to config file

    Args:
        key (PKey): PKCS12 Key
        cert (X509): public X509 certificate
        password (str): password to encrypt the key
        enc_file (str): path to encrypted file
        config_file (str): path to config file
    """
    
    if 'validation' not in config.sections():
        config.add_section('validation')
    
    pkcs12 = PKCS12()
    pkcs12.set_certificate(cert)
    pkcs12.set_privatekey(key)
    pkcs12.set_ca_certificates([cert])
    
    digest = binascii.hexlify(pkcs12.export(passphrase=password.encode()))
    config.set('validation', 'token', password)
    
    try: 
        with open(enc_file, "wb") as f:
            f.write(digest)
        
        with open(config_file, "w") as f:
            config.write(f)
    except IOError as ex:
        print(f"Failed to write to {config_file}/{enc_file}", ex)
    
    return digest


def load(path, password): 
    """Load the key from encrypted file

    Args:
        path (str): path to encrypted file
        password (str): password to decrypt the key

    Returns:
        X509, PKey: X509 Certificate, PKCS12 Key
    """

    try:
        with open(path, "rb") as ef:
            enc_data = ef.read()
            
            pfx = load_pkcs12(bytes.fromhex(enc_data.decode()), password.encode())
            return pfx.get_certificate(), pfx.get_privatekey()
    
    except Error:
        print("verify failure on PKCS12 file")
        return None, None
        
    except IOError as ex:
        print(f"Failed to read {path}", ex)
        return None, None
    
   


def signMessage(message, private_key):
    """Sign message using private SHA256 signature

    Args:
        message (str): message to digest
        private_key (PKey): PKCS12 Key

    Returns:
        str: signed message in hexadecimal string
    """
    encoded = message.encode()
    digest = hashlib.sha256(encoded).digest()
    signature = sign(private_key, digest, "sha256")
    return message + binascii.hexlify(signature).decode()


def extract(signed_message):
    """Extract the signature and the message from signed message

    Args:
        signed_message (str): a string message with embedded signature

    Returns:
        str, str: tuple of signature and message in that order
    """
    message, signature = signed_message[:-512], bytes.fromhex(signed_message[-512:])
    return signature, message


def verifySignature(signature, message, cert):
    """Verify the signature of a signed message

    Args:
        signature (str): signature to verify
        message (str): message to verify
        pkey (X509): public X509 Certificate

    Returns:
        bool: True if signature is verified
    """
    try:
        digest = hashlib.sha256(message.encode()).digest()
        verify(cert, signature, digest, "sha256")
        return True
    except Error as e:
         return False
    
    
def verifyAndExtract(signed_message, cert):
    """verify the integrity of data and extract the message.

    Args:
        signed_message (str | bytes): data to extract from and to verify
        cert (X509): public X509 Certificate (public key)

    Returns:
        str | bytes: message from verified source
    """
    verified = verifySignature(*extract(signed_message), cert)
    if verified:
        message = extract(signed_message)[0]
        return message
    else:
        print("Invalid signature!")
        return None


    
def test():
    # Define the message to be signed
    msg = json.dumps({
        'timeStamp': "",
        'stationFullname': 'Pasila asema',
        'schedule': [
        {
            'IC11': [
            {
                'trainNumber': 11,
                'trainType': 'IC',
                'trainCategory': 'Long-distance',
                'commuterLineID': '',
                'timetable': [
                {
                    'destination': 'Joensuu asema',
                    'type': 'DEPARTURE',
                    'cancelled': False,
                    'scheduledTime': '2023-04-03T15:35:00.000Z',
                    'differenceInMinutes': None,
                    'liveEstimateTime': None,
                    'commercialTrack': '4',
                    'trainStopping': True,
                    'cause': None,
                    'stop_on_stations': [
                    'Käpylä',
                    'Oulunkylä',
                    'Pukinmäki'
                    ]}]}]}]})


    cert, key = keygen()

    signed = signMessage(msg, key)
    print(signed)

    signature, message = extract(signed)

    print("verified", verifySignature(signature, message, cert))



