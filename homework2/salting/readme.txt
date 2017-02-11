# Salted hashed passwords
This one didn't really take much effort. After fixing an incorrect string
concatenation in my findsalt script, it quickly found the salt, hence the name
I guess. To run, use:
  
  ./run-findsalt

For the second part, it was pretty similar. After remembering to remove
trailing newline characters, it quickly cracked a number of salted passwords.
To run, use:

  ./yahoocrack /playpen/passwords_part2/yahoo_hashes
