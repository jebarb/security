#!/usr/bin/python3
import fileinput
import hashlib
import sys

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
for uname, sha1 in tocrack.items():
    if hashlib.sha1(''.join(['y!:', uname, ':', 'ELEMENTS'])
                    .encode('utf-8')).hexdigest() == sha1:
        print(uname + ':' + 'ELEMENTS')
for line in fileinput.input(0):
    line = line.rstrip('\n').upper()
    found = []
    for uname, sha1 in tocrack.items():
        if hashlib.sha1(''.join(['y!:', uname, ':',  line])
                        .encode('utf-8')).hexdigest() == sha1:
            print(uname + ':' + line)
            found.append(uname)
    for i in found:
        del tocrack[i]
    if len(tocrack) == 0:
        print('All passwords cracked')
        break

print("done")
