#!/usr/bin/python3
import hashlib


def process_file():  # process input and output
    expected = "904ea074572894b0977d9f922f34343967d3ff9f"
    user = "whoami"
    pword = "$un-7uzu"
    for s1 in range(32, 127):
        for s2 in range(32, 127):
            salt = ''.join([chr(s1), chr(s2), ":", user, ":", pword])
            res = hashlib.sha1(salt.encode('utf-8')).hexdigest()
            if res == expected:
                print(salt)
                print(res)
                return


process_file()
