#!/usr/bin/python3
import fileinput
import hashlib
import sys

filein = open(sys.argv[1])
fileout = open(sys.argv[2], 'w')
tocrack = {}
for line in filein:
    line = line.rstrip('\n')
    line = line.split(':')
    if len(line) != 2:
        continue
    uname = line[0]
    sha1 = line[1]
    tocrack[line[0]] = line[1]
for line in fileinput.input(0):
    line = line.rstrip('\n')
    found = []
    for uname, sha1 in tocrack.items():
        if hashlib.sha1(''.join(['y!:', uname, ':',  line])
                        .encode('utf-8')).hexdigest() == sha1:
            print(uname + ':' + line, file=fileout, flush=True)
            found.append(uname)
    for i in found:
        del tocrack[i]
    if len(tocrack) == 0:
        print('All passwords cracked', flush=True)
        break

