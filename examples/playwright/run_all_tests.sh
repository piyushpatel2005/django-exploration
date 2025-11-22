#!/bin/bash
# Shell script to run all Playwright example tests

set -e  # Exit on error

echo "============================================================"
echo "Running All Playwright Examples"
echo "============================================================"

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Counter for results
PASSED=0
FAILED=0

# Function to run a test
run_test() {
    local dir=$1
    local file=$2
    
    echo ""
    echo "------------------------------------------------------------"
    echo "[$dir] Running $file..."
    echo "------------------------------------------------------------"
    
    if (cd "$dir" && python "$file" > /dev/null 2>&1); then
        echo "✓ $dir - PASSED"
        ((PASSED++))
        return 0
    else
        echo "✗ $dir - FAILED"
        ((FAILED++))
        return 1
    fi
}

# Run all main.py files
for dir in */; do
    if [ -f "${dir}main.py" ]; then
        run_test "$dir" "main.py" || true  # Continue on error
    fi
done

# Run pytest tests if pytest is available
if command -v pytest &> /dev/null; then
    echo ""
    echo "------------------------------------------------------------"
    echo "Running pytest tests..."
    echo "------------------------------------------------------------"
    
    for test_file in $(find . -name "test_*.py" -type f); do
        test_dir=$(dirname "$test_file")
        test_name=$(basename "$test_file")
        run_test "$test_dir" "$test_name" || true
    done
fi

# Summary
echo ""
echo "============================================================"
echo "SUMMARY"
echo "============================================================"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo "Total:  $((PASSED + FAILED))"
echo "============================================================"

# Exit with error if any tests failed
if [ $FAILED -gt 0 ]; then
    exit 1
else
    exit 0
fi

