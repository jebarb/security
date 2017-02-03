/* Copyright (c) 2013, UNC Chapel Hill. All rights reserved.
 * Author: Andrew M. White
 *
 * Demonstration of how to work with binary files and hex representations.
 *
 */

#include <stdint.h>   // typedefs (e.g., uint8_t)
#include <stdio.h>    // printf, fopen/close

void print_hex(uint8_t *buffer, size_t num_bytes) {
  fprintf(stderr, "read buffer of size %lu\n", num_bytes);
  for (size_t i = 0; i < num_bytes; i++) {
    /*
     * print each byte in hexidecimal to stdout (see "man 3 printf")
     * conversion specifier 'x': unsigned hex (lower-case; X for uppercase)
     * field width 02: force two places (zero in the left column if < 128)
     */
    printf("%02x",(unsigned char)  buffer[i]);
  }
  printf("\n");
}

int bitwise_xor(FILE *f, FILE *g) {
  // your implementation here
  const size_t buffer_size = 30;
  int charf, charg;
  size_t size = 0;
  uint8_t xored[buffer_size];

  while ((charf = fgetc(f)) != EOF && (charg = fgetc(g)) != EOF) {
    xored[size] = charf^charg;
    size++;
  }
  print_hex(xored, size);
  return 0;
}

int main(int argc, char *argv[]) {

  if (argc != 3) {
    printf("usage: %s <filename> <filename>\n", argv[0]);
    printf("  filenames: binary files to read\n");
    return 1;
  }

  FILE *f = fopen(argv[1], "rb");
  FILE *g = fopen(argv[2], "rb");

  if ((f == NULL) || (g == NULL)) {
    fprintf(stderr, "error opening file %s\n", (f == NULL) ? argv[1] : argv[2]);
    return 1;
  } else {
    fprintf(stderr, "opened files %s and %s\n", argv[1], argv[2]);
  }

  int retval = bitwise_xor(f, g);

  fclose(f);    // always close opened files
  fclose(g);    // always close opened files

  if (retval > 0) {
    fprintf(stderr, "error reading file(s)\n");
    return 1;
  }

  return 0;
}
