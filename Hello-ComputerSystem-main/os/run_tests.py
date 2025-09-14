#!/usr/bin/env python3
"""
Test Runner for OS Simulator
Runs all tests in the project
"""

import sys
import os
import unittest
import importlib.util

def add_project_to_path():
    """Add the project root to Python path"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

def discover_tests():
    """Discover all test files in the tests directory"""
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern='test_*.py')
    return suite

def run_specific_lab_test(lab_name):
    """Run tests for a specific lab"""
    test_file = f'test_{lab_name}.py'
    test_path = os.path.join(os.path.dirname(__file__), 'tests', test_file)
    
    if not os.path.exists(test_path):
        print(f"❌ Test file {test_file} not found")
        return False
    
    # Import the test module
    spec = importlib.util.spec_from_file_location(f"test_{lab_name}", test_path)
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)
    
    # Run the tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_module)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_all_tests():
    """Run all tests in the project"""
    print("🧪 Running All Tests for OS Simulator")
    print("=" * 50)
    
    suite = discover_tests()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("🎉 All Tests PASSED!")
    else:
        print("❌ Some Tests FAILED!")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
    
    return result.wasSuccessful()

def output_help():
    """Output help message"""
    print("Usage: python3 run_tests.py [lab_name|all]")
    print("Examples:")
    print("  python3 run_tests.py        # Run all tests")
    print("  python3 run_tests.py all    # Run all tests")
    print("  python3 run_tests.py lab1   # Run lab1 tests only")
    print("  python3 run_tests.py lab2   # Run lab2 tests only")
    print("  python3 run_tests.py lab3   # Run lab3 tests only")

def main():
    """Main entry point"""
    add_project_to_path()
    
    if len(sys.argv) == 1:
        # No arguments, run all tests
        success = run_all_tests()
    elif len(sys.argv) == 2:
        lab_name = sys.argv[1]
        if lab_name in ["--help", "-h", "help"]:
            output_help()
            sys.exit(0)
        elif lab_name == "all":
            success = run_all_tests()
        else:
            print(f"🧪 Running Tests for {lab_name}")
            print("=" * 50)
            success = run_specific_lab_test(lab_name)
            if success:
                print("\n" + "=" * 50)
                print(f"🎉 All Tests for {lab_name} PASSED!")
    else:
        output_help()
        sys.exit(1)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
