#include <stdlib.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
//shamelessly taken from http://stackoverflow.com/questions/1024389/print-an-int-in-binary-representation-using-c


char * int2bin(uint32_t i) {
  size_t bits = sizeof(uint32_t) * CHAR_BIT;
  char * str = malloc(bits + 1);
  if(!str) return NULL;
  str[bits] = 0;
  // type punning because signed shift is implementation-defined
  unsigned u = *(unsigned *)&i;
  for(; bits--; u >>= 1)
	str[bits] = u & 1 ? '1' : '0';
  return str;
}


uint32_t OurSubhashFunction(const uint8_t *key, size_t len) {
  char * result;
  uint32_t h = 535590091; // class ID (535/590-091)
  for (size_t i = 0; i < len; i++){
    // modify the hashing function here
    h ^= (uint32_t)key[i] << 8*(i % 4);
    result =  int2bin(h);
    printf("Round:%lu hash: %s value=%u \n", i, result,h);
    free(result);
  }
  return h;
}

int main(int argc, char ** argv) {
  if(argc <2) {
		  printf("Usage : %s key\n", argv[0]);
		  exit(-1);
  }
  OurSubhashFunction((uint8_t *)argv[1],strlen(argv[1]));
}

