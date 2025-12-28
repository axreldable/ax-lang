#!/usr/bin/env python3
"""
Script to bump version in pyproject.toml
Supports patch, minor, and major version bumps following semantic versioning.
"""

import argparse
import re
import sys
from pathlib import Path


def parse_version(version_str: str) -> tuple[int, int, int]:
    """Parse version string into major, minor, patch components."""
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version_str.strip())
    if not match:
        raise ValueError(f"Invalid version format: {version_str}")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def format_version(major: int, minor: int, patch: int) -> str:
    """Format version components into string."""
    return f"{major}.{minor}.{patch}"


def bump_version(version_str: str, bump_type: str) -> str:
    """Bump version according to type (patch, minor, major)."""
    major, minor, patch = parse_version(version_str)

    if bump_type == "patch":
        patch += 1
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")

    return format_version(major, minor, patch)


def update_pyproject_version(pyproject_path: Path, new_version: str) -> str:
    """Update version in pyproject.toml and return the old version."""
    content = pyproject_path.read_text()

    # Find current version
    version_pattern = r'^version\s*=\s*"([^"]+)"'
    match = re.search(version_pattern, content, re.MULTILINE)

    if not match:
        raise ValueError("Could not find version in pyproject.toml")

    old_version = match.group(1)

    # Replace version
    new_content = re.sub(
        version_pattern,
        f'version = "{new_version}"',
        content,
        count=1,
        flags=re.MULTILINE,
    )

    pyproject_path.write_text(new_content)

    return old_version


def main():
    parser = argparse.ArgumentParser(description="Bump version in pyproject.toml")
    parser.add_argument(
        "bump_type", choices=["patch", "minor", "major"], help="Type of version bump"
    )
    parser.add_argument(
        "--pyproject",
        type=Path,
        default=Path("python/pyproject.toml"),
        help="Path to pyproject.toml (default: python/pyproject.toml)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print new version without updating file"
    )

    args = parser.parse_args()

    if not args.pyproject.exists():
        print(f"Error: {args.pyproject} not found", file=sys.stderr)
        sys.exit(1)

    # Read current version
    content = args.pyproject.read_text()
    version_match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)

    if not version_match:
        print("Error: Could not find version in pyproject.toml", file=sys.stderr)
        sys.exit(1)

    current_version = version_match.group(1)
    new_version = bump_version(current_version, args.bump_type)

    if args.dry_run:
        print(f"Current version: {current_version}")
        print(f"New version: {new_version}")
    else:
        old_version = update_pyproject_version(args.pyproject, new_version)
        print(f"Bumped version from {old_version} to {new_version}")
        # Output for GitHub Actions
        print(f"::set-output name=old_version::{old_version}")
        print(f"::set-output name=new_version::{new_version}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
