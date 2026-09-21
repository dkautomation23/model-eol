# -*- coding: utf-8 -*-
"""Finding retired model ids in source, without crying wolf.

The whole difficulty is that a retired id is a prefix of live ones. `gpt-4` dies
on 23 October; `gpt-4o`, `gpt-4o-mini` and `gpt-4.1` do not. `o1` dies; `o1-mini`
does not. A plain substring search reports every one of them and is then ignored
by the person reading it, which is the same as not running.

Two rules make it honest:

  * a match must not touch another identifier character on either side, so
    `gpt-4` cannot match inside `gpt-4o`;
  * the alternation is ordered longest first, so `gpt-4-turbo-2024-04-09` is
    reported as itself rather than as `gpt-4-turbo`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from fnmatch import fnmatch
from pathlib import Path

from .table import BY_MODEL, RETIREMENTS

ID_CHAR = r"A-Za-z0-9._-"
BOUNDED = re.compile(
    rf"(?<![{ID_CHAR}])(?:"
    + "|".join(re.escape(r.model) for r in sorted(RETIREMENTS, key=lambda r: -len(r.model)))
    + rf")(?![{ID_CHAR}])"
)

SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
    "target", ".mypy_cache", ".pytest_cache", "vendor",
}
TEXT_SUFFIX = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs", ".rs", ".go", ".rb",
    ".java", ".kt", ".cs", ".php", ".sh", ".ps1", ".yml", ".yaml", ".json",
    ".toml", ".ini", ".cfg", ".env", ".md", ".txt", ".ipynb", ".sql", ".tf",
}
MAX_BYTES = 2 * 1024 * 1024


@dataclass(frozen=True)
class Hit:
    path: str
    line: int
    model: str
    text: str

    @property
    def shutdown(self) -> date:
        return BY_MODEL[self.model].shutdown

    @property
    def replacement(self) -> str:
        return BY_MODEL[self.model].replacement


def find_in_text(text: str, path: str = "<text>") -> list[Hit]:
    hits: list[Hit] = []
    for number, line in enumerate(text.splitlines(), start=1):
        for m in BOUNDED.finditer(line):
            hits.append(Hit(path, number, m.group(0), line.strip()[:160]))
    return hits


def candidate_files(root: Path, exclude: tuple[str, ...] = ()) -> list[Path]:
    """Files worth reading. `exclude` takes globs relative to root.

    A repository that documents model identifiers - a changelog, a table, this
    tool's own table - matches itself. Without a way to exclude that, the report
    is mostly the documentation and the real call site is buried in it.
    """
    if root.is_file():
        return [root]
    out = []
    for path in root.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        if exclude:
            rel = path.relative_to(root).as_posix()
            # fnmatch, not PurePath.match: the latter does not expand ** and
            # full_match only exists from 3.13, while CI runs 3.10 too.
            if any(fnmatch(rel, pattern) for pattern in exclude):
                continue
        if path.suffix.lower() not in TEXT_SUFFIX:
            continue
        try:
            if path.stat().st_size > MAX_BYTES:
                continue
        except OSError:
            continue
        out.append(path)
    return sorted(out)


def scan(root: Path, exclude: tuple[str, ...] = ()) -> list[Hit]:
    hits: list[Hit] = []
    for path in candidate_files(root, exclude):
        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except (UnicodeDecodeError, OSError):
            continue
        rel = path.relative_to(root) if root.is_dir() else path
        hits.extend(find_in_text(text, str(rel)))
    return hits


def group_by_date(hits: list[Hit]) -> dict[date, list[Hit]]:
    grouped: dict[date, list[Hit]] = {}
    for hit in hits:
        grouped.setdefault(hit.shutdown, []).append(hit)
    return dict(sorted(grouped.items()))
