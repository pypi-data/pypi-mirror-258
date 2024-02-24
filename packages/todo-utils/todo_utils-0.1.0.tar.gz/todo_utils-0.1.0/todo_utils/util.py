"""Main functions for the todo-extractor script."""
import json
import re
import subprocess
import typing

TODO_REGEXP = "^.*TODO:.*"
FIXME_REGEXP = "^.*FIXME:.*"


def grep_cmd(search_string: str) -> typing.List[str]:
    """Returns the command to run the selected grep program including flags

    Prioritizes ripgrep (rg) and returns grep if rg is not installed.
    """
    cmd = ["grep", "-rn"]
    if not subprocess.run(
        "command -v rg", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    ).returncode:
        cmd = ["rg", "-n"]
    cmd.append(search_string)
    return cmd


def search_todos_indir(dir: str) -> typing.List[typing.Dict[str, str]]:
    """Search directory for TODO notes and return the commands"""

    r = subprocess.run(
        grep_cmd(TODO_REGEXP), cwd=dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
    )
    return [
        m.groupdict()
        for m in re.finditer(r"^(?P<file>.*):(?P<line>\d*):.*TODO:\s*(?P<comment>.*)", r.stdout, re.M)
    ]

def search_fixmes_indir(dir: str) -> typing.List[typing.Dict[str, str]]:
    """Search directory for FIXME notes and return the commands"""

    r = subprocess.run(
        grep_cmd(FIXME_REGEXP), cwd=dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
    )
    return [
        m.groupdict()
        for m in re.finditer(r"^(?P<file>.*):(?P<line>\d*):.*FIXME:\s*(?P<comment>.*)", r.stdout, re.M)
    ]


def serialize_result(search_result: list) -> str:
    """Serializes a list to JSON and return the string

    If the list cannot be serialized, an empty list will be returned.
    """
    try:
        return json.dumps(search_result, indent=2)
    except TypeError:
        # List contains non-serializable objects
        return "[]"


def search_todos(dir: str) -> str:
    """Searches in directory for TODO notes and returns JSON"""
    return search_todos_indir(dir)
    # return serialize_result(search_todos_indir(dir))

def search_fixmes(dir: str) -> str:
    """Searches in directory for FIXME notes and returns JSON"""
    return search_fixmes_indir(dir)
    # return serialize_result(search_fixmes_indir(dir))
