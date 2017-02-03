#!/usr/bin/python3
import fileinput
import re


tf = {
        'a': ['a', 'A', '&', '*', '4', '@', 'v'],
        'b': ['b', 'B', '8', '<'],
        'c': ['c', 'C'],
        'd': ['d', 'D'],
        'e': ['e', 'E', '3'],
        'f': ['f', 'F', '<'],
        'g': ['g', 'G', '`'],
        'h': ['h', 'H'],
        'i': ['i', 'I', '1', '=', '>', '?'],
        'j': ['j', 'J'],
        'k': ['k', 'K'],
        'l': ['l', 'L', '1', '~'],
        'm': ['m', 'M'],
        'n': ['n', 'N', '!'],
        'o': ['o', 'O', '0', '1', '|'],
        'p': ['p', 'P'],
        'q': ['q', 'Q'],
        'r': ['r', 'R'],
        's': ['s', 'S', '$', '5', 'c'],
        't': ['t', 'T', '2', '7', '8', 'B', 'b'],
        'u': ['u', 'U'],
        'v': ['v', 'V'],
        'w': ['w', 'W'],
        'x': ['x'],
        'y': ['y', 'Y', 'u'],
        'z': ['z']
        }

pwords = []


def transform_string(string, buf, idx):
    for c in tf[string[idx].lower()]:
        if idx == 7:
            pwords.append(''.join([buf, c]))
        else:
            transform_string(string, ''.join([buf, c]), idx+1)


def process_file():  # process input and output
    transform_string("yosemite", '', 0)
    for i in pwords:
        print(i)


process_file()
