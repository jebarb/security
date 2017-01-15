/* Copyright (c) 2013, UNC Chapel Hill. All rights reserved.
 * Author: Andrew M. White
 *
 * Demonstration of how to work with binary files and hex representations.
 *
 */

#include <stdint.h>   // typedefs (e.g., uint8_t)
#include <stdio.h>    // printf, fopen/close

void print_hex(uint8_t *buffer, size_t num_bytes) {
  /*
   * function to print an array of bytes in hexademical notiation 
   * outputs on stdout, one line per call 
   * hint: see "man 3 printf"
   *
   * uint8_t *buffer: array of bytes
   * size_t num_bytes: number of bytes to print from array
   */

  //
  // INSERT YOUR CODE HERE
  //
  int i;
  for (i = num_bytes + 1; i > 0; --i) {
    printf("%x", buffer[num_bytes - i]);
  }
}

int bin2hex(FILE *f) {
  /*  
   * function to read from stream in n-byte chunks
   * * generally faster than byte-at-a-time)
   * * do not have to know how long the file is
   * * do not have to buffer more than n bytes in memory
   *
   * FILE *f: pointer to open FILE stream
   */ 

  // const to avoid dynamic memory allocation
  const size_t buffer_size = 30;

  // uint8_t: single unsigned byte
  uint8_t buffer[buffer_size];

  size_t bytes_read; 
  do { 
    // read up to buffer_size bytes from file
    bytes_read = fread((void *)&buffer, sizeof(uint8_t), buffer_size, f);

    // bytes_read: # bytes actually read this round
    fprintf(stderr, "read buffer of size %lu\n", bytes_read);

    // bail out if we hit the end of the file
    if(bytes_read == 0) break;

    // print the current buffer in hex
    print_hex(buffer, bytes_read);
  } while (bytes_read == buffer_size);

  // reading less than the buffer size MAY be an I/O error
  if (ferror(f)) {
    perror("error reading input file");
    return 1;
  }

  return 0;
}

int main(int argc, char *argv[]) {
  /* 
   *  argc: # of command line arguments
   *  argv: array of command-line arguments
   *  each accounts for the name of the invoked program in argv[0]
   */
  if (argc != 2) {
    printf("usage: %s <filename>\n", argv[0]);
    printf("  filename: name of a binary file to read\n");
    return 1; 
  }

  // open the file for reading in binary mode
  FILE *f = fopen(argv[1], "rb");

  // check for errors opening the file
  if (f == NULL) {
    fprintf(stderr, "error opening file %s\n", argv[1]);
    return 1;
  } else {
    fprintf(stderr, "opened file %s\n", argv[1]);
  }

  // actually read in the bytes and print them out
  int retval = bin2hex(f);

  fclose(f);    // always close opened files

  // catch any errors from the read loop
  if (retval > 0) { 
    fprintf(stderr, "error reading file %s\n", argv[1]);
    return 1;
  }

  return 0;
}
