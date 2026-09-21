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
    column: int
    text: str = ""
    """Empty unless --show-lines is passed.

    The whole source line used to go into the report and into the JSON. A
    compact config with the model id and the API key on one line would then be
    copied straight into a CI log by a tool whose job is to prevent trouble.
    The file, the line and the column say where to look without quoting it.
    """

    @property
    def shutdown(self) -> date:
        return BY_MODEL[self.model].shutdown

    @property
    def replacement(self) -> str:
        return BY_MODEL[self.model].replacement

    @property
    def provider(self) -> str:
        return BY_MODEL[self.model].provider

    @property
    def replacement_dies(self) -> date | None:
        """The day the recommended replacement itself retires, when it does.

        Eight of Google's rows point at a model that is also on the list - the
        page tells you to move to something that has its own shutdown date.
        Migrating twice is a decision; not being told is not.
        """
        entry = BY_MODEL.get(self.replacement)
        return entry.shutdown if entry else None


def find_in_text(text: str, path: str = "<text>", show_lines: bool = False) -> list[Hit]:
    hits: list[Hit] = []
    for number, line in enumerate(text.splitlines(), start=1):
        for m in BOUNDED.finditer(line):
            hits.append(Hit(path, number, m.group(0), m.start() + 1,
                            line.strip()[:160] if show_lines else ""))
    return hits


def all_files(root: Path, exclude: tuple[str, ...] = ()) -> list[Path]:
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
            # full_match only exists from 3.13, while CI runs 3.11 too.
            if any(fnmatch(rel, pattern) for pattern in exclude):
                continue
        out.append(path)
    return sorted(out)


@dataclass(frozen=True)
class Result:
    """What was found, and what could not be looked at.

    The second half is the point. An earlier version returned only the hits, so
    a repository of .vue files, or one whose files were all unreadable, got
    "No retired identifiers found" - which reads as "you are fine" and was
    really "I did not look". Silence has to be distinguishable from a clean
    answer, so the counts come back with the hits and the CLI refuses to call
    an empty look a pass.
    """

    hits: list
    read: int
    skipped_suffix: int
    skipped_size: int
    unreadable: int

    @property
    def looked_at_nothing(self) -> bool:
        return self.read == 0


def scan(root: Path, exclude: tuple[str, ...] = (), show_lines: bool = False) -> Result:
    hits: list[Hit] = []
    read = skipped_suffix = skipped_size = unreadable = 0
    for path in all_files(root, exclude):
        if path.suffix.lower() not in TEXT_SUFFIX:
            skipped_suffix += 1
            continue
        try:
            if path.stat().st_size > MAX_BYTES:
                skipped_size += 1
                continue
        except OSError:
            unreadable += 1
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except (UnicodeDecodeError, OSError):
            unreadable += 1
            continue
        read += 1
        rel = path.relative_to(root) if root.is_dir() else path
        hits.extend(find_in_text(text, str(rel), show_lines))
    return Result(hits, read, skipped_suffix, skipped_size, unreadable)


def group_by_date(hits: list[Hit]) -> dict[date, list[Hit]]:
    grouped: dict[date, list[Hit]] = {}
    for hit in hits:
        grouped.setdefault(hit.shutdown, []).append(hit)
    return dict(sorted(grouped.items()))
