    .section .rodata
msg:
    .asciz "Hello, World!\n"

    .section .text
    .global _start
_start:
    # Write "Hello, World!" to stdout
    mov $1, %rax            # syscall: write
    mov $1, %rdi            # file descriptor: stdout
    lea msg(%rip), %rsi     # pointer to message
    mov $14, %rdx           # message length
    syscall
    
    # Exit the program
    mov $60, %rax           # syscall: exit
    xor %rdi, %rdi          # status: 0
    syscall
