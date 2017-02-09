#!/usr/bin/python3
import fileinput
import hashlib
import re
import random
import copy


hashin = "/playpen/passwords_part2/mnemonic_hashes"
seeds = ["/playpen/passwords_part2/texts/artofwar.txt",
         "/playpen/passwords_part2/texts/theraven.txt"]
matched = False
yours = set([line.rstrip('\n') for line in fileinput.input(hashin)])
inputs = []
tf = {}
for i in range(97, 123):  # initilize dict of char: [char]
    tf[chr(i)] = [chr(i)]


def transform_string(s, buf, idx):  # does stuff
    global matched, yours, tf
    for c in tf[s[idx]]:
        if idx == 7:
            res = ''.join([buf, c])
            try:
                yours.remove(hashlib.sha1(res.encode('utf-8')).hexdigest())
                matched = True
            except:
                pass
        else:
            transform_string(s, ''.join([buf, c]), idx+1)


def process_mnemons(char):  # also does stuff
    global inputs, yours, matched
    matched = False
    for string in inputs:
        if char == '' or char in string:
            transform_string(string, '', 0)


def main():
    global yours, tf, matched
    found = copy.deepcopy(tf)  # for to save the good chars
    for seed in seeds:  # process seed files into mnemnonmics
        for line in fileinput.input(seed):
            if re.match("^\s*$", line):
                continue
            line = re.split("[^'a-zA-Z]+", line)
            mnemonic = ''
            for word in line:
                word = word.lstrip("'")
                if len(word) == 0:
                    continue
                mnemonic = ''.join([mnemonic, word[0].lower()])
                if len(mnemonic) == 8:
                    break
            if len(mnemonic) < 8:
                continue
            inputs.append(mnemonic)
    count = 0
    while True:  # build new dict
        count += 1
        if count % 30 == 0:  # expensive operation, limit completion check
            tf = copy.deepcopy(found)
            process_mnemons('')
            matched = False
        if len(yours) == 0:  # DONE!
            for i in tf.items():
                print(i)
            return
        for c in tf:  # take a random sample of substitutions
            offset = random.randint(0, len(found[c])-1)
            tf[c] = found[c][offset:offset+1]
        letter = 'a'
        char = '!'  # first printable non-whitespace asky car
        while True:  # test substitutions
            if char not in found[letter]:  # oh, this is new
                tf[letter] = char
                process_mnemons(letter)
                if matched:  # and it's a valid substitution (probably)
                    found[letter].append(char)
            char = chr(ord(char) + 1)
            if ord(char) > 126:  # move on to next letter
                tf[letter] = letter
                char = '!'  # still the first askie chair
                letter = chr(ord(letter) + 1)
                if ord(letter) > 122:  # reached z
                    break


main()
