import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.process import Process

def priority_scheduler(procs: list[Process]) -> Process:
    # TODO: implement a priority scheduler
    if not procs:  
        raise ValueError("No processes available to schedule")
    highestProc= procs[0]
    for proc in procs[1:]:
        if proc.priority > highestProc.priority:
            highestProc = proc
    return highestProc
