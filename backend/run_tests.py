#!/usr/bin/env python3
"""
Test runner script for Email Task Manager
"""
import sys
import os
import subprocess
import argparse
from pathlib import Path

def run_tests(test_type=None, coverage=True, verbose=False):
    """Run tests with specified options"""
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Build pytest command
    cmd = ['python', '-m', 'pytest']
    
    if test_type:
        cmd.extend(['-m', test_type])
    
    if coverage:
        cmd.extend(['--cov=.', '--cov-report=term-missing', '--cov-report=html:htmlcov'])
    
    if verbose:
        cmd.append('-v')
    
    # Add test directory
    cmd.append('tests/')
    
    print(f"Running tests with command: {' '.join(cmd)}")
    print("=" * 60)
    
    # Run tests
    try:
        result = subprocess.run(cmd, check=True)
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print(f"❌ Tests failed with exit code {e.returncode}")
        return e.returncode

def run_specific_test(test_file):
    """Run a specific test file"""
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    cmd = ['python', '-m', 'pytest', f'tests/{test_file}', '-v']
    
    print(f"Running specific test: {test_file}")
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n" + "=" * 60)
        print("✅ Test passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print(f"❌ Test failed with exit code {e.returncode}")
        return e.returncode

def run_coverage_report():
    """Generate coverage report"""
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    cmd = ['python', '-m', 'coverage', 'report', '--show-missing']
    
    print("Generating coverage report...")
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Coverage report failed with exit code {e.returncode}")
        return e.returncode

def main():
    parser = argparse.ArgumentParser(description='Run Email Task Manager tests')
    parser.add_argument('--type', '-t', choices=['unit', 'integration', 'api', 'models', 'services', 'utils'],
                       help='Run specific test type')
    parser.add_argument('--file', '-f', help='Run specific test file')
    parser.add_argument('--no-coverage', action='store_true', help='Run tests without coverage')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--coverage-report', action='store_true', help='Generate coverage report only')
    
    args = parser.parse_args()
    
    if args.coverage_report:
        return run_coverage_report()
    
    if args.file:
        return run_specific_test(args.file)
    
    return run_tests(
        test_type=args.type,
        coverage=not args.no_coverage,
        verbose=args.verbose
    )

if __name__ == '__main__':
    sys.exit(main())
