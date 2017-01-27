import fileinput


tf = {
        'a': ['a', 'A', '4', '@'],
        'b': ['b', 'B', '6', '8'],
        'c': ['c', 'C', '(', '['],
        'd': ['d', 'D', '6', ']', ')'],
        'e': ['e', 'E', '3'],
        'f': ['f', 'F', '#'],
        'g': ['g', 'G', '9'],
        'h': ['h', 'H', '#'],
        'i': ['i', 'I', '!', '1', 'l', 'j'],
        'j': ['j', 'J', 'i'],
        'k': ['k', 'K', '<'],
        'l': ['l', 'L', '1', '!', 'I', 'i'],
        'm': ['m', 'M'],
        'n': ['n', 'N'],
        'o': ['o', 'O', '0'],
        'p': ['p', 'P'],
        'q': ['q', 'Q', '9'],
        'r': ['r', 'R'],
        's': ['s', 'S', '5', '$'],
        't': ['t', 'T', '+'],
        'u': ['u', 'U'],
        'v': ['v', 'V', '<', '>'],
        'w': ['w', 'W'],
        'x': ['x', 'X', '%'],
        'y': ['y', 'Y', '?'],
        'z': ['z', 'Z', '2', '7']
        }


def transform_string(string):
    _transform_string(string, '', 0)


def _transform_string(string, buf, idx):
    char = tf[string[idx]]
    for c in char:
        if idx == 7:
            print(''.join([buf, c]))
        else:
            _transform_string(string, ''.join([buf, c]), idx+1)


def process_file():  # process input and output
    for line in fileinput.input():
        line = line.split()
        mnemonic = ''
        for word in line:
            for letter in word:
                if letter in tf:
                    mnemonic = ''.join([mnemonic, letter])
                    break
            if len(mnemonic) == 8:
                break
        if (len(mnemonic) < 8):
            continue
        transform_string(mnemonic)


process_file()
