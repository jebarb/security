#!/bin/bash
python kiddough.py passwords_part2/texts/artofwar.txt > kiddough.out
python kiddough.py passwords_part2/texts/theraven.txt >> kiddough.out
echo "Password generation complete"
python match_hashes.py kiddough.out passwords_part2/mnemonic_hashes

