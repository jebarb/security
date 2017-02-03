/* Copyright (c) 2013, UNC Chapel Hill. All rights reserved.
 * Author: Andrew M. White
 *
 * Demonstration of how to work with binary files and hex representations.
 *
 */

#include <stdint.h>   // typedefs (e.g., uint8_t)
#include <stdio.h>    // printf, fopen/close
#include <stdlib.h>   // realloc
#include <string.h>   // strlen 

uint8_t hex2int(char c) {
  /*
   * convert a single ASCII hex character to it's integer value
   * i.e., (char)'F' => (int)16
   * 
   * char c: character to convert
   */

  if ((c >= '0') && (c <= '9')) {
    // decimal digit
    return (uint8_t)(c - '0');
  } else if ((c >= 'A') && (c <= 'Z')) { 
    // upper-case hex digit (e.g., A-F)
    return (uint8_t)(c - 'A' + 10);
  } else if ((c >= 'a') && (c <= 'z')) {
    // lower-case hex digit (e.g., a-f)
    return (uint8_t)(c - 'a' + 10);
  } else { 
    fprintf(stderr, "encountered non-hexadecimal ASCII character ('%c')\n", c);
    return 255;
  }
}

uint8_t hexpair2bin(char *buffer, size_t index) {
  /* 
   * convert *two* consecutive hex ASCII characters to byte value
   * 
   * char *buffer: array of hex digits
   * size_t index: index of first digit of pair (second is at index + 1)
   */


  uint8_t value, tmp1, tmp2;

  //
  // INSERT 

  tmp1 = buffer[index] > 57 ? buffer[index] - 'a' + 10 : buffer[index] - '0';
  tmp2 = buffer[index+1] > 57 ? buffer[index+1] - 'a' + 10 : buffer[index+1] - '0';

  value = (tmp1 << 4) + tmp2;
  printf("%x", value);

  return value;
}

size_t hex2bin(char *input_buffer, 
    uint8_t **output_buffer, 
    size_t *output_buffer_size) {
  /*
   * convert ASCII hex characters to byte values
   * allocates memory for output buffer
   * caller is responsible for freeing buffer
   *
   * char *input_buffer: array of ASCII hex characters
   * uint8_t **output_buffer: pointer to array which we overwrite with
   *                          our dynamically allocated array
   * size_t *output_buffer_size: pointer to integer which we overwrite
   *                             with the size of our dynamically 
   *                             allocated array
   */

  // one byte per pair of hex digits
  size_t bytes_to_write = strlen(input_buffer)/2;

  if (bytes_to_write > *output_buffer_size) {
    // too many bytes to write to our current buffer
    // reallocate a larger buffer and update our pointers
    *output_buffer_size = bytes_to_write * sizeof(uint8_t);
    *output_buffer = (uint8_t *)realloc((void *)*output_buffer, *output_buffer_size);
    fprintf(stderr, "output_buffer_size is now %lu\n", *output_buffer_size);
  }

  size_t bytes_written = 0;
  while (bytes_written < bytes_to_write) {
    // write bytes to output buffer one-at-a-time
    (*output_buffer)[bytes_written] = hexpair2bin(input_buffer, bytes_written*2);
    bytes_written += 1;
  }

  return bytes_written;
}

int main(int argc, char *argv[]) {

  if (argc != 3) {
    printf("usage: %s <input filename> <output filename>\n", argv[0]);
    printf("  input filename: name of file containing upper-case hex\n");
    printf("  output filename: name of file to which to write binary\n");
    return 1; 
  }

  // open our files for reading and writing
  FILE *fin = fopen(argv[1], "r");   // non-binary input
  // check for errors opening the file
  if (fin == NULL) {
    fprintf(stderr, "error opening file %s\n", argv[1]);
    return 1;
  } else {
    fprintf(stderr, "opened file %s\n", argv[1]);
  }

  FILE *fout = fopen(argv[2], "wb"); // binary output
  // check for errors opening the file
  if (fout == NULL) {
    fprintf(stderr, "error opening file %s\n", argv[2]);
    return 1;
  } else {
    fprintf(stderr, "opened file %s\n", argv[2]);
  }

  // unintialized string buffers to hold input chars 
  char *input_buffer = NULL;
  size_t input_buffer_size = 0;

  // unintialized string buffers to hold output bytes
  uint8_t *output_buffer = NULL;
  size_t output_buffer_size = 0;

  ssize_t chars_read = -1;
  size_t bytes_written = 0;
  while ((chars_read = getline(&input_buffer, &input_buffer_size, fin)) >= 0) { 
    // read and process file line-at-a-time

    // remove newline char if necessary
    if (input_buffer[chars_read-1] == '\n') { 
      chars_read -= 1;
      input_buffer[chars_read] = '\0';
    }

    if (chars_read > 0) {
      // convert ASCII hex char array to array of bytes
      bytes_written = hex2bin(input_buffer, &output_buffer, &output_buffer_size); 

      // write to output file
      fwrite(output_buffer, sizeof(uint8_t), bytes_written, fout);
      fprintf(stderr, "wrote buffer of size %lu\n", bytes_written);
    }
  }

  // always free dynamically allocated memory
  free(input_buffer);  // allocated by getline
  free(output_buffer); // allocated by hex2bin

  // always close file handles
  fclose(fin);
  fclose(fout);

  return 0;
}

