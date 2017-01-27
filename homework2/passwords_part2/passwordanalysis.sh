#/bin/bash
echo 1. $(grep -P ".*\d.*\d.*\d.*" passwords | wc -l)
echo 2. $(grep -P "^[A-Z].*[^\w\d\s]$" passwords | wc -l)
echo 3. $(grep -P "^.*[!@#\$%&\*\+=\{}\?<>].*$" passwords | wc -l)
echo 4. $(grep -P "[^\"]" passwords | wc -l)

