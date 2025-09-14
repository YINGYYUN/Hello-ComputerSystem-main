import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.process import Process

def sequential_scheduler(procs: list[Process]) -> Process:
    # TODO: implement a sequential scheduler
    # Simple implementation: return the first process
    raise NotImplementedError("sequential_scheduler is not implemented yet")
