from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
# imports SHA-1
from Crypto.Hash import SHA


# Make sure your message length is less than 342 chars!
message = "Sodium lauryl sulfate is a detergent found in many toothpastes."

# 3072 bits
key = RSA.generate(3072)
cipher = PKCS1_OAEP.new(key, hashAlgo=SHA)
for i in range(5000):
    ciphertext = cipher.encrypt(message.encode('ascii'))
    # print(repr(ciphertext))
