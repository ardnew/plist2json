#!/bin/bash
set -e

# Check if version argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <version>"
    echo ""
    echo "Example: $0 0.2.0"
    echo ""
    echo "Optional: Provide release notes via stdin"
    echo "Example: echo 'Release notes here' | $0 0.2.0"
    exit 1
fi

VERSION="$1"

# Validate version format (basic semver check)
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version must be in semver format (e.g., 1.0.0)"
    exit 1
fi

echo "==> Preparing release version $VERSION"

# Update version in pyproject.toml
echo "==> Updating version in pyproject.toml"
sed -i.bak "s/^version = .*/version = \"$VERSION\"/" pyproject.toml

# Update version in setup.py
echo "==> Updating version in setup.py"
sed -i.bak "s/version=\"[^\"]*\"/version=\"$VERSION\"/" setup.py

# Update version in pkg/__init__.py
echo "==> Updating version in pkg/__init__.py"
sed -i.bak "s/__version__ = .*/__version__ = \"$VERSION\"/" pkg/__init__.py

# Clean up backup files
rm -f pyproject.toml.bak setup.py.bak pkg/__init__.py.bak

# Clean previous builds
echo "==> Cleaning previous builds"
rm -rf build/ dist/ *.egg-info

# Install/upgrade build tools
echo "==> Installing build tools"
pip install --quiet --upgrade build twine

# Build distribution packages
echo "==> Building distribution packages"
python -m build

# Verify the build
if [ ! -f "dist/plist2json-${VERSION}-py3-none-any.whl" ]; then
    echo "Error: Wheel package not found"
    exit 1
fi

if [ ! -f "dist/plist2json-${VERSION}.tar.gz" ]; then
    echo "Error: Source distribution not found"
    exit 1
fi

echo "==> Built packages:"
ls -lh dist/

# Commit version changes
echo "==> Committing version changes"
git add pyproject.toml setup.py pkg/__init__.py
git commit -m "Bump version to $VERSION"

# Create and push tag
echo "==> Creating git tag v$VERSION"
git tag -a "v$VERSION" -m "Release version $VERSION"
git push origin main
git push origin "v$VERSION"

# Check if stdin has content (release notes)
RELEASE_NOTES=""
if [ ! -t 0 ]; then
    # stdin is not a terminal, read from it
    RELEASE_NOTES=$(cat)
fi

# Create GitHub release
echo "==> Creating GitHub release"
if [ -n "$RELEASE_NOTES" ]; then
    # Use provided release notes
    gh release create "v$VERSION" \
        "dist/plist2json-${VERSION}-py3-none-any.whl" \
        "dist/plist2json-${VERSION}.tar.gz" \
        --title "v$VERSION" \
        --notes "$RELEASE_NOTES"
else
    # Auto-generate release notes
    gh release create "v$VERSION" \
        "dist/plist2json-${VERSION}-py3-none-any.whl" \
        "dist/plist2json-${VERSION}.tar.gz" \
        --title "v$VERSION" \
        --generate-notes
fi

echo "==> Release v$VERSION published successfully!"
echo ""
echo "Uploaded files:"
echo "  - plist2json-${VERSION}-py3-none-any.whl"
echo "  - plist2json-${VERSION}.tar.gz"
