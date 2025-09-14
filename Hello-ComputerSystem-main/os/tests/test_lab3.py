import unittest
import sys
import os
from typing import List
from io import StringIO
from copy import deepcopy
from contextlib import redirect_stdout

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import src.myos as myos
from src.process import Process, Syscall, SyscallType
from labs.lab3 import my_run

class TestLab3(unittest.TestCase):
    
    def capture_output(self, procs: List[Process]) -> str:
        """Capture the output from my_run function"""
        myos.init(lambda procs: procs[0], procs)
        f = StringIO()
        with redirect_stdout(f):
            my_run()
        return f.getvalue().rstrip('\n')  # Remove trailing newlines
    
    def reference_output(self, procs: List[Process]) -> str:
        """Reference implementation for expected output"""
        output = []
        # Create a copy of processes to avoid modifying the original list
        proc_list = [proc.__copy__() for proc in procs]
        
        while proc_list:
            # Simple sequential execution for reference
            current = proc_list[0]
            
            # Check if process has more syscalls to execute
            if current.step >= len(current.syscalls):
                # Process has no more syscalls, remove it
                proc_list.remove(current)
                continue
            
            # Get the current syscall
            call = current.syscalls[current.step]
            current.step += 1
            
            # Handle different syscall types
            if call.syscall == SyscallType.SYS_EXIT:
                proc_list.remove(current)
            elif call.syscall == SyscallType.SYS_WRITE:
                output.append(call.arg)
            elif call.syscall == SyscallType.SYS_WRITE_DOUBLE:
                # WRITE_DOUBLE outputs twice
                output.append(call.arg)
                output.append(call.arg)
        
        return ''.join(output)

    def test_lab3_implemented(self):
        """Test that my_run function exists and is callable"""
        self.assertTrue(callable(my_run))

    def test_basic_write(self):
        """Test basic WRITE syscall"""
        procs = [
            Process([
                Syscall(SyscallType.SYS_WRITE, "A"),
                Syscall(SyscallType.SYS_EXIT)
            ])
        ]
        
        result = self.capture_output(deepcopy(procs))
        expected = self.reference_output(procs)
        
        self.assertEqual(result, expected, f"Expected '{expected}', got '{result}'")

    def test_basic_write_double(self):
        """Test basic WRITE_DOUBLE syscall"""
        procs = [
            Process([
                Syscall(SyscallType.SYS_WRITE_DOUBLE, "B"),
                Syscall(SyscallType.SYS_EXIT)
            ])
        ]
        
        result = self.capture_output(deepcopy(procs))
        expected = self.reference_output(procs)
        
        # WRITE_DOUBLE should output twice
        self.assertEqual(result, "BB")
        self.assertEqual(result, expected, f"Expected '{expected}', got '{result}'")

    def test_mixed_syscalls(self):
        """Test mixed WRITE and WRITE_DOUBLE syscalls"""
        procs = [
            Process([
                Syscall(SyscallType.SYS_WRITE, "A"),
                Syscall(SyscallType.SYS_WRITE_DOUBLE, "B"),
                Syscall(SyscallType.SYS_WRITE, "C"),
                Syscall(SyscallType.SYS_EXIT)
            ])
        ]
        
        result = self.capture_output(deepcopy(procs))
        expected = self.reference_output(procs)
        
        # Expected: A, B, B, C
        self.assertEqual(result, "ABBC")
        self.assertEqual(result, expected, f"Expected '{expected}', got '{result}'")

    def test_multiple_processes(self):
        """Test multiple processes with different syscalls"""
        procs = [
            Process([
                Syscall(SyscallType.SYS_WRITE, "1"),
                Syscall(SyscallType.SYS_EXIT)
            ]),
            Process([
                Syscall(SyscallType.SYS_WRITE_DOUBLE, "2"),
                Syscall(SyscallType.SYS_EXIT)
            ]),
            Process([
                Syscall(SyscallType.SYS_WRITE, "3"),
                Syscall(SyscallType.SYS_WRITE_DOUBLE, "4"),
                Syscall(SyscallType.SYS_EXIT)
            ])
        ]
        
        result = self.capture_output(deepcopy(procs))
        expected = self.reference_output(procs)
        
        self.assertEqual(result, expected, f"Expected '{expected}', got '{result}'")

    def test_only_write_double(self):
        """Test process with only WRITE_DOUBLE syscalls"""
        procs = [
            Process([
                Syscall(SyscallType.SYS_WRITE_DOUBLE, "X"),
                Syscall(SyscallType.SYS_WRITE_DOUBLE, "Y"),
                Syscall(SyscallType.SYS_WRITE_DOUBLE, "Z"),
                Syscall(SyscallType.SYS_EXIT)
            ])
        ]
        
        result = self.capture_output(deepcopy(procs))
        expected = self.reference_output(procs)
        
        # Expected: X, X, Y, Y, Z, Z
        self.assertEqual(result, "XXYYZZ")
        self.assertEqual(result, expected, f"Expected '{expected}', got '{result}'")

    def test_empty_process_list(self):
        """Test with empty process list"""
        procs = []
        
        result = self.capture_output(procs.copy())
        expected = self.reference_output(procs)
        
        self.assertEqual(result, "")  # Empty string
        self.assertEqual(result, expected, f"Expected '{expected}', got '{result}'")

    def test_process_only_exit(self):
        """Test process with only EXIT syscall"""
        procs = [
            Process([
                Syscall(SyscallType.SYS_EXIT)
            ])
        ]
        
        result = self.capture_output(procs)
        expected = self.reference_output(procs)
        
        self.assertEqual(result, "")  # Empty string
        self.assertEqual(result, expected, f"Expected '{expected}', got '{result}'")

    def test_complex_scenario(self):
        """Complex test with multiple processes and syscall types"""
        procs = [
            Process([
                Syscall(SyscallType.SYS_WRITE, "START"),
                Syscall(SyscallType.SYS_WRITE_DOUBLE, "MID"),
                Syscall(SyscallType.SYS_WRITE, "END"),
                Syscall(SyscallType.SYS_EXIT)
            ]),
            Process([
                Syscall(SyscallType.SYS_WRITE_DOUBLE, "DOUBLE1"),
                Syscall(SyscallType.SYS_WRITE_DOUBLE, "DOUBLE2"),
                Syscall(SyscallType.SYS_EXIT)
            ]),
            Process([
                Syscall(SyscallType.SYS_WRITE, "SINGLE"),
                Syscall(SyscallType.SYS_EXIT)
            ])
        ]
        
        result = self.capture_output(deepcopy(procs))
        expected = self.reference_output(procs)
        
        self.assertEqual(result, expected, f"Expected '{expected}', got '{result}'")

if __name__ == '__main__':
    print("============================================================")
    print("Lab3 WRITE_DOUBLE Syscall Tests")
    print("============================================================")
    
    unittest.main(verbosity=2)
    
    print("============================================================")
    print("🎉 All Tests PASSED")
    print("============================================================")
