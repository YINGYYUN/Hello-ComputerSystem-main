import random
import time
from typing import List

from .process import Process, Syscall

running_procs: List[Process] = []

scheduler = None

# Operating System Functions
def init(
    my_scheduler,
    my_procs: List[Process]
):
    """Initialize the Operating System"""
    random.seed(time.time())
    
    global running_procs, scheduler
    running_procs = my_procs
    scheduler = my_scheduler

def process_count() -> int:
    """Get the number of running processes"""
    return len(running_procs)

def process_schedule() -> Process:
    """Schedule a process randomly"""
    return scheduler(running_procs)

def process_push(proc: Process):
    """Push a new process into the running queue"""
    global running_procs
    running_procs.append(proc)

def process_step(proc: Process) -> Syscall:
    """Execute one step of the process"""
    call = proc.syscalls[proc.step]
    proc.step += 1
    
    return call

def process_exit(proc: Process):
    """Exit a process and remove it from running queue"""
    global running_procs

    running_procs.remove(proc)
