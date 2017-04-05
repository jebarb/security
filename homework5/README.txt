README: 

MAKE findkey:

  gcc findkey.c -o findkey -lssl3 -lcrypto -lssl

I ran 'findkey' with this command:
  
  $ ./findkey /playpen/crypto/aes1.enc aes1.msg
  decafbad

We found the seed to be ``

  $ cat aes1.msg
  Correct...snip...