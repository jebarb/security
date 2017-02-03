#!/usr/bin/python3
import fileinput
import re

pwords = []

# for i in range(97, 123):  # empty predefined subs
#     tf[chr(i)] = tf[chr(i)][:1]


def transform_string(string, buf, idx):
    for c in tf[string[idx].lower()]:
        if idx == 7:
            pwords.append(''.join([buf, c]))
        else:
            transform_string(string, ''.join([buf, c]), idx+1)


def process_file():  # process input and output
    for line in fileinput.input():
        line = re.sub('[^a-zA-Z]+', ' ', line)
        line = line.split()
        mnemonic = ''
        for word in line:
            if word == '':
                continue
            mnemonic = ''.join([mnemonic, str(len(word))])
            if len(mnemonic) == 8:
                break
        if len(mnemonic) < 8:
            continue
        print(mnemonic)
        #transform_string(mnemonic, '', 0)
    for i in pwords:
        print(i)


process_file()
