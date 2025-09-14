import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.process import Process

def priority_scheduler(procs: list[Process]) -> Process:
    # TODO: implement a priority scheduler
    raise NotImplementedError("priority_scheduler is not implemented yet")
