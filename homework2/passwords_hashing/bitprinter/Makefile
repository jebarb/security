## Copyright (c) 2013, UNC Chapel Hill. All rights reserved.
## Author: Andrew M. White
##
## Simple makefile for introductory COMP535 lab programs.

# macros to define commonly used strings
CC = gcc
CFLAGS = -Wall -std=c99

# general Makefile syntax
# <target name> : <target prerequisites>
# 	<command(s) to build target>
# 	
# target name:    generally, a file to check for updated prereqs and build
#							 		if necessary
# prerequisites:  files or other targets required to build current target
# commands: 			shell commands to build target given prereqs

# special variables
# '$@': target name
# '$?': target's prereqs

bitprinter: bitprinter.c
	$(CC) $(CFLAGS) $? -o $@

# .PHONY tells make not to look for these files
# i.e., there won't be a file named 'clean' to check
.PHONY : clean 
clean:
	rm bitprinter 
