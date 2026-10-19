#!/usr/bin/env python3
"""Check the canon library before anything is committed or published.

Three jobs, in order of how much damage they prevent:

  1. Nothing reaches the site by accident. An entry is publishable only when it says
     status: approved and carries the creator's sign-off. This script never changes a
     status; it only reports what each entry claims.
  2. No personal data. Private information and conversation transcripts must not enter
     the repository, so the obvious shapes of it are flagged here.
  3. The front matter is consistent, so the entries can become wiki data later without
     a cleanup pass.

    python3 tools/canon-check.py            # check every entry
    python3 tools/canon-check.py --approved # list what is cleared for publication

Exit status is 1 if any entry fails.
"""
import datetime as _dt
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CANON = ROOT / "canon"
SKIP = {"README.md", "TEMPLATE.md"}

STATUSES = {"draft", "review", "approved", "superseded"}
CONFIDENCES = {"established", "developing", "unknown", ""}
REQUIRED = ("name", "type", "status")

# Shapes of personal data. Deliberately broad: a false positive costs a glance,
# a miss puts someone's details in a public repository.
PRIVATE = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "an email address"),
    (re.compile(r"(?<!\d)(?:\+\d{1,3}[\s-]?)?(?:\(?\d{3,5}\)?[\s-]?){2,4}\d{3,4}(?!\d)"), "a phone number"),
    (re.compile(r"\b\d{1,4}\s+[A-Z][a-z]+\s+(?:Road|Street|Lane|Avenue|Drive|Close|Way)\b"), "a street address"),
    (re.compile(r"^\s*(?:ChatGPT|Claude|User|Assistant|Me)\s*:", re.M), "a conversation transcript"),
    (re.compile(r"\bhttps?://(?:chat\.openai\.com|chatgpt\.com|claude\.ai)/\S+"), "a link to a private chat"),
]


def front_matter(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm = {}
    for line in text[3:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.split("#")[0].strip()
    return fm


def check(path):
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)
    problems = []

    for pattern, what in PRIVATE:
        if pattern.search(text):
            problems.append(f"looks like it contains {what}")

    fm = front_matter(text)
    if fm is None:
        problems.append("has no front matter; copy canon/TEMPLATE.md")
        return problems, None

    for key in REQUIRED:
        if not fm.get(key):
            problems.append(f"front matter is missing {key}")

    status = fm.get("status", "")
    if status and status not in STATUSES:
        problems.append(f"status '{status}' is not one of {', '.join(sorted(STATUSES))}")
    if fm.get("confidence", "") not in CONFIDENCES:
        problems.append(f"confidence '{fm['confidence']}' is not one of established, developing, unknown")

    if status == "approved":
        for key in ("approved_by", "approved_on"):
            if not fm.get(key):
                problems.append(f"is approved but has no {key}")
        if "[CANON TO CONFIRM" in text:
            problems.append("is approved but still carries a CANON TO CONFIRM marker")
    for key in ("updated", "approved_on"):
        value = fm.get(key, "")
        if value:
            try:
                _dt.date.fromisoformat(value)
            except ValueError:
                problems.append(f"{key} '{value}' is not a YYYY-MM-DD date")

    return problems, fm


def main(argv):
    if not CANON.is_dir():
        print(f"no canon library at {CANON}", file=sys.stderr)
        return 1

    entries = sorted(p for p in CANON.rglob("*.md") if p.name not in SKIP)
    if not entries:
        print("No entries yet. Copy canon/TEMPLATE.md into a folder to start one.")
        return 0

    only_approved = "--approved" in argv
    failed = 0
    counts = {}
    for path in entries:
        problems, fm = check(path)
        status = (fm or {}).get("status", "unknown")
        counts[status] = counts.get(status, 0) + 1
        if problems:
            failed += 1
            print(f"\n{path.relative_to(ROOT)}")
            for p in problems:
                print(f"  - {p}")
        elif only_approved and status == "approved":
            print(f"{path.relative_to(ROOT)}  {fm.get('name','')}")

    if not only_approved:
        print()
        for status in sorted(counts):
            print(f"{counts[status]:4d}  {status}")
        print(f"{len(entries):4d}  entries, {failed} with problems")
        print("\nOnly 'approved' entries may appear on the site.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
