
import base64
from Crypto.Cipher import AES
from os import environ
import re
import string

# When we decrypt our json response we get quite a lot of non-ascii characters.
# These need to be cleaned up so that we can load our json data without any errors.
# One way to do this is to filter out only printable characters, and so we define
# our printable set here:
printable = set(string.printable)

# We need to grab our decryption key and IV value from our environment - in our
# case this is on heroku
key = environ['KEY']
iv = environ['IV']

def fixJSON(jsonStr):
    '''Helper function to fix dirty or broken json'''
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
    '''Main decode function used to decode the public API json values on the Fantasy F1 API'''
    # Load our environment variables as bytes
    keyBytes = bytes.fromhex(key)  
    ivBytes = bytes.fromhex(iv)
    # Define encryption type and call our decryption function
    aes = AES.new(keyBytes, AES.MODE_CBC, ivBytes)
    result = aes.decrypt(base64.b64decode(inputText)).decode("utf-8", errors='ignore')

    # Now we need to fix our json string with a number of fixes, firstly 
    # with printable characters
    result = ''.join(filter(lambda x: x in printable, result))
    # Then remove other utf-8 characters 
    result = re.sub(r'[^\x00-\x7F]+',r' ', result).strip().rstrip('\x0f')
    result = result.replace("\u0003",'').replace("\u0002",'').replace("\u0010",'').replace('\x0e', '')
    # Lastly lets call our fixJson function to make sure that there are no
    # errors in the json string
    result = fixJSON(result)
    return result