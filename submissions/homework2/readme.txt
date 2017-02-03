a)
  1. Strongly agree
  2. Agree
  3. Agree
  4. Agree
b) 411 and 530, solely for command line usage
   410 or 550, for runtime effeciency/understanding of data strucuters
c) I felt thoroughly prepared
d) Online password cracking for the composite string. Felt like I had no idea
   which direction to go in
e) Copied from respective readmes:
  1:
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
    a minute or two. The program is in the mneminic directory. To run it, in
    the mnemonic folder, use:

      ./bruteforce-kiddough.py.

    To run my kiddough, use the following:

      (
      ./kiddough /playpen/passwords_part2/texts/artofwar.txt;
      ./kiddough /playpen/passwords_part2/texts/theraven.txt
      ) > kiddough.out

    To run my checker, use the following:

      ./generate-check.sh


  2:
    # Online password cracking
    The first password was trivial to find. I wrote the script fooCracker, then
    wrote another script to run the correct command to get one of the passwords 
    which gave me the daily password in a couple of minutes. To run, in the
    online folder, use:

      ./get-daily-pass.sh

    The master password was much more difficult. I basically attempted permutations
    of every noteworthy string on Jan's google+ page, kept trying different cases,
    different representations, etc. I ended up switching over to a different
    method.

    I began researching ways to do a hex dump of an executable that doesn't have 
    read permissions by dumping the memory it's stored in. I found some utilities
    that use ptrace to find the elf header of an executable in memory, then dump
    the following memory segment. This turned out to be ineffective. One of the
    utilities I found wouldn't compile on the VM, one couldn't find the ELF, the
    other just dumped a sign extended -1. I assume this is because the setuid bit
    is set, which is known to make these utilities very unhappy.

    About five years later and after a fair amount of time spent in office hours, I 
    finally got my script to output the correct master pass by using a slightly
    different strategy using a larger set of strings combined in a more reasonable
    manner. To run, in the online folder, use:

      ./get-master-pass.sh


  3:
    # Salted hashed passwords
    This one didn't really take much effort. After fixing an incorrect string
    concatenation in my findsalt script, it quickly found the salt, hence the name
    I guess. To run, in the online folder, use:

      ./run-findsalt

    For the second part, it was pretty similar. After remembering to remove
    trailing newline characters, it quickly cracked a number of salted passwords.
    To run, in the online folder, use:

      ./yahoocrack /playpen/passwords_part2/yahoo_hashes


f) roughly 15 hours

To run all scripts back to back, use ./runall.sh

