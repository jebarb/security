#!/usr/bin/python3
import fileinput
import hashlib
import copy
import re
import random


hashin = "hash.in"
seedin = "input.txt"
num_hashes = 0
matches = 0
speed = 1
yours = [line.rstrip('\n') for line in fileinput.input(hashin)]
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
        't': ['t', '2', '7', 'T', '8', 'B', 'b'],
        'u': ['u', 'U'],
        'v': ['v', 'V'],
        'w': ['w', 'W'],
        'x': ['x'],
        'y': ['y', 'Y', 'u'],
        'z': ['z'],
        }
#for i in range(97, 123):  # empty predefined subs
#    tf[chr(i)] = tf[chr(i)][:speed]
found = copy.deepcopy(tf)
orig = copy.deepcopy(tf)


def transform_string(string, buf, idx, mine):
    global matches, num_hashes, yours, tf
    for c in tf[string[idx]]:
        if idx == 7:
            num_hashes += 1
            mine[hashlib.sha1(
                ''.join([buf, c]).encode('utf-8')).hexdigest()] = ''
        else:
            transform_string(string, ''.join([buf, c]), idx+1, mine)


def process_file():
    global matches, inputs
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
    global inputs, matches, yours
    mine = {}
    for string in inputs:
        transform_string(string, '', 0, mine)
    for i in yours:
        if i in mine:
            matches += 1


def print_results():
    new_percent = matches/goal*100
    for ltr, val in tf.items():
        print("'" + ltr + "': ", end="")
        print(val, end="")
        print(",")
    print("")
    print("\nGiven hashes:       " + str(goal))
    print("Calculated hashes:  " + str(num_hashes))
    print("Matches:            " + str(matches))
    print("Coverage:           " + str(int(new_percent)) + "%\n")
    print("Result dict:")


def main():
    global yours, num_hashes, matches, tf, speed, found, orig
    offset = 0
    process_file()
    while True:  # build new dict
        num_hashes = 0
        matches = 0
        new_char = False
        for c in tf:
            if len(tf[c]) > speed:
                offset = random.randint(0, len(tf[c])-speed)
                tf[c] = tf[c][offset:offset+speed]
        process_inputs()
        base_percent = matches/goal*100
        letter = 'a'
        char = '!'
        new_percent = 0.0
        while True:  # test substitutions
            num_hashes = 0
            matches = 0
            if char not in tf[letter]:  # save good subs
                tf[letter].append(char)
                process_inputs()
                new_percent = matches/goal*100
                if new_percent > base_percent and char not in found[letter]:
                    new_char = True
                    found[letter].append(char)
                    print("  Letter, substitution: " + letter + ", " + char)
                tf[letter].pop()
            char = chr(ord(char) + 1)
            if ord(char) > 126:  # move on to next letter
                char = '!'
                letter = chr(ord(letter) + 1)
                if ord(letter) > 122:  # reached z
                    num_hashes = 0
                    matches = 0
                    tf = copy.deepcopy(found)
                    if new_char:
                        process_inputs()
                        if print_results() == 100:
                            print("SUCCESS!!")
                            return
                    break


main()
