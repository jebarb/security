README: 

MAKE findkey:

  gcc findkey.c -o findkey -lssl3 -lcrypto -lssl

We ran 'findkey' with this command:
  
  $ ./findkey /playpen/crypto/aes3.enc aes3.msg
  59186fef

We found the seed to be `59186fef`

  $ cat aes3.msg
  Correct: Congratulations to all graduating seniors!

We also found the seed for:
  /playpen/crypto/aes4.enc to be `5abbee82`
  /playpen/crypto/aes1.enc to be `58776824`

OUR APPROACH:

  Our approach was to begin searching at the current
  time, iterating over the 16 lower bits, and branching in 
  both directions from there.

Challenges:
  
  Our biggest challenge was finding out what we needed to do.
  Once we had a goal, the total assignement took about 2.5 hours
  to complete.
