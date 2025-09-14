import sys
import os
import random

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.myos import *
from src.process import SyscallType, Process, Syscall

def random_scheduler(procs):
    """A random scheduler that selects a process randomly"""
    return random.choice(procs)

def run():
    """
    Main running loop for the Operating System.
    The Operating System will randomly choose a process to run until all processes exit.
    """
    while process_count() > 0:
        # The Operating System will randomly choose a process to run
        current = process_schedule()
        
        # Switch process context and run it until a syscall
        call = process_step(current)
        
        if call.syscall == SyscallType.SYS_EXIT:
            # Process exits
            process_exit(current)
        elif call.syscall == SyscallType.SYS_WRITE:
            # Write the character from syscall arg to the console
            print(call.arg, end='', flush=True)
    
    print()  # Print newline at the end


def main():
    """
    Main function - demonstrates the mini operating system
    
    In this model, we have a mini Operating System that can run multiple processes.
    Each process has a context that contains two variables: remaining_step and char_to_output.
    remaining_step is the number of steps that a process will run and then exit by doing a syscall EXIT.
    char_to_output is the character that a process will write to the console by doing a syscall WRITE.
    """
    # Initialize the Operating System
    init(
        random_scheduler,
        [
            Process([Syscall(SyscallType.SYS_WRITE, 'A')] * 5 + [Syscall(SyscallType.SYS_EXIT)]),  # Process A runs 5 steps, outputs character 'A'
            Process([Syscall(SyscallType.SYS_WRITE, 'B')] * 5 + [Syscall(SyscallType.SYS_EXIT)]),  # Process B runs 5 steps, outputs character 'B'
            Process([Syscall(SyscallType.SYS_WRITE, 'C')] * 5 + [Syscall(SyscallType.SYS_EXIT)]),  # Process C runs 5 steps, outputs character 'C'
        ]
    )
    
    # Start running
    run()

if __name__ == "__main__":
    main()
