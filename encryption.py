
import base64
from Crypto.Cipher import AES
from os import environ
import re

key = environ['KEY']
iv = environ['IV']


def decode(inputText):
    keyBytes = bytes.fromhex(key)  
    ivBytes = bytes.fromhex(iv)
    aes = AES.new(keyBytes, AES.MODE_CBC, ivBytes)
    result = aes.decrypt(base64.b64decode(inputText)).decode("utf-8", errors='ignore')
    result = re.sub(r'[^\x00-\x7f]',r'', result).strip().rstrip('\x0f')
    result = result.replace("\u0003",'').replace("\u0002",'').replace("\u0010",'').replace('\x0e', '')
    return result