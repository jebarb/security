[bits 32]

global GetCPUFamily
GetCPUFamily:
  ; Implementation goes here...
  push ebp           ; save ebp on stack
  mov ebp, esp       ; save stack pointer in ebp
  push ebx           ; save ebx
  mov eax, 1         ; first arg for CPUID to get family and other info
  CPUID              ; get CPUID info
  shl eax, 20        ; get rid of exta
  shr eax, 28        ; info from CPUID
  pop ebx            ; restore ebx
  mov esp, ebp       ; restore stack pointer
  pop ebp            ; restore ebp from stack
  ret

global GetPID
GetPID:
  ; Implementation goes here...
  push ebp           ; save ebp on stack
  mov ebp, esp       ; save esp in ebp
  sub esp, 4         ; make space for one local variable
  push ebx           ; save ebx
  mov eax, 0x14      ; getpid syscall
  int 0x80           ; execute syscall
  mov ebx, [ebp+8]   ; get first argument
  mov [ebx], eax     ; store PID at pointer
  pop ebx            ; restore ebx
  mov esp, ebp       ; restore stack pointer
  pop ebp            ; restore ebp from stack
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
  push ebp            ; save ebp on stack
  mov ebp, esp        ; save stack pointer in ebp
  sub esp, 16         ; make space for 4 local variables
  push ebx            ; save ebx
  mov eax, [ebp+12]   ; length of string
  mov ebx, [ebp+8]    ; pointer to string
  mov edx, [ebp+16]   ; value to use in xor
  mov ecx, 0          ; counter

XORLoop:
  xor [ebx], edx      ; xor first 4 bytes at pointer
  add ebx, 4          ; increment pointer by 4 bytes
  add ecx, 1          ; increment counter
  cmp ecx, eax        ; while ecx is
  jl XORLoop          ; less than eax

  pop ebx             ; restore ebx
  mov esp, ebp        ; restore stack pointer
  pop ebp             ; restore ebp from stack
  ret
