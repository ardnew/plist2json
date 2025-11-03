# plist2json

![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Zero-external-dependency command-line tool to convert Apple Property List (plist) files from binary or XML to JSON format.


## Description

`plist2json` is a Python-based utility that converts plist files from binary or XML to JSON format. Input is read from stdin (default) or command-line argument, and output is written to stdout. It handles non-serializable objects gracefully and provides an option to format the JSON indentation. 

The conventional `plutil` refuses to convert to JSON many standard plist files found across macOS due to unsupported data types, irregular encodings, or other issues. You'll find really useful error messages such as:

```bash
$ plutil -convert json -o- problematic.plist
<stdin>: invalid object in plist for destination format

$ plutil -convert xml1 -o- problematic.plist
# ...valid XML output...
$ plutil -convert xml1 -o- problematic.plist | plutil -convert json -o- -
<stdin>: invalid object in plist for destination format

$ plutil -convert binary1 -o- problematic.plist | plutil -convert json -o- -
<stdin>: invalid object in plist for destination format
```

These are often benign problems unrelated to the actual data content such as trailing or leading `\0` or `\n` bytes, non-standard date formats, etc.

This tool instead uses the Python `plistlib` module, which is much more forgiving and can successfully parse and convert many such problematic plists to JSON.

The project depends only on the Python standard library as distributed by default with Apple macOS for easy installation even in offline or air-gapped environments.


## Features

- ✅ No external dependencies (uses Python standard library)
- ✅ Convert both binary and XML plist formats
- ✅ Read from files or stdin for pipeline integration
- ✅ Customizable JSON indentation
- ✅ Graceful handling of non-serializable objects
- ✅ Unicode (UTF-8) support
- ✅ Informative error messages


## Installation

Download the latest released wheel package (*.whl) and install using pip:

```bash
pip install plist2json-<version>-py3-none-any.whl
```

The wheel package includes all necessary files and can be installed without Internet access.


### Requirements

- Python 3.7 or higher


## Usage


### Basic usage

Convert a plist file from any supported format to JSON:

```bash
plist2json input.plist          # read from file
cat input.plist | plist2json    # read from stdin
```

The output JSON is printed compactly without any extra whitespace by default.

```bash
plist2json -i 2     input.plist    # 2 spaces
plist2json -i $'\t' input.plist    # 1 tab (bash or zsh)
```

Use with `jq` to filter and process JSON output

```bash
plist2json input.plist | jq '.someKey'             # extract value as JSON
plist2json input.plist | jq -r '.tableKey | @csv'  # extract table as CSV
```


### Command-line options

```
usage: plist2json [-h] [-i INDENT] [file]

Convert plist to JSON

positional arguments:
  file                  Input plist file (default: stdin)

optional arguments:
  -h, --help            show this help message and exit
  -i INDENT, --indent INDENT
                        Indentation for JSON output (number of spaces or string)
```


## Examples


### Example 1: Basic conversion

```bash
$ plist2json example.plist
{"key1":"value1","key2":42,"array":["item1","item2"]}
```


### Example 2: Formatted output

```bash
$ plist2json -i 4 example.plist
{
    "key1": "value1",
    "key2": 42,
    "array": [
        "item1",
        "item2",
        "item3"
    ]
}
```


### Example 3: Using in a shell script

```bash
#!/bin/bash
# Convert the `.array` to tab-separated values
plist2json example.plist | jq -r '.array | @tsv'
# Output:
#item1    item2    item3
```


## Development

Clone the repository, install in editable mode, and run tests:

```bash
git clone https://github.com/yourusername/plist2json.git
cd plist2json
pip install -e .
# Run tests to verify installation
python -m pytest tests/
```


## Testing

This project maintains **100% test coverage** with a comprehensive test suite. The tests cover all functionality including:

- All input/output modes (file, stdin)
- Various indentation options
- Error handling and edge cases
- Unicode and special character support
- All data types and structures

### Running Tests

Install test dependencies:
```bash
pip install -r requirements-dev.txt
```

Run the test suite:
```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=pkg --cov-report=term-missing --cov-branch

# Generate HTML coverage report
pytest tests/ --cov=pkg --cov-report=html
# Open htmlcov/index.html in your browser
```

For more details about the test suite, see [tests/README.md](tests/README.md).


### Publishing a release

The project includes a `publish.sh` script that automates the release process. It will:

- Update the version number in all project files
- Build wheel and source distribution packages
- Commit version changes and create a git tag
- Create a GitHub release with the built packages


*Prerequisites:*

- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
- Python build tools (`build` and `twine` will be installed automatically)


*Usage:*

```bash
# Publish with auto-generated release notes
./publish.sh 0.2.0

# Publish with custom release notes
echo "Bug fixes and performance improvements" | ./publish.sh 0.2.0

# Publish with multi-line release notes
cat <<EOF | ./publish.sh 0.2.0
## What's New
- Added feature X
- Fixed bug Y
- Improved performance of Z
EOF
```

The script will create a new release on GitHub with the wheel package (`.whl`) and source distribution (`.tar.gz`) attached as downloadable assets.


## License

This project is licensed under the [MIT License](LICENSE).


## Contributing

The intent is to keep this project as simple as possible, with an emphasis on compatibility and ease of installation (no external dependencies).

But feel free to submit pull requests that align with these goals:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## Acknowledgments

Project scaffolding and README authoring assisted by Claude Sonnet 4.5 via GitHub Copilot.
