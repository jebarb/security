// This library contains basic utility functions for obtaining information
// about the computer's processor, process and files.
#ifndef LOW_LEVEL_INFO_H
#define LOW_LEVEL_INFO_H

// This returns the "family" value as reported by the system's processor. The
// number returned should be between 0 and 15. This should be implemented in
// low_level_asm.asm
int GetCPUFamily();

// This sets the given int to the pid of the current process. This should be
// implemented in low_level_asm.asm.
void GetPID(int *pid);

// Exits the current process, with code 123. This is implemented as an example
// in low_level_asm.asm.
void CustomExit();

// This function fills the content_names array with the names of the files and
// directories in the current working directory. If there are more files in the
// directory than max_files, then the remaining files should be ignored.
// This returns the number of files listed, up to max_files. The caller is
// responsible for freeing each name after it is no longer needed.
int GetCurrentDirectoryContents(char **names, int max_files);

// This function performs in place XOR operation on the string passed in the
// first argument. Each byte of the string up to length specified in the second
// argument is XORed with a  byte long key specified in the third argument. This function
// returns the amount of bytes that were XORed.  The callee is responsible for
// preserving registers. The function will be invoked using standard c calling convention
// ( see cdecl).
int XORString(char * to_xor, int length, int key);

#endif  // LOW_LEVEL_INFO_H
