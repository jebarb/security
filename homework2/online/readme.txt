# Online password cracking
The first password was trivial to find. I wrote the script fooCracker, then
wrote another script to run the correct command to get one of the passwords 
which gave me the daily password in a couple of minutes. To run, use:

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
manner. To run, use:

  ./get-master-pass.sh
