#!/usr/bin/env python3

import subprocess
import sys
from enum import Enum
from pathlib import Path
import tomli
import tomli_w
import typer
from typing import Optional

class VersionBump(str, Enum):
    PATCH = "patch"
    MINOR = "minor"
    MAJOR = "major"

def get_git_status() -> tuple[bool, bool]:
    """Returns (has_changes, is_up_to_date)"""
    # Check for pending changes
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    has_changes = bool(result.stdout.strip())
    
    # Check if branch is up to date
    subprocess.run(["git", "remote", "update"], capture_output=True)
    result = subprocess.run(["git", "status", "-uno"], capture_output=True, text=True)
    is_up_to_date = "Your branch is up to date" in result.stdout
    
    return has_changes, is_up_to_date

def bump_version(current_version: str, bump_type: VersionBump) -> str:
    major, minor, patch = map(int, current_version.split('.'))
    
    if bump_type == VersionBump.MAJOR:
        major += 1
        minor = 0
        patch = 0
    elif bump_type == VersionBump.MINOR:
        minor += 1
        patch = 0
    else:  # PATCH
        patch += 1
    
    return f"{major}.{minor}.{patch}"

def main(
    bump_type: VersionBump = typer.Option(
        VersionBump.PATCH,
        "--bump",
        "-b",
        help="Version part to bump: patch, minor, or major",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-d",
        help="Print commands without executing them",
    ),
):
    """
    Helper script to release a new version of live-differ.
    Checks git status, bumps version, and prints git commands to execute.
    """
    # Check git status
    has_changes, is_up_to_date = get_git_status()
    
    if has_changes:
        typer.secho("Error: You have pending changes. Please commit or stash them first.", fg="red")
        raise typer.Exit(1)
    
    if not is_up_to_date:
        typer.secho("Error: Your branch is not up to date with remote. Please pull first.", fg="red")
        raise typer.Exit(1)
    
    # Read current version from pyproject.toml
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        typer.secho("Error: pyproject.toml not found", fg="red")
        raise typer.Exit(1)
    
    with open(pyproject_path, "rb") as f:
        pyproject = tomli.load(f)
    
    current_version = pyproject["project"]["version"]
    new_version = bump_version(current_version, bump_type)
    
    # Update pyproject.toml
    pyproject["project"]["version"] = new_version
    with open(pyproject_path, "wb") as f:
        tomli_w.dump(pyproject, f)
    
    # Print commands
    commands = [
        f"git add pyproject.toml",
        f'git commit -m "chore: bump version to v{new_version}"',
        f"git tag v{new_version}",
        f"git push origin main v{new_version}",
    ]
    
    typer.secho(f"\nVersion bumped from v{current_version} to v{new_version}", fg="green")
    typer.secho("\nRun these commands to complete the release:", fg="blue")
    for cmd in commands:
        typer.secho(f"{cmd}", fg="yellow")

if __name__ == "__main__":
    typer.run(main)
