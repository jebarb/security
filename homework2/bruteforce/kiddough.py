import fileinput
import hashlib


tf = {
        'a': ['a', 'A', '4', '@', '&'],
        'b': ['b', 'B', '8'],
        'c': ['c', 'C'],
        'd': ['d', 'D'],
        'e': ['e', 'E', '3'],
        'f': ['f', 'F'],
        'g': ['g', 'G'],
        'h': ['h', 'H'],
        'i': ['i', 'I', '1'],
        'j': ['j', 'J'],
        'k': ['k', 'K'],
        'l': ['l', 'L', '1'],
        'm': ['m', 'M'],
        'n': ['n', 'N'],
        'o': ['o', 'O', '0'],
        'p': ['p', 'P'],
        'q': ['q', 'Q'],
        'r': ['r', 'R'],
        's': ['s', 'S', '5', '$'],
        't': ['t', 'T'],
        'u': ['u', 'U'],
        'v': ['v', 'V'],
        'w': ['w', 'W'],
        'x': ['x', 'X'],
        'y': ['y', 'Y'],
        'z': ['z', 'Z']
        }


def transform_string(string, buf, idx, out):
    for c in tf[string[idx].lower()]:
        if idx == 7:
            out.write(''.join([buf, c]))
        else:
            transform_string(string, ''.join([buf, c]), idx+1, out)
    out.close()


def process_hashes():
    yours = {}
    for line in fileinput.input("hash.in"):
        yours[line.rstrip('\n')] = line.rstrip('\n')
    matches = 0
    for f in fileinput.input("hash.out"):
        if hashlib.sha1(f.rstrip('\n').encode("utf-8")).hexdigest() in yours:
            matches += 1
    res = open("results.txt")
    res.write("Number of given hashes: " + str(len(yours)))
    res.write("Number of matches:      " + str(matches))
    res.write("Hit percentage:         " + str(matches/len(yours)*100) + "%\n")
    res.write('')
    return matches/len(yours)*100


def process_file():  # process input and output
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
        transform_string(mnemonic, '', 0, open("hash.out", 'w'))


def main():
    process_file()
    prev_percent = process_hashes()
    letter = 'a'
    char = '!'
    prev_percent = 0.0
    new_percent = 0.0
    while True:
        tf[letter].append(char)
        process_file()
        new_percent = process_hashes()
        if new_percent <= prev_percent:
            tf[letter].pop()
        else:
            print("Letter: " + letter)
            print("Char: " + char)
            print("Hit percentage: " + str(new_percent))
            prev_percent = new_percent
        if char > 126:
            char = ' '
            letter += letter
            if letter > 122:
                return


main()
