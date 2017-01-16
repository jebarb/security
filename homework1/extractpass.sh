#!/bin/bash
vboxmanage debugvm "COMP535VM_2" dumpvmcore --filename sec.elf
size=0x$(objdump -h sec.elf | grep -m1 load1 | cut -d ' ' -f 13);off=0x$(objdump -h sec.elf | grep -m1 load1 | cut -d ' ' -f 19);head -c $(($size+$off)) sec.elf|tail -c +$(($off+1)) > sec.raw
volatility -f sec.raw printkey --profile=Win7SP1x86 -o $(volatility -f sec.raw hivelist --profile=Win7SP1x86 2> /dev/null | grep 'SOFTWARE' | cut -d ' ' -f 1) -K Microsoft\\Windows 2> /dev/null | tail -1
