// This program tests out the values returned by the low_level_info library.
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "low_level_info.h"
#define MAX_FILES 100

int print_hex_string(char * to_print, int length){
  int i = 0;
  for (i=0; i<length; i++){
    printf("0x%02x ",(unsigned char) to_print[i]);
  }
  printf("\n");
  return i;
}


int main(int argc, char **argv) {
  int my_pid, file_count, i, xor_key;
  char **names = NULL;
  char * test_string;
  int retval = 0;
  names = (char**) malloc(sizeof(char*) * MAX_FILES);
  if (names == NULL) {
    printf("Failed allocating content names array.\n");
    return 1;
  }

  // Print the CPU's reported family value
  printf("CPU family: %d.\n", GetCPUFamily());

  my_pid = 4;
  // Print the process' PID
  GetPID(&my_pid);
  printf("My PID is %d.\n", my_pid);

  // Print the contents of the current directory
  file_count = GetCurrentDirectoryContents(names, MAX_FILES);
  for (i = 0; i < file_count; i++) {
    printf("File %d name: %s.\n", i + 1, names[i]);
    free(names[i]);
    names[i] = NULL;
  }
  free(names);
  names = NULL;
  if (argc <3) {
    test_string = (char *) malloc(256);
    if (test_string == NULL) exit(-1);
    printf("Please enter the string to XoR\n");
    fgets(test_string,256,stdin);
    test_string[strcspn(test_string, "\n")] = 0;
    printf("Please enter the key (0-255)\n");
    scanf("%d", &xor_key);
  }
  else {
    test_string = strndup(argv[1],256);
    if (test_string == NULL) exit(-1);
    xor_key = atoi(argv[2]);
    if (xor_key < 0 || xor_key >255) exit(-1);
  }
  printf("Before XOR: %s\n", test_string);
  printf("Hex representation:\n");
  print_hex_string(test_string, strlen(test_string));
  retval = XORString(test_string,strlen(test_string),(char) xor_key);
  printf("XORed %d bytes with key 0x%x\n",retval, xor_key);
  printf("String representation: %s\n", test_string);
  printf("Hex representation:\n");
  print_hex_string(test_string, retval);
  free(test_string);
  // Exit with code 123
  CustomExit();

  // This shouldn't be reached.
  return 0;
}
