Forensics:

To start, I used instructions found on a website on RAM analysis [1] to create 
a memory dump. I then utilized a volatility cheatsheet [2] to find the correct 
registry entry. Initially, I had trouble logging in, but it turned out there 
was a typo in the password. I downloaded the updated VM image and used a hacky 
script I made as I extracted the password several times while trying to 
diagnose the issue (extractpass.sh in homework1 folder), the output of which 
being: 'REG_SZ        Password        : (S) $t0inS@a'.

For the next exercise, I first got the dump off the VM because I'm currently 
using a weak laptop that can't seem to run a VM properly. I then looked through 
the volatility commands and found the 'cmdscan' option which gave me the 
location of 'Elliot.exe' which I ran as instructed, with the following output: 
C:\Windows\SoftwareDistribution\Download>Elliot.exe
Please provide your PID:720076615
Password for PID 720076615: 010607c0b3e67943

[1] http://wiki.yobi.be/wiki/RAM_analysis
[2] http://downloads.volatilityfoundation.org/releases/2.4/CheatSheet_v2.4.pdf
