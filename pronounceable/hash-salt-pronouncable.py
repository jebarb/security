#!/usr/bin/python3
import hashlib
import sys
import random


letters = list(map(chr, range(97, 123)))
vowels = ['a', 'e', 'i', 'o', 'u']
consonants = [letter for letter in letters if letter not in vowels]
filein = open(sys.argv[1])
tocrack = {}
for line in filein:
    line = line.rstrip('\n')
    line = line.split(':')
    if len(line) != 2:
        continue
    uname = line[0]
    sha1 = line[1]
    tocrack[line[0]] = line[1]


def generate_word():
    global letters, vowels, consonants
    res = ''
    cons = 0
    vow = 0
    for i in range(8):
        char = ''
        if cons == 2 or (len(res) in [1, 7] and cons == 1):
            cons = 0
            char = vowels[random.randint(0, len(vowels)-1)]
        elif vow == 2 or (len(res) in [1, 7] and vow == 1):
            vow = 0
            char = consonants[random.randint(0, len(consonants)-1)]
        else:
            char = letters[random.randint(0, len(letters)-1)]
        if char in vowels:
            vow += 1
        elif char in consonants:
            cons += 1
        res = ''.join([res, char])
    return res


while True:
    word = generate_word()
    found = []
    for uname, sha1 in tocrack.items():
        print(uname + ":" + sha1)
        if hashlib.sha1(''.join(["y!:", uname, ":",  word])
                        .encode('utf-8')).hexdigest() == sha1:
            print(uname + ":" + word)
            found.append(uname)
    for i in found:
        del tocrack[i]
    if len(tocrack) == 0:
        print("All passwords cracked")
        break

print("done")
