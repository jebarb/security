#!/bin/bash
(
./kiddough /playpen/passwords_part2/texts/artofwar.txt;
./kiddough /playpen/passwords_part2/texts/theraven.txt
) > kiddough.out

echo "Password generation complete"
./match_hashes.py kiddough.out /playpen/passwords_part2/mnemonic_hashes

