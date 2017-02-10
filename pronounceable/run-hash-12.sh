#!/bin/bash
(
cat 12char-cracked.txt | cut -d ":" -f 2
while [ 1 ]; do 
  gpw 100000 8
  gpw 100000 9
  gpw 100000 10
  gpw 100000 11
  gpw 100000 12
done
) | ./hashit.py pronounceable_8-12_salted 12char-cracked.txt
