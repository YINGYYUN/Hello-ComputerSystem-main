"""
OS Simulator - Core Modules

This package contains the core components of the operating system simulator.
"""

# 导入核心模块
from .process import Process, Syscall, SyscallType
from .myos import (
    init, 
    process_count, 
    process_schedule, 
    process_step, 
    process_exit,
    running_procs,
    scheduler
)

__all__ = [
    'Process',
    'Syscall', 
    'SyscallType',
    'init',
    'process_count',
    'process_schedule', 
    'process_step',
    'process_exit',
    'running_procs',
    'scheduler'
]
