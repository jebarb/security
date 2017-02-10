#!/bin/bash
(
cat 8char-cracked.txt | cut -d ":" -f 2
while [ 1 ]; do
  gpw 1000000 8
  #pwgen -c -0 -1 -N 100
  #python2 passogva-1.0/passogva.py
done
) | ./hashit.py pronounceable_8-salted 8char-cracked.txt
