import fileinput


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


def transform_string(string, buf, idx):
    for c in tf[string[idx].lower()]:
        if idx == 7:
            print(''.join([buf, c]))
        else:
            transform_string(string, ''.join([buf, c]), idx+1)


def process_file():  # process input and output
    for line in fileinput.input():
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


process_file()
