#!/usr/bin/python3
import fileinput
import hashlib
import copy
import re
import random


hashin = "bighash"
match = False
seedin = "input.txt"
yours = set([line.rstrip('\n') for line in fileinput.input(hashin)])
goal = len(yours)
inputs = []
tf = {
        'a': ['a', '&', '*', '4', '@', 'A', 'v'],
        'b': ['b', '8', 'B', '<'],
        'c': ['c', 'C'],
        'd': ['d', 'D'],
        'e': ['e', '3', 'E'],
        'f': ['f', '<', 'F'],
        'g': ['g', 'G', '`'],
        'h': ['h', 'H'],
        'i': ['i', '1', '=', '>', '?', 'I'],
        'j': ['j', 'J'],
        'k': ['k', 'K'],
        'l': ['l', '1', 'L', '~'],
        'm': ['m', 'M'],
        'n': ['n', '!', 'N'],
        'o': ['o', '0', 'O', '|', '1'],
        'p': ['p', 'P'],
        'q': ['q', 'Q'],
        'r': ['r', 'R'],
        's': ['s', '$', '5', 'S', 'c'],
        't': ['t', '2', '7', 'T'],
        'u': ['u', 'U'],
        'v': ['v', 'V'],
        'w': ['w', 'W'],
        'x': ['x'],
        'y': ['y', 'Y', 'u'],
        'z': ['z'],
        }


def transform_string(string, buf, idx, mine):
    global yours, tf, match
    for c in tf[string[idx]]:
        if idx == 7:
            if hashlib.sha1(''.join([buf, c]).encode('utf-8')).hexdigest() in mine:
                match = True
        else:
            transform_string(string, ''.join([buf, c]), idx+1, mine)


def process_file():
    global inputs, seedin
    for line in fileinput.input(seedin):
        line = re.sub('[^a-zA-Z]+', ' ', line)
        line = line.split()
        mnemonic = ''
        for word in line:
            if word == '':
                continue
            mnemonic = ''.join([mnemonic, word[0].lower()])
            if len(mnemonic) == 8:
                break
        if len(mnemonic) < 8:
            continue
        inputs.append(mnemonic)


def process_inputs():
    global inputs
    mine = {}
    for string in inputs:
        transform_string(string, '', 0, mine)


def print_results():
    print("Result dict:")
    for ltr, val in tf.items():
        print("'" + ltr + "': ", end="")
        print(val, end="")
        print(",")


def main():
    global match, tf
    process_file()
    while True:  # build new dict
        for c in tf:
            tf[c] = chr(random.randint(32, 128))
        process_inputs()
        if match:
            print_results()
            return


main()
