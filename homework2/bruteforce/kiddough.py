import fileinput
import hashlib
import copy


num_hashes = 0
matches = 0
notmine = []
for line in fileinput.input("hash.in"):
    notmine.append(line.rstrip('\n'))
yours = set(notmine)


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
        'x': ['x', 'X'],
        'y': ['y', 'Y', 'u'],
        'z': ['z', 'Z']
        }

for i in range(97, 122):
    tf[chr(i)] = tf[chr(i)][:1]

found = copy.deepcopy(tf)


def transform_string(string, buf, idx):
    global matches
    global num_hashes
    global yours
    global tf
    for c in tf[string[idx].lower()]:
        if idx == 7:
            num_hashes += 1
            if hashlib.sha1(''.join([buf, c]).encode('utf-8')).hexdigest() \
                    in yours:
                        matches += 1
        else:
            transform_string(string, ''.join([buf, c]), idx+1)


def process_file():
    for line in fileinput.input("input.txt"):
        line = line.split()
        mnemonic = ''
        for word in line:
            word = word.lstrip('_-,.?"\'')
            mnemonic = ''.join([mnemonic, word[0]])
            if len(mnemonic) == 8:
                break
        if len(mnemonic) < 8:
            continue
        transform_string(mnemonic, '', 0)


def main():
    global yours
    global num_hashes
    global matches
    global tf
    global found
    process_file()
    base_percent = matches/len(yours)*100
    letter = 'a'
    char = '!'
    new_percent = 0.0
    while True:
        matches = 0
        num_hashes = 0
        if char not in tf[letter]:
            tf[letter].append(char)
            process_file()
            new_percent = matches/len(yours)*100
            # if new_percent <= prev_percent:
            tf[letter].pop()
            # else:
            if new_percent > base_percent:
                found[letter].append(char)
                print("Letter: " + letter)
                print("  Char: " + char)
        char = chr(ord(char) + 1)
        if ord(char) > 126:
            char = '!'
            letter = chr(ord(letter) + 1)
            if ord(letter) > 122:
                matches = 0
                num_hashes = 0
                tf = copy.deepcopy(found)
                process_file()
                new_percent = matches/len(yours)*100
                print("\nGiven hashes:       " + str(len(yours)))
                print("Calculated hashes:  " + str(num_hashes))
                print("Matches:            " + str(matches))
                print("Hit percentage:     " + str(int(new_percent)) + "\n")
                for ltr, val in tf.items():
                    print("'" + ltr + "': [", end="")
                    for ltr2 in val:
                        print("'" + ltr2, end="', ")
                    print("],")
                return


main()
