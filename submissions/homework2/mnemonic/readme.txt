# Mnemonic password generation
I initially attempted to adhere to the assignment description. However, after
running my program the first time, I only saw a 40% hit rate. Annoyed, I
decided to think up an algorithm that would find the substitutions for me.

It's a pretty simple program. It first parses the seed files and stores the
monemonic line representations in a list. It builds a dict of the form
char:[char] for char in [a-z]. It stores the hashes to be matched in a set.

It then selects a random set of known substitutions (being only a-z at first),
then iterates through that set from start to end, for each letter trying out
one new character substitution at a time, attempting all printable non-
whitespace ascii characters. It builds a list of substituted mnemonic
passwords, hashes them, and checks them agains the given set of hashes. This 
runs in an infinite loop until a complete solution is found.

This method got me a 94% hit rate on the first run, and after a bit of tuning
and correction of input parsing, it can consistently find all substitutions in
a minute or two. The program is in the mneminic directory. To run it, use:

  ./bruteforce-kiddough.py.

To run my kiddough, use the following:

  (
  ./kiddough /playpen/passwords_part2/texts/artofwar.txt;
  ./kiddough /playpen/passwords_part2/texts/theraven.txt
  ) > kiddough.out

To run my checker, use the following:

  ./generate-check.sh
