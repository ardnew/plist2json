#!/usr/bin/env python3

import argparse
import json
import plistlib
import sys


def serialize_default(obj):
    """Handle non-serializable objects in JSON output."""
    return f"<<non-serializable: {type(obj).__name__}>>"


def read_plist(file_path=None):
    """Read plist from file or stdin."""
    if file_path:
        with open(file_path, 'rb') as f:
            return plistlib.load(f)
    else:
        return plistlib.loads(sys.stdin.read().encode("utf-8"))


def main():
    parser = argparse.ArgumentParser(description='Convert plist to JSON')
    parser.add_argument('-i', '--indent', type=str, default=None,
                        help='Indentation for JSON output (number of spaces or string)')
    parser.add_argument('file', nargs='?',
                        help='Input plist file (default: stdin)')
    args = parser.parse_args()

    try:
        indent = args.indent
        if indent is not None:
            try:
                indent = int(indent)
            except ValueError:
                pass
        
        data = read_plist(args.file)
        output = json.dumps(data, indent=indent,
                           default=serialize_default, ensure_ascii=False)
        print(output)
        return 0
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        return 1
    except plistlib.InvalidFileException as e:
        print(f"Error: Invalid plist format - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
