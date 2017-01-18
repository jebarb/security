#!/bin/bash
top="SOFTWARE"
entry="Password"
folder="Microsoft\\Windows"
vm="COMP535VM_2"
while [[ $# -gt 1 ]]
do
  key="$1"
  case $key in
    -t|--top)
      top="$2"
      shift
      ;;
    -e|--entry)
      entry="$2"
      shift
      ;;
    -v|--vm)
      vm="$2"
      shift
      ;;
    -f|--folder)
      folder="$2"
      ;;
    *)
      ;;
  esac
  shift
done

vboxmanage debugvm $vm dumpvmcore --filename sec.elf
size=0x$(objdump -h sec.elf | grep -m1 load1 | cut -d ' ' -f 13)
offset=0x$(objdump -h sec.elf | grep -m1 load1 | cut -d ' ' -f 19)
echo Size: $size
echo Offset: $offset
head -c $(($size+$offset)) sec.elf|tail -c +$(($offset+1)) > sec.raw
top=$(volatility -f sec.raw hivelist --profile=Win7SP1x86 2> /dev/null | \
  grep $top | cut -d ' ' -f 1)
echo Top: $top
volatility -f sec.raw printkey --profile=Win7SP1x86 -o $top \
  -K $folder 2> /dev/null | grep -a $entry

