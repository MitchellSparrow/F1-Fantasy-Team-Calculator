
import base64
from Crypto.Cipher import AES
from os import environ
import re
import string

printable = set(string.printable)

key = environ['KEY']
iv = environ['IV']

def fixJSON(jsonStr):
    # First remove the " from where it is supposed to be.
    jsonStr = re.sub(r'\\', '', jsonStr)
    jsonStr = re.sub(r'{"', '{`', jsonStr)
    jsonStr = re.sub(r'"}', '`}', jsonStr)
    jsonStr = re.sub(r'":"', '`:`', jsonStr)
    jsonStr = re.sub(r'":', '`:', jsonStr)
    jsonStr = re.sub(r'","', '`,`', jsonStr)
    jsonStr = re.sub(r'",', '`,', jsonStr)
    jsonStr = re.sub(r',"', ',`', jsonStr)
    jsonStr = re.sub(r'\["', '\[`', jsonStr)
    jsonStr = re.sub(r'"\]', '`\]', jsonStr)

    # Remove all the unwanted " and replace with ' '
    jsonStr = re.sub(r'"',' ', jsonStr)

    # Put back all the " where it supposed to be.
    jsonStr = re.sub(r'\`','\"', jsonStr)

    return jsonStr

def decode(inputText):
    keyBytes = bytes.fromhex(key)  
    ivBytes = bytes.fromhex(iv)
    aes = AES.new(keyBytes, AES.MODE_CBC, ivBytes)
    result = aes.decrypt(base64.b64decode(inputText)).decode("utf-8", errors='ignore')
    result = ''.join(filter(lambda x: x in printable, result))
    result = re.sub(r'[^\x00-\x7F]+',r' ', result).strip().rstrip('\x0f')
    result = result.replace("\u0003",'').replace("\u0002",'').replace("\u0010",'').replace('\x0e', '')
    result = fixJSON(result)
    return result