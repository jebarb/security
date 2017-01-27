import fileinput
import sys
import hashlib


def process_hashes():
    if len(sys.argv) < 3:
        print("FEED ME MORE ARGUMENTS")
        return
    yours = {}
    for line in fileinput.input(sys.argv[2]):
        yours[line] = line
    matches = 0
    for line in fileinput.input(sys.argv[1]):
        if hashlib.sha1(line).hexdigest in yours:
            matches += 1
    print("Number of given hashes: " + str(len(yours)))
    print("Number of matches:      " + str(matches))
    print("Hit percentage:         " + str(matches/len(yours)*100) + "%")


process_hashes()
