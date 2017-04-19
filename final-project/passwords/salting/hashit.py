#!/usr/bin/python3
import fileinput
import hashlib
import sys
import binascii

#format: python hashit.py testuser < testpass

filein = open(sys.argv[1])
tocrack = {}
for line in filein:
    line = line.rstrip('\n')
    line = line.split(' ')
    if len(line) != 2:
        continue
    uname = line[1]
    sha1 = line[0]
    tocrack[uname] = sha1
for line in fileinput.input(0):
    line = line.rstrip('\n')
    found = []
    for uname, sha1 in tocrack.items():
        temp = hashlib.md5(uname + hashlib.sha1(uname + hashlib.md5(line).hexdigest()).hexdigest()).hexdigest()
        #print(temp)
        if temp == sha1:
            print(uname + " " + line)
            found.append(uname)
    for i in found:
        del tocrack[i]
    if len(tocrack) == 0:
        print("All passwords cracked")
        break

print("done")
