low_level_info_test: low_level_asm.o low_level_info.o low_level_info_test.c
	gcc -g -m32 -Wall -o low_level_info_test low_level_info_test.c \
		low_level_asm.o low_level_info.o

clean:
	rm -f *.o
	rm -f low_level_info_test

low_level_asm.o: low_level_asm.asm
	nasm -f elf -o low_level_asm.o low_level_asm.asm

low_level_info.o: low_level_info.c low_level_info.h
	gcc -m32 -c -Wall -o low_level_info.o low_level_info.c

