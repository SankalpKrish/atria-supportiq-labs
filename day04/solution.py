"""Audit dependency pins in a requirements file."""

import re

COMPARISON = re.compile(r"[<>=!~]+")
SUPPORTED_OPERATORS = {"==", ">=", "<="}


def parse_requirement(line):
    """Return the package name, supported operator, and version."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    comparison = COMPARISON.search(line)
    if comparison is None:
        return line, "", ""

    name = line[:comparison.start()].strip()
    operator = comparison.group()
    if operator not in SUPPORTED_OPERATORS:
        return name, "", ""

    version = line[comparison.end():].strip()
    return name, operator, version


def find_unpinned(lines):
    """Return the sorted names of requirements without an exact pin."""
    requirements = filter(None, map(parse_requirement, lines))
    return sorted(name for name, operator, _ in requirements if operator != "==")


def resolve_versions(lines):
    """Return the sorted package and version pairs for exact pins."""
    requirements = filter(None, map(parse_requirement, lines))
    return sorted((name, version) for name, operator, version in requirements if operator == "==")
