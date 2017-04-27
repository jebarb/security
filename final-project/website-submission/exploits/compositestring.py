#!/usr/bin/python3
import hashlib
import sys

words = ['Foil',
         'foil',
         'Right',
         'right',
         'Hand',
         'hand',
         'Westborough',
         'westborough',
         'Mass',
         'mass',
         'Massachusets',
         'massachusets',
         'MA',
         'Fencing',
         'fencing',
         'UNC']
endings = ['5',
           '7',
           '57',
           '2013',
           '2014',
           '13',
           '14']
uname = 'drdesai'
passhash = 'db5dba470848fff60c31a329285149d6'


def hashit(line):
    md51 = hashlib.md5(line.encode('utf-8')).hexdigest()
    sha1 = hashlib.sha1((uname + str(md51)).encode('utf-8')).hexdigest()
    hashed = hashlib.md5((uname + str(sha1)).encode('utf-8')).hexdigest()
    if hashed == passhash:
        print(uname + " " + line)
        sys.exit(0)


for word in words:
    for end in endings:
        hashit(''.join([word, end]))
        for word2 in words:
            hashit(''.join([word, word2, end]))
            for word3 in words:
                hashit(''.join([word, word2, word3, end]))
