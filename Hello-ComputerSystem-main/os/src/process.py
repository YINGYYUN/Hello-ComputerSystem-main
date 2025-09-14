from enum import Enum
from typing import List

# Syscall enumeration
class SyscallType(Enum):
    SYS_EXIT = 0   # Process exits
    SYS_WRITE = 1  # Write to console with a character
    SYS_WRITE_DOUBLE = 2
    SYS_FORK  = 3

class Syscall:
    """System call structure"""
    def __init__(self, syscall: SyscallType, arg: object=None):
        self.syscall = syscall
        self.arg = arg

class Process:
    """Process's Context"""
    def __init__(self, syscalls: List[Syscall], priority: int = 0):
        self.syscalls = syscalls
        self.step = 0  # Current step
        self.priority = priority  # Process priority (higher value = higher priority)

    def __copy__(self):
        # Custom deepcopy to avoid issues with mutable default arguments
        copied_syscalls = [Syscall(call.syscall, call.arg) for call in self.syscalls]
        new_process = Process(copied_syscalls, self.priority)
        new_process.step = self.step
        return new_process
