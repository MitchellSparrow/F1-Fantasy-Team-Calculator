
import base64
from Crypto.Cipher import AES
from os import environ

key = environ['KEY']
iv = environ['IV']

def decode(inputText):
    keyBytes = bytes.fromhex(key)  
    ivBytes = bytes.fromhex(iv)
    aes = AES.new(keyBytes, AES.MODE_CBC, ivBytes)
    return aes.decrypt(base64.b64decode(inputText)).decode("utf-8") 


