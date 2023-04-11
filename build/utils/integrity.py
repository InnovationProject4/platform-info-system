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
import json, hashlib, configparser, binascii

from OpenSSL.crypto import (
    TYPE_RSA,
    FILETYPE_PEM,
    FILETYPE_ASN1,
    FILETYPE_TEXT,
    Error,
    PKey,
    sign,
    verify,
    load_certificate,
    load_publickey,
    load_privatekey,
    X509,
    PKCS12,
    PKCS7
)


def keygen():
    """Generate RSA 2048 public-private pair with keylength of 2048

    Returns:
        cert, PKey: public X509 certificate, private-public pair
    """
    cert = X509()
    key = PKey()
    key.generate_key(TYPE_RSA, 2048)
    cert.set_pubkey(key)
    return cert, key


def signMessage(message, private_key):
    """Sign message using private SHA256 signature

    Args:
        message (str): message to digest
        private_key (PKey): cryptographic private-public pair

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

    #print("verified", verifySignature(signature, message, cert))
    
    
test()






