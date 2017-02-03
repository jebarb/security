#!/usr/bin/python3
import fileinput
import hashlib
import copy
import re
import random


hashin = "littlehash"
seedin = "smallin.txt"
yours = set([line.rstrip('\n') for line in fileinput.input(hashin)])
goal = len(yours)


def main():
    for i in yours:
        print(i)
    while True:  # build new dict
        string = ''
        for c in range(0, 8):
            string = ''.join([string, chr(random.randint(32, 128))])
        if hashlib.sha1(string.encode('utf-8')).hexdigest() in yours:
            print(string)
            return

main()
