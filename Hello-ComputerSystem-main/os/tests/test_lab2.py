import unittest
import sys
import os
from typing import List, Callable

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.process import Process, Syscall, SyscallType
from labs.lab2 import priority_scheduler

class TestLab2(unittest.TestCase):
    def run_os(self, scheduler: Callable[[List[Process]], Process], procs: List[Process]) -> List[str]:
        output = []
        
        while len(procs) > 0:
            current: Process = scheduler(procs)
            
            if current.step >= len(current.syscalls):
                procs.remove(current)
                continue
                
            call = current.syscalls[current.step]
            current.step += 1
            
            if call.syscall == SyscallType.SYS_EXIT:
                procs.remove(current)
            elif call.syscall == SyscallType.SYS_WRITE:
                output.append(call.arg)
        
        return output
    
    def reference_priority(self, procs: List[Process]) -> List[str]:
        """Reference implementation for priority scheduler"""
        output = []
        # Create a copy of processes to avoid modifying the original list
        proc_list = [proc.__copy__() for proc in procs]
        
        while proc_list:
            # Find the process with highest priority
            highest_priority_proc = max(proc_list, key=lambda p: p.priority)
            
            # Execute one step of the highest priority process
            if highest_priority_proc.step < len(highest_priority_proc.syscalls):
                call = highest_priority_proc.syscalls[highest_priority_proc.step]
                highest_priority_proc.step += 1
                
                if call.syscall == SyscallType.SYS_EXIT:
                    proc_list.remove(highest_priority_proc)
                elif call.syscall == SyscallType.SYS_WRITE:
                    output.append(call.arg)
            else:
                # Process has no more syscalls
                proc_list.remove(highest_priority_proc)
        
        return output

    def test_lab2_implemented(self):
        """Test that priority_scheduler function exists and is callable"""
        self.assertTrue(callable(priority_scheduler))

    def test_priority_basic(self):
        """Basic priority test with 2 processes"""
        procs = [
            Process([
                Syscall(SyscallType.SYS_WRITE, "A"),
                Syscall(SyscallType.SYS_EXIT)
            ], priority=1),
            Process([
                Syscall(SyscallType.SYS_WRITE, "B"),
                Syscall(SyscallType.SYS_EXIT)
            ], priority=2)
        ]
        
        # Make copies for both runs
        procs_copy1 = [proc.__copy__() for proc in procs]
        procs_copy2 = [proc.__copy__() for proc in procs]
        
        result = self.run_os(priority_scheduler, procs_copy1)
        expected = self.reference_priority(procs_copy2)
        
        self.assertEqual(result, expected, f"Expected {expected}, got {result}")

    def test_priority_multiple_steps(self):
        """Test priority scheduling with multiple steps per process"""
        procs = [
            Process([
                Syscall(SyscallType.SYS_WRITE, "A1"),
                Syscall(SyscallType.SYS_WRITE, "A2"),
                Syscall(SyscallType.SYS_EXIT)
            ], priority=1),
            Process([
                Syscall(SyscallType.SYS_WRITE, "B1"),
                Syscall(SyscallType.SYS_WRITE, "B2"),
                Syscall(SyscallType.SYS_EXIT)
            ], priority=3),
            Process([
                Syscall(SyscallType.SYS_WRITE, "C1"),
                Syscall(SyscallType.SYS_EXIT)
            ], priority=2)
        ]
        
        # Make copies for both runs
        procs_copy1 = [proc.__copy__() for proc in procs]
        procs_copy2 = [proc.__copy__() for proc in procs]
        
        result = self.run_os(priority_scheduler, procs_copy1)
        expected = self.reference_priority(procs_copy2)
        
        self.assertEqual(result, expected, f"Expected {expected}, got {result}")

    def test_priority_same_priority(self):
        """Test behavior when processes have the same priority"""
        procs = [
            Process([
                Syscall(SyscallType.SYS_WRITE, "A"),
                Syscall(SyscallType.SYS_EXIT)
            ], priority=1),
            Process([
                Syscall(SyscallType.SYS_WRITE, "B"),
                Syscall(SyscallType.SYS_EXIT)
            ], priority=1),
            Process([
                Syscall(SyscallType.SYS_WRITE, "C"),
                Syscall(SyscallType.SYS_EXIT)
            ], priority=2)
        ]
        
        # Make copies for both runs
        procs_copy1 = [proc.__copy__() for proc in procs]
        procs_copy2 = [proc.__copy__() for proc in procs]
        
        result = self.run_os(priority_scheduler, procs_copy1)
        expected = self.reference_priority(procs_copy2)
        
        self.assertEqual(result, expected, f"Expected {expected}, got {result}")

    def test_priority_zero_priority(self):
        """Test processes with zero and negative priorities"""
        procs = [
            Process([
                Syscall(SyscallType.SYS_WRITE, "A"),
                Syscall(SyscallType.SYS_EXIT)
            ], priority=0),
            Process([
                Syscall(SyscallType.SYS_WRITE, "B"),
                Syscall(SyscallType.SYS_EXIT)
            ], priority=-1),
            Process([
                Syscall(SyscallType.SYS_WRITE, "C"),
                Syscall(SyscallType.SYS_EXIT)
            ], priority=1)
        ]
        
        # Make copies for both runs
        procs_copy1 = [proc.__copy__() for proc in procs]
        procs_copy2 = [proc.__copy__() for proc in procs]
        
        result = self.run_os(priority_scheduler, procs_copy1)
        expected = self.reference_priority(procs_copy2)
        
        self.assertEqual(result, expected, f"Expected {expected}, got {result}")

    def test_priority_stress(self):
        """Stress test with many processes of different priorities"""
        procs = []
        for i in range(10):
            procs.append(Process([
                Syscall(SyscallType.SYS_WRITE, f"P{i}"),
                Syscall(SyscallType.SYS_EXIT)
            ], priority=i % 3))  # Priorities 0, 1, 2
        
        # Make copies for both runs
        procs_copy1 = [proc.__copy__() for proc in procs]
        procs_copy2 = [proc.__copy__() for proc in procs]
        
        result = self.run_os(priority_scheduler, procs_copy1)
        expected = self.reference_priority(procs_copy2)
        
        self.assertEqual(result, expected, f"Expected {expected}, got {result}")

    def test_single_process_priority(self):
        """Test with a single process"""
        procs = [
            Process([
                Syscall(SyscallType.SYS_WRITE, "SINGLE"),
                Syscall(SyscallType.SYS_WRITE, "PROCESS"),
                Syscall(SyscallType.SYS_EXIT)
            ], priority=5)
        ]
        
        # Make copies for both runs
        procs_copy1 = [proc.__copy__() for proc in procs]
        procs_copy2 = [proc.__copy__() for proc in procs]
        
        result = self.run_os(priority_scheduler, procs_copy1)
        expected = self.reference_priority(procs_copy2)
        
        self.assertEqual(result, expected, f"Expected {expected}, got {result}")

if __name__ == '__main__':
    print("============================================================")
    print("Lab2 Priority Scheduler Tests")
    print("============================================================")
    
    unittest.main(verbosity=2)
    
    print("============================================================")
    print("🎉 All Tests PASSED")
    print("============================================================")
