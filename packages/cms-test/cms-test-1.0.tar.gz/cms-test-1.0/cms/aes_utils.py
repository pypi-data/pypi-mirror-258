import base64
from Crypto.Cipher import AES

BS = 16
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def aes_decrypt(value):
    iv = b'encryptionIntVec'
    key = b'aesEncryptionKey'
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(base64.b64decode(value)).decode())

def decrypt(value, typ: str):
    if typ.upper() == 'AES':
        return aes_decrypt(value)
    else:
        raise Exception('Invalid encryption type!')