#!/usr/bin/python3
import fileinput
import sys
import hashlib


def process_hashes():
    if len(sys.argv) < 3:
        print("FEED ME MORE ARGUMENTS")
        return
    mine = set([hashlib.sha1(line.rstrip('\n').encode("utf-8")).hexdigest()
            for line in fileinput.input(sys.argv[1])])
    matches = 0
    given = 0
    calculated = len(mine)
    for f in fileinput.input(sys.argv[2]):
        given += 1
        if f.rstrip('\n') in mine:
            matches += 1
    print("Number of given hashes:        " + str(given))
    print("Numbcer of calculated hashes:  " + str(len(mine)))
    print("Number of matches:             " + str(matches))
    print("Coverage:                      " + str(matches/given*100) + "%")


process_hashes()
