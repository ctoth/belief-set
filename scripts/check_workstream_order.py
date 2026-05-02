from __future__ import annotations

import re
import sys
from pathlib import Path


ITEM_RE = re.compile(r"^### (?P<id>[A-Z]+-\d+) ")
DEP_RE = re.compile(r"^\*\*Depends on:\*\* (?P<deps>.+)$")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_workstream_order.py <workstream.md>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    lines = path.read_text(encoding="utf-8").splitlines()
    seen: set[str] = set()
    current: str | None = None
    errors: list[str] = []

    for line_number, line in enumerate(lines, start=1):
        item_match = ITEM_RE.match(line)
        if item_match:
            item_id = item_match.group("id")
            current = item_id
            if item_id in seen:
                errors.append(f"{path}:{line_number}: duplicate item {item_id}")
            seen.add(item_id)
            continue

        dep_match = DEP_RE.match(line)
        if not dep_match or current is None:
            continue

        raw_deps = dep_match.group("deps").strip()
        if raw_deps == "none":
            continue

        for dependency in (item.strip() for item in raw_deps.split(",")):
            if dependency not in seen:
                errors.append(
                    f"{path}:{line_number}: {current} depends on {dependency}, "
                    "which has not appeared earlier",
                )

    for error in errors:
        print(error, file=sys.stderr)

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
