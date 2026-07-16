#!/usr/bin/env python3
"""Read-only structural audit for an evidence-tracked Markdown wiki."""

from __future__ import annotations

import argparse
import ast
import re
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

REQUIRED = {"title", "domain", "type", "status", "code_version", "last_verified", "tags", "sources", "related"}
STATUSES = {"draft", "source-checked", "verified", "partial", "design-only", "stale", "deprecated"}
LINK_RE = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, text
    data: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"\'')
    return data, text


def local_target(source: Path, raw: str) -> Path | None:
    target = raw.split("#", 1)[0].strip()
    if not target or target.startswith(("http://", "https://", "mailto:")):
        return None
    return (source.parent / target).resolve()


def list_value(raw: str) -> list[str]:
    try:
        value = ast.literal_eval(raw)
    except (SyntaxError, ValueError):
        return []
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []


def heading_fragments(text: str) -> set[str]:
    fragments: set[str] = set()
    for line in text.splitlines():
        if not line.startswith("#"):
            continue
        heading = line.lstrip("#").strip().lower()
        slug = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE).replace(" ", "-")
        slug = re.sub(r"-+", "-", slug).strip("-")
        if slug:
            fragments.add(slug)
    return fragments


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki", required=True, type=Path, help="Wiki root directory")
    parser.add_argument("--repo", type=Path, help="Repository root for frontmatter source paths; defaults to wiki parent")
    parser.add_argument("--exclude", action="append", default=[], help="Path component to exclude")
    args = parser.parse_args()

    root = args.wiki.resolve()
    repo = (args.repo or root.parent).resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    excludes = set(args.exclude) | {"templates", "legacy"}
    candidates = sorted(p for p in root.rglob("*.md") if not any(part in excludes for part in p.relative_to(root).parts))
    failures: list[str] = []
    pages: dict[Path, dict[str, str]] = {}
    texts: dict[Path, str] = {}
    inbound: Counter[Path] = Counter()
    graph: dict[Path, set[Path]] = defaultdict(set)

    exempt_frontmatter = {root / "log.md"}
    for path in candidates:
        meta, text = parse_frontmatter(path)
        texts[path] = text
        if path not in exempt_frontmatter:
            missing = REQUIRED - set(meta)
            if missing:
                failures.append(f"schema {path.relative_to(root)} missing={','.join(sorted(missing))}")
                continue
            if meta.get("status") not in STATUSES:
                failures.append(f"status {path.relative_to(root)} value={meta.get('status')!r}")
            for key in ("title", "domain", "type", "status", "code_version"):
                if not meta.get(key):
                    failures.append(f"empty {path.relative_to(root)} field={key}")
            pages[path] = meta
            for source in list_value(meta.get("sources", "")):
                if source.startswith(("http://", "https://")):
                    continue
                source_path = (repo / source.split("#", 1)[0]).resolve()
                if not source_path.exists():
                    failures.append(f"source-path {path.relative_to(root)} -> {source}")

        for raw in LINK_RE.findall(text):
            target = local_target(path, raw)
            if target is None:
                continue
            if not target.exists():
                failures.append(f"link {path.relative_to(root)} -> {raw}")
                continue
            if "#" in raw and target.is_file() and target.suffix == ".md":
                fragment = raw.split("#", 1)[1].strip().lower()
                target_text = target.read_text(encoding="utf-8")
                if fragment and fragment not in heading_fragments(target_text):
                    failures.append(f"fragment {path.relative_to(root)} -> {raw}")
            if target.suffix == ".md" and root in target.parents:
                graph[path].add(target)
                inbound[target] += 1

    titles: dict[str, list[Path]] = defaultdict(list)
    for path, meta in pages.items():
        titles[meta["title"]].append(path)
    for title, paths in titles.items():
        if len(paths) > 1:
            failures.append("duplicate-title " + title + " -> " + ",".join(str(p.relative_to(root)) for p in paths))

    entry = root / "README.md"
    reachable: set[Path] = set()
    queue = deque([entry]) if entry.exists() else deque()
    while queue:
        current = queue.popleft()
        if current in reachable:
            continue
        reachable.add(current)
        queue.extend(graph.get(current, ()))

    orphan_exempt = {entry, root / "log.md"}
    for path in pages:
        if path not in orphan_exempt and inbound[path] == 0:
            failures.append(f"orphan {path.relative_to(root)}")
        if path not in orphan_exempt and path not in reachable:
            failures.append(f"unreachable {path.relative_to(root)}")

    verified = [p for p, meta in pages.items() if meta.get("status") == "verified"]
    for path in verified:
        text = texts[path].lower()
        if "test" not in text and "runtime" not in text:
            failures.append(f"verified-without-evidence-marker {path.relative_to(root)}")

    print(f"wiki={root}")
    print(f"candidates={len(candidates)}")
    print(f"material_pages={len(pages)}")
    print(f"lifecycle={dict(sorted(Counter(m['status'] for m in pages.values()).items()))}")
    print(f"failures={len(failures)}")
    for failure in failures:
        print(f"  {failure}")
    print("result=" + ("PASS" if not failures else "FAIL"))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
