x86 and C:

I've only had experience with MIPS, so I first searched for a good x86 quick
start guide [1]. After reading up on calling conventions, registers, syntax,
etc., I started on the first task, using the wikipedia page on CPUID [2] as
a reference. The first two tasks went smoothly, but I had difficulty with the
third task. I wasn't able to XOR with keys larger than 127, but it turns out
the issue was a bug in the tast code. The key was being cast to a char when it
should have been cast to an unsigned char.

The final task ended up being easier than the third for me. I just looked up
documentation for dirent.h and everything went smoothly from there forward.


Forensics:

To start, I used instructions found on a website on RAM analysis [3] to create 
a memory dump. I then utilized a volatility cheatsheet [4] to find the correct 
registry entry. Initially, I had trouble logging in, but it turned out there 
was a typo in the password. I downloaded the updated VM image and used a hacky 
script I made as I extracted the password several times while trying to 
diagnose the issue (extractpass.sh in homework1 folder). While playing around
with the script, I noticed that sometimes the registry entry would not show up,
with or without use of the script. Since the VM takes so long to boot, I didn't
attempt to diagnose the problem, but it seems to be related to uptime before
dumping the memory.

For the next exercise, I first got the dump off the VM because I'm currently 
using a weak laptop that doesn't have much memory. I then looked through 
the volatility commands and found the 'cmdscan' option which gave me the 
location of 'Elliot.exe' which I ran as instructed.


[1] https://www.cs.virginia.edu/~evans/cs216/guides/x86.html
[2] https://en.wikipedia.org/wiki/CPUID
[3] http://wiki.yobi.be/wiki/RAM_analysis
[4] http://downloads.volatilityfoundation.org/releases/2.4/CheatSheet_v2.4.pdf
