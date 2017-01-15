[bits 32]

global GetCPUFamily
GetCPUFamily:
  ; Implementation goes here...
  mov eax, 1
  CPUID
  shl eax, 20
  shr eax, 28
  ret

global GetPID
GetPID:
  ; Implementation goes here...
  mov eax, 0x14
  int 0x80
  mov ebx, [esp+8]
  mov [ebx], eax
  ret

global CustomExit
CustomExit:
  ; Set the eax register to 1, for the "exit" system call
  mov eax, 1
  ; Set the ebx register to our exit code, which will be 123
  mov ebx, 123
  ; Run int 0x80 to invoke the linux system call
  int 0x80
  ; Normally, you'd place a 'ret' here, but the exit syscall doesn't return.


global XORString
XORString:
  ; Implementation goes here
  ret
