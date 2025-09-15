
import sys
import os
from src.myos import process_count, process_schedule, process_step, process_exit, process_push
from src.process import SyscallType
import copy
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def my_run():
    while process_count() > 0:
        current = process_schedule()
        call = process_step(current)
        if call.syscall == SyscallType.SYS_EXIT:
            process_exit(current)
        elif call.syscall == SyscallType.SYS_WRITE:
            print(call.arg, end='', flush=True)
        elif call.syscall == SyscallType.SYS_WRITE_DOUBLE:
            print(call.arg, end='', flush=True)
            print()
            print(call.arg, end='', flush=True)
        elif call.syscall == SyscallType.SYS_FORK:
            new_proc = copy.copy(current)
            process_push(new_proc)
    print()