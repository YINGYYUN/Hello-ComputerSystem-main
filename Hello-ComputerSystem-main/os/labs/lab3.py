import sys
import os
from src.myos import process_count, process_schedule, process_step, process_exit
from src.process import SyscallType
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def my_run():
    # TODO: implement the main running loop that supports WRITE_DOUBLE syscall
    while process_count() > 0:
        current = process_schedule()
        call = process_step(current)
        if call.syscall == SyscallType.SYS_EXIT:
            process_exit(current)
        elif call.syscall == SyscallType.SYS_WRITE:
            print(call.arg, end='', flush=True)
        elif call.syscall == SyscallType.SYS_WRITE_DOUBLE:
            print(call.arg, end='', flush=True)
            print(call.arg, end='', flush=True)
    print()
