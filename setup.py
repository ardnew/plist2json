#!/usr/bin/env python3
"""Setup script for plist2json."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="plist2json",
    version="0.1.1",
    author="ardnew",
    author_email="andrew@ardnew.com",
    description="Convert Apple plist files to JSON format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ardnew/plist2json",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "plist2json=pkg:main",
        ],
    },
)
