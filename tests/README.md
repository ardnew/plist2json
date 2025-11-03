# Test Suite for plist2json

This directory contains comprehensive test cases for the plist2json package.

## Test Coverage

The test suite achieves **100% code coverage** including branch coverage.

## Running Tests

### Prerequisites
```bash
pip install -r requirements-dev.txt
```

### Run all tests
```bash
pytest tests/
```

### Run tests with coverage report
```bash
pytest tests/ --cov=pkg --cov-report=term-missing --cov-branch
```

### Generate HTML coverage report
```bash
pytest tests/ --cov=pkg --cov-report=html
# Open htmlcov/index.html in your browser
```

## Test Structure

- **TestSerializeDefault**: Tests for the `serialize_default()` function
  - Handles non-serializable objects (bytes, custom classes, datetime)

- **TestReadPlist**: Tests for the `read_plist()` function
  - Reading from files
  - Reading from stdin
  - Complex nested data structures

- **TestMain**: Tests for the `main()` function
  - File input with various indent options (numeric, string, zero)
  - Stdin input with and without indentation
  - Error handling (file not found, invalid plist, exceptions)
  - Various data types (unicode, booleans, floats, arrays, dicts)
  - Edge cases (empty plist, deeply nested structures)

- **TestMainAsScript**: Tests for script execution
  - Running as a module (`python -m pkg`)
  - Direct script execution
  - `if __name__ == '__main__'` guard coverage

## Test Coverage Summary

```
Name              Stmts   Miss Branch BrPart  Cover
-----------------------------------------------------
pkg/__init__.py       3      0      0      0   100%
pkg/__main__.py      38      0      6      0   100%
-----------------------------------------------------
TOTAL                41      0      6      0   100%
```

## Test Cases (27 total)

1. Serialization of non-JSON types
2. Reading plist from file
3. Reading plist from stdin
4. Complex nested data structures
5. File input with default indentation
6. File input with numeric indentation
7. File input with string indentation (tabs)
8. Stdin input
9. Stdin input with indentation
10. File not found error handling
11. Invalid plist format error handling
12. Non-serializable objects handling
13. Unicode character support
14. Empty plist files
15. Array-based plist files
16. Deeply nested structures
17. Generic exception handling
18. Short indent option (-i)
19. Zero indentation
20. Boolean values
21. Float values
22. Special characters in filenames
23. Module execution
24. Direct script execution
25. Name guard coverage
