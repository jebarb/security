Low Level Info Exercise
=======================

This project is intended for an exercise in writing C and assembly code to
interact with the system.

Included Files
--------------

 - low_level_info.h

    This file is a C header file that includes the signatures of the functions
    that need to be implemented.

 - low_level_asm.asm

    This file contains x86 assmebly to be assembled using the nasm tool. The
    boilerplate for linking the assembly functions to a C program is already in
    place, and an example function, CustomExit, is already defined.

 - low_level_info.c

    This will define a C library, that will only contain one function for now.
    It should be used to define the GetCurrentDirectoryContents function.

 - low_level_info_test.c

    This file defines the main() function for a test program. The test progam
    calls all of the functions defined in low_level_info.h and prints the
    results. When it runs successfully, you should see output similar to this:

        CPU family: 6.
        My PID is 24156.
        File 1 name: low_level_info.h.
        File 2 name: ..
        File 3 name: ...
        File 4 name: makefile.
        File 5 name: low_level_info_test.c.
        File 6 name: low_level_asm.asm.
        File 7 name: low_level_asm.o.
        File 8 name: low_level_info.c.
        File 9 name: low_level_info_test.
        File 10 name: low_level_info.o.

 - makefile

    This file contains instructions to use the defined C and assembly libraries
    to build the low_level_info_test executable.
