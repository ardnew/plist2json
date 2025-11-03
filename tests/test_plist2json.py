#!/usr/bin/env python3
"""Comprehensive test suite for plist2json."""

import io
import json
import os
import plistlib
import pytest
import runpy
import subprocess
import sys
import tempfile
from unittest.mock import patch, MagicMock

from pkg.__main__ import main, read_plist, serialize_default


class TestSerializeDefault:
    """Test cases for serialize_default function."""
    
    def test_serialize_default_bytes(self):
        """Test serialization of bytes object."""
        result = serialize_default(b"test")
        assert result == "<<non-serializable: bytes>>"
    
    def test_serialize_default_custom_object(self):
        """Test serialization of custom object."""
        class CustomClass:
            pass
        obj = CustomClass()
        result = serialize_default(obj)
        assert result == "<<non-serializable: CustomClass>>"
    
    def test_serialize_default_datetime(self):
        """Test serialization of datetime object."""
        from datetime import datetime
        dt = datetime.now()
        result = serialize_default(dt)
        assert result == "<<non-serializable: datetime>>"


class TestReadPlist:
    """Test cases for read_plist function."""
    
    def test_read_plist_from_file(self):
        """Test reading plist from a file."""
        test_data = {"key": "value", "number": 42}
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            result = read_plist(temp_path)
            assert result == test_data
        finally:
            os.unlink(temp_path)
    
    def test_read_plist_from_stdin(self):
        """Test reading plist from stdin."""
        test_data = {"key": "value", "list": [1, 2, 3]}
        plist_bytes = plistlib.dumps(test_data)
        plist_str = plist_bytes.decode('utf-8')
        
        with patch('sys.stdin.read', return_value=plist_str):
            result = read_plist(None)
            assert result == test_data
    
    def test_read_plist_complex_data(self):
        """Test reading plist with complex nested data."""
        test_data = {
            "string": "test",
            "integer": 123,
            "float": 45.67,
            "boolean": True,
            "array": [1, "two", 3.0],
            "dict": {"nested": "value"}
        }
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            result = read_plist(temp_path)
            assert result == test_data
        finally:
            os.unlink(temp_path)


class TestMain:
    """Test cases for main function."""
    
    def test_main_with_file_default_indent(self):
        """Test main with file input and default indentation."""
        test_data = {"key": "value", "number": 42}
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            with patch('sys.argv', ['plist2json', temp_path]):
                with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                    result = main()
                    output = mock_stdout.getvalue()
                    assert result == 0
                    assert json.loads(output) == test_data
        finally:
            os.unlink(temp_path)
    
    def test_main_with_file_numeric_indent(self):
        """Test main with file input and numeric indentation."""
        test_data = {"key": "value", "array": [1, 2, 3]}
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            with patch('sys.argv', ['plist2json', '--indent', '2', temp_path]):
                with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                    result = main()
                    output = mock_stdout.getvalue()
                    assert result == 0
                    assert json.loads(output) == test_data
                    assert '\n' in output  # Should have newlines with indent
        finally:
            os.unlink(temp_path)
    
    def test_main_with_file_string_indent(self):
        """Test main with file input and string indentation."""
        test_data = {"key": "value"}
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            with patch('sys.argv', ['plist2json', '--indent', '\t', temp_path]):
                with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                    result = main()
                    output = mock_stdout.getvalue()
                    assert result == 0
                    assert json.loads(output) == test_data
                    assert '\t' in output  # Should have tabs
        finally:
            os.unlink(temp_path)
    
    def test_main_with_stdin(self):
        """Test main with stdin input."""
        test_data = {"key": "value", "number": 42}
        plist_bytes = plistlib.dumps(test_data)
        plist_str = plist_bytes.decode('utf-8')
        
        with patch('sys.argv', ['plist2json']):
            with patch('sys.stdin.read', return_value=plist_str):
                with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                    result = main()
                    output = mock_stdout.getvalue()
                    assert result == 0
                    assert json.loads(output) == test_data
    
    def test_main_with_stdin_and_indent(self):
        """Test main with stdin input and indentation."""
        test_data = {"key": "value"}
        plist_bytes = plistlib.dumps(test_data)
        plist_str = plist_bytes.decode('utf-8')
        
        with patch('sys.argv', ['plist2json', '-i', '4']):
            with patch('sys.stdin.read', return_value=plist_str):
                with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                    result = main()
                    output = mock_stdout.getvalue()
                    assert result == 0
                    assert json.loads(output) == test_data
    
    def test_main_file_not_found(self):
        """Test main with non-existent file."""
        with patch('sys.argv', ['plist2json', 'nonexistent.plist']):
            with patch('sys.stderr', new=io.StringIO()) as mock_stderr:
                result = main()
                error_output = mock_stderr.getvalue()
                assert result == 1
                assert "not found" in error_output
                assert "nonexistent.plist" in error_output
    
    def test_main_invalid_plist_format(self):
        """Test main with invalid plist format."""
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            f.write(b"This is not a valid plist file")
            temp_path = f.name
        
        try:
            with patch('sys.argv', ['plist2json', temp_path]):
                with patch('sys.stderr', new=io.StringIO()) as mock_stderr:
                    result = main()
                    error_output = mock_stderr.getvalue()
                    assert result == 1
                    assert "Invalid plist format" in error_output
        finally:
            os.unlink(temp_path)
    
    def test_main_with_non_serializable_objects(self):
        """Test main with non-serializable objects in plist."""
        # Create a plist with datetime which requires custom serialization
        from datetime import datetime
        test_data = {"key": "value", "date": datetime(2023, 1, 1, 12, 0, 0)}
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            with patch('sys.argv', ['plist2json', temp_path]):
                with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                    result = main()
                    output = mock_stdout.getvalue()
                    assert result == 0
                    # Datetime should be serialized by default handler
                    parsed = json.loads(output)
                    assert parsed["key"] == "value"
        finally:
            os.unlink(temp_path)
    
    def test_main_with_unicode_characters(self):
        """Test main with Unicode characters."""
        test_data = {"key": "café", "emoji": "🎉", "chinese": "你好"}
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            with patch('sys.argv', ['plist2json', temp_path]):
                with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                    result = main()
                    output = mock_stdout.getvalue()
                    assert result == 0
                    parsed = json.loads(output)
                    assert parsed["key"] == "café"
                    assert parsed["emoji"] == "🎉"
                    assert parsed["chinese"] == "你好"
        finally:
            os.unlink(temp_path)
    
    def test_main_with_empty_plist(self):
        """Test main with empty plist."""
        test_data = {}
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            with patch('sys.argv', ['plist2json', temp_path]):
                with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                    result = main()
                    output = mock_stdout.getvalue()
                    assert result == 0
                    assert json.loads(output) == {}
        finally:
            os.unlink(temp_path)
    
    def test_main_with_array_plist(self):
        """Test main with plist containing array as root."""
        test_data = [1, 2, 3, "four", {"five": 5}]
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            with patch('sys.argv', ['plist2json', temp_path]):
                with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                    result = main()
                    output = mock_stdout.getvalue()
                    assert result == 0
                    assert json.loads(output) == test_data
        finally:
            os.unlink(temp_path)
    
    def test_main_with_deeply_nested_structure(self):
        """Test main with deeply nested data structure."""
        test_data = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "value": "deep"
                        }
                    }
                }
            }
        }
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            with patch('sys.argv', ['plist2json', temp_path]):
                with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                    result = main()
                    output = mock_stdout.getvalue()
                    assert result == 0
                    assert json.loads(output) == test_data
        finally:
            os.unlink(temp_path)
    
    def test_main_exception_handling(self):
        """Test main with unexpected exception."""
        with patch('sys.argv', ['plist2json', 'test.plist']):
            with patch('pkg.__main__.read_plist', side_effect=Exception("Unexpected error")):
                with patch('sys.stderr', new=io.StringIO()) as mock_stderr:
                    result = main()
                    error_output = mock_stderr.getvalue()
                    assert result == 1
                    assert "Error:" in error_output
                    assert "Unexpected error" in error_output
    
    def test_main_short_indent_option(self):
        """Test main with short indent option -i."""
        test_data = {"key": "value"}
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            with patch('sys.argv', ['plist2json', '-i', '2', temp_path]):
                with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                    result = main()
                    output = mock_stdout.getvalue()
                    assert result == 0
                    assert json.loads(output) == test_data
        finally:
            os.unlink(temp_path)
    
    def test_main_indent_zero(self):
        """Test main with zero indentation."""
        test_data = {"key": "value"}
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            with patch('sys.argv', ['plist2json', '--indent', '0', temp_path]):
                with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                    result = main()
                    output = mock_stdout.getvalue()
                    assert result == 0
                    assert json.loads(output) == test_data
        finally:
            os.unlink(temp_path)
    
    def test_main_with_boolean_values(self):
        """Test main with boolean values."""
        test_data = {"true_value": True, "false_value": False}
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            with patch('sys.argv', ['plist2json', temp_path]):
                with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                    result = main()
                    output = mock_stdout.getvalue()
                    assert result == 0
                    parsed = json.loads(output)
                    assert parsed["true_value"] is True
                    assert parsed["false_value"] is False
        finally:
            os.unlink(temp_path)
    
    def test_main_with_float_values(self):
        """Test main with float values."""
        test_data = {"float": 3.14159, "negative": -2.71828}
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            with patch('sys.argv', ['plist2json', temp_path]):
                with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                    result = main()
                    output = mock_stdout.getvalue()
                    assert result == 0
                    parsed = json.loads(output)
                    assert abs(parsed["float"] - 3.14159) < 0.00001
                    assert abs(parsed["negative"] - (-2.71828)) < 0.00001
        finally:
            os.unlink(temp_path)
    
    def test_main_with_special_characters_in_filename(self):
        """Test main with special characters in filename."""
        test_data = {"key": "value"}
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, 
                                        prefix='test file ', suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            with patch('sys.argv', ['plist2json', temp_path]):
                with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                    result = main()
                    output = mock_stdout.getvalue()
                    assert result == 0
                    assert json.loads(output) == test_data
        finally:
            os.unlink(temp_path)


class TestMainAsScript:
    """Test running as script."""
    
    def test_main_when_run_as_module(self):
        """Test the if __name__ == '__main__' block."""
        test_data = {"key": "value"}
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            # Test by importing the module with __name__ set to '__main__'
            result = subprocess.run(
                [sys.executable, '-m', 'pkg', temp_path],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0
            assert json.loads(result.stdout) == test_data
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_main_script_direct_execution(self):
        """Test direct execution of __main__.py script."""
        test_data = {"key": "value"}
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            # Test by running the __main__.py file directly
            result = subprocess.run(
                [sys.executable, 'pkg/__main__.py', temp_path],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0
            assert json.loads(result.stdout) == test_data
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_main_name_guard(self):
        """Test the __name__ == '__main__' guard using runpy."""
        test_data = {"key": "value"}
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.plist') as f:
            plistlib.dump(test_data, f)
            temp_path = f.name
        
        try:
            with patch('sys.argv', ['pkg.__main__', temp_path]):
                with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                    with pytest.raises(SystemExit) as exc_info:
                        # Run the module as __main__ which will execute line 56
                        runpy.run_module('pkg', run_name='__main__', alter_sys=True)
                    
                    assert exc_info.value.code == 0
                    output = mock_stdout.getvalue()
                    assert json.loads(output) == test_data
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
