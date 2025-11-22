#!/usr/bin/env python3
"""
Script to run all Playwright example tests.

This script will:
1. Run all main.py files in subdirectories
2. Run all pytest test files
"""

import os
import subprocess
import sys
from pathlib import Path

def run_main_files():
    """Run all main.py files in subdirectories."""
    base_dir = Path(__file__).parent
    main_files = sorted(base_dir.glob("*/main.py"))
    
    print("=" * 70)
    print("Running main.py files")
    print("=" * 70)
    
    results = []
    for main_file in main_files:
        dir_name = main_file.parent.name
        print(f"\n[{dir_name}] Running {main_file.name}...")
        print("-" * 70)
        
        try:
            result = subprocess.run(
                [sys.executable, str(main_file)],
                cwd=main_file.parent,
                capture_output=False,
                timeout=60
            )
            if result.returncode == 0:
                print(f"✓ {dir_name} - PASSED")
                results.append((dir_name, True))
            else:
                print(f"✗ {dir_name} - FAILED (exit code: {result.returncode})")
                results.append((dir_name, False))
        except subprocess.TimeoutExpired:
            print(f"✗ {dir_name} - TIMEOUT (exceeded 60 seconds)")
            results.append((dir_name, False))
        except Exception as e:
            print(f"✗ {dir_name} - ERROR: {e}")
            results.append((dir_name, False))
    
    return results

def run_pytest_tests():
    """Run all pytest test files."""
    base_dir = Path(__file__).parent
    
    print("\n" + "=" * 70)
    print("Running pytest tests")
    print("=" * 70)
    
    # Find all test files, excluding virtual environment directories
    test_files = []
    for test_file in base_dir.glob("**/test_*.py"):
        # Skip files in virtual environment directories
        parts = test_file.parts
        if any(part in ('.env', 'venv', '.venv', '__pycache__', 'site-packages') for part in parts):
            continue
        test_files.append(test_file)
    
    test_files = sorted(test_files)
    
    if not test_files:
        print("No pytest test files found.")
        return []
    
    results = []
    for test_file in test_files:
        dir_name = test_file.parent.name
        print(f"\n[{dir_name}] Running {test_file.name}...")
        print("-" * 70)
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(test_file), "-v"],
                cwd=test_file.parent,
                capture_output=False,
                timeout=60
            )
            if result.returncode == 0:
                print(f"✓ {dir_name} - PASSED")
                results.append((dir_name, True))
            else:
                print(f"✗ {dir_name} - FAILED (exit code: {result.returncode})")
                results.append((dir_name, False))
        except subprocess.TimeoutExpired:
            print(f"✗ {dir_name} - TIMEOUT (exceeded 60 seconds)")
            results.append((dir_name, False))
        except Exception as e:
            print(f"✗ {dir_name} - ERROR: {e}")
            results.append((dir_name, False))
    
    return results

def main():
    """Main function to run all tests."""
    print("\n" + "=" * 70)
    print("Playwright Examples Test Runner")
    print("=" * 70)
    
    # Run main.py files
    main_results = run_main_files()
    
    # Run pytest tests
    pytest_results = run_pytest_tests()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    all_results = main_results + pytest_results
    total = len(all_results)
    passed = sum(1 for _, success in all_results if success)
    failed = total - passed
    
    print(f"\nTotal tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed > 0:
        print("\nFailed tests:")
        for name, success in all_results:
            if not success:
                print(f"  - {name}")
    
    print("\n" + "=" * 70)
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()

