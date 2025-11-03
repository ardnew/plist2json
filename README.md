# plist2json

Simple command-line tool to convert Apple Property List (plist) files from binary or XML to JSON format.


## Description

`plist2json` is a Python-based utility that converts plist files from binary or XML to JSON format. Input is read from stdin (default) or command-line argument, and output is written to stdout. It handles non-serializable objects gracefully and provides an option to format the JSON indentation. 

The project depends only on the Python standard library as distributed by default with Apple macOS for easy installation even in offline or air-gapped environments (see [Install from release package](#install-from-release-package)).


## Features

- ✅ No external dependencies (uses Python standard library)
- ✅ Convert both binary and XML plist formats
- ✅ Read from files or stdin for pipeline integration
- ✅ Customizable JSON indentation
- ✅ Graceful handling of non-serializable objects
- ✅ Unicode (UTF-8) support
- ✅ Informative error messages


## Installation


### Install from source

```bash
git clone https://github.com/yourusername/plist2json.git
cd plist2json
pip install .
```


### Install from release package

Download the latest released wheel package (*.whl) and install using pip:

```bash
pip install plist2json-<version>-py3-none-any.whl
```

The wheel package includes all necessary files and can be installed without Internet access.


### Requirements

- Python 3.7 or higher


## Usage


### Basic usage

Convert a plist file to JSON:

```bash
plist2json input.plist
```


### Read from stdin

```bash
cat input.plist | plist2json
```


### Custom indentation

Use a specific number of spaces for indentation:

```bash
plist2json -i 2 input.plist
```

Use tab characters for indentation (bash or zsh):

```bash
plist2json -i $'\t' input.plist
```

Output compact JSON (no added whitespace):

```bash
plist2json -i "" input.plist
```


### Pipeline examples

Convert and save to a file:

```bash
plist2json input.plist > output.json
```

Process multiple plist files (bash or zsh):

```bash
for file in *.plist; do
    plist2json "$file" > "${file%.plist}.json"
done
```


### Use with `jq` to filter and process JSON output

```bash
# Extract a specific key's value
plist2json input.plist | jq '.someKey'
```

```bash
# Convert an array in the plist to CSV format
plist2json input.plist | jq -r '.anotherKey | @csv'
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


### Example 2: Compact output

```bash
$ plist2json -i "" example.plist
{"key1":"value1","key2":42,"array":["item1","item2"]}
```


### Example 3: Using in a shell script

```bash
#!/bin/bash
# Convert the `.array` to tab-separated values
plist2json example.plist | jq -r '.array | @tsv'
# Output:
#item1    item2    item3
```


## Error Handling

The tool provides clear error messages for common issues:

- **File not found**: `Error: File 'missing.plist' not found`
- **Invalid plist format**: `Error: Invalid plist format - <details>`
- **Other errors**: `Error: <error message>`


### Exit codes:

- `0`: Success
- `1`: Error occurred


## Development


### Running tests

```bash
python -m pytest tests/
```


### Publishing a release

The project includes a `publish.sh` script that automates the release process. It will:

- Update the version number in all project files
- Build wheel and source distribution packages
- Commit version changes and create a git tag
- Create a GitHub release with the built packages

#### Prerequisites

- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
- Python build tools (`build` and `twine` will be installed automatically)

#### Usage

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
