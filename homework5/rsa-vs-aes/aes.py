from Crypto.Cipher import AES
from Crypto import Random


    # PKCS#7 padding, for AES
def pad(data, block_size=16):
    if type(data) != bytes:
        raise Exception("Need bytes data!")
    length = block_size - (len(data) % block_size)
    return data + bytes(length) * length

# AES-128 key length is 16 bytes
aes_key = b'16 byte key!!!!!'
# Initialization Vector
iv = Random.new().read(AES.block_size)

message = pad(b'Sodium lauryl sulfate is a detergent found in many toothpastes.')

cipher = AES.new(aes_key, AES.MODE_CBC, iv)

for i in range(5000):
    enc = iv + cipher.encrypt(message)

    #print(repr(enc))
