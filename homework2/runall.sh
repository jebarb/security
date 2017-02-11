#!/bin/bash
(
./mnemonic/kiddough /playpen/passwords_part2/texts/artofwar.txt;
./mnemonic/kiddough /playpen/passwords_part2/texts/theraven.txt
) > mnemonic/kiddough.out
echo "Password generation complete"
mnemonic/match_hashes.py mnemonic/kiddough.out /playpen/passwords_part2/mnemonic_hashes
cat mnemonic/kiddough.out | ./online/fooCracker
./online/compositestring.py | ./online/fooCracker
./salting/findsalt whoami '$un-7uzu' 904ea074572894b0977d9f922f34343967d3ff9f
(
john --wordlist=salting/cracklib-small --stdout 2>/dev/null;
john --wordlist=/usr/share/dict/words --stdout 2>/dev/null;
john --wordlist=/usr/share/dict/words --rules --stdout 2>/dev/null;
john --wordlist --rules sony_pwdump --stdout 2>/dev/null;
john --markov sony_pwdump --stdout 2>/dev/null
) | ./salting/hashit.py /playpen/passwords_part2/yahoo_hashes

