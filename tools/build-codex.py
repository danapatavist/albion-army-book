#!/usr/bin/env python3
"""Compile the lore library into codex.json, the data the book renders from.

Why a build step rather than fetching Markdown in the browser: the approval gate
becomes physical. A draft article is not hidden at runtime, it is never written into
the published file at all, so no bug in the site can leak one. It also keeps a
Markdown parser out of the browser and needs no CI — GitHub Pages serves the result
as a static file.

    python3 tools/build-codex.py                  # approved only -> codex.json
    python3 tools/build-codex.py --include-drafts # everything    -> codex.draft.json

codex.draft.json is gitignored. Previewing drafts locally is deliberately a dead end:
there is no path from it to the published site.

Articles are emitted as structured blocks, not HTML. The website decides how to set
them: which spread, which column, where the art goes. Cross-references between
articles are resolved to stable ids here, so the site never has to know about file
paths, and renaming a display name cannot break a link.

The book is art-directed, not text poured into columns, so every block carries a
stable id of the form "<article-id>:<n>". An editorial override names that id to
force a page break, pin an illustration beside a passage, give a passage a full page
or open it across a spread. Ids are assigned in document order and do not shift when
wording changes, only when blocks are added or removed. Any `layout:` key in an
article's front matter is passed through untouched for the same purpose; this build
reads none of it, so the vocabulary can be settled later without recutting the data.
"""
import datetime as _dt
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LORE = ROOT / "lore"
SKIP = {"README.md", "CONTRIBUTING.md", "TEMPLATE.md"}

PUBLISHABLE_STATUS = "approved"

PLACES = {"spread", "full", "half", "column", "ink"}
BREAKS = {"page", "spread"}
# one directive is a line of key=value pairs; quoted values may contain spaces

HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET = re.compile(r"^\s*[-*]\s+(.*)$")
# inline: [text](target) | **strong** | *emphasis*
INLINE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|\*([^*]+)\*")


def front_matter(text):
    """Return (front matter dict, body). Lists are read as repeated '- ' lines."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm, key = {}, None
    for line in text[3:end].splitlines():
        if not line.strip():
            continue
        bullet = BULLET.match(line)
        if bullet and key:
            fm.setdefault(key, [])
            if isinstance(fm[key], list):
                fm[key].append(bullet.group(1).strip().strip('"'))
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"')
            fm[key] = value if value else []
    return fm, text[end + 4:]


def directives(all_block_ids, problems):
    """Read codex-layout.json and check every override against the real blocks.

    Art direction lives here rather than in the lore entries: lore/CONTRIBUTING.md
    keeps artwork and layout independent of the canon text, so an editor can
    re-art-direct the book without touching a word of canon.

    An override naming a block that does not exist is an error, not a warning. Art
    must not go quietly missing because a paragraph was rewritten.
    """
    path = ROOT / "codex-layout.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        problems.append(f"codex-layout.json is not valid JSON: {exc}")
        return {}

    by_article = {}
    for d in data.get("overrides", []):
        at = d.get("at", "")
        if at not in all_block_ids:
            problems.append(f"override anchors at {at!r}, which is not a block in the lore library")
            continue
        if "place" in d and d["place"] not in PLACES:
            problems.append(f"{at}: place={d['place']} is not one of {', '.join(sorted(PLACES))}")
            continue
        if "break" in d and d["break"] not in BREAKS:
            problems.append(f"{at}: break={d['break']} is not one of {', '.join(sorted(BREAKS))}")
            continue
        if "place" not in d and "break" not in d:
            problems.append(f"{at}: override does nothing; it needs place= or break=")
            continue
        # art is referenced, never embedded; a file that is not there yet becomes a
        # holding box rather than a broken image, so pages can be art-directed early
        if d.get("art"):
            d = dict(d)
            d["missing"] = not (ROOT / "lore" / "approved-artwork" / d["art"]).is_file()
        by_article.setdefault(at.split(":")[0], []).append(d)

    for article_id, items in by_article.items():
        items.sort(key=lambda d: all_block_ids.index(d["at"]))
    return by_article


def spans(text, resolve):
    """Split a line into plain text, strong, emphasis and cross-reference spans."""
    out, pos = [], 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            out.append({"text": text[pos:m.start()]})
        label, target, strong, em = m.groups()
        if label is not None:
            ref = resolve(target)
            out.append({"ref": ref, "text": label} if ref else {"text": label})
        elif strong is not None:
            out.append({"strong": strong})
        else:
            out.append({"em": em})
        pos = m.end()
    if pos < len(text):
        out.append({"text": text[pos:]})
    return [s for s in out if s.get("text") != "" or "strong" in s or "em" in s or "ref" in s]


def blocks(body, resolve, article_id):
    """Parse the body into headings, paragraphs and lists. No HTML is produced."""
    out, para, items = [], [], []

    def flush():
        nonlocal para, items
        if para:
            out.append({"type": "p", "spans": spans(" ".join(para), resolve)})
            para = []
        if items:
            out.append({"type": "list", "items": [spans(i, resolve) for i in items]})
            items = []

    for raw in body.splitlines():
        line = raw.rstrip()
        head = HEADING.match(line)
        bullet = BULLET.match(line)
        if head:
            flush()
            level = len(head.group(1))
            # the body's own H1 repeats the front matter title; the site sets that itself
            if level > 1:
                out.append({"type": "heading", "level": level, "text": head.group(2).strip()})
        elif bullet:
            if para:
                flush()
            items.append(bullet.group(1).strip())
        elif not line.strip():
            flush()
        else:
            if items:
                flush()
            para.append(line.strip())
    flush()
    # stable handles for editorial overrides; document order, independent of wording
    for n, block in enumerate(out, 1):
        block["id"] = f"{article_id}:{n}"
    return out


def main(argv):
    include_drafts = "--include-drafts" in argv
    if not LORE.is_dir():
        print(f"no lore library at {LORE}", file=sys.stderr)
        return 1

    # never build on a library that fails its own checks
    check = subprocess.run([sys.executable, "-I", str(ROOT / "tools" / "canon-check.py")],
                           capture_output=True, text=True)
    if check.returncode != 0:
        print(check.stdout.strip(), file=sys.stderr)
        print("\ncanon-check failed; not building.", file=sys.stderr)
        return 1

    paths = sorted(p for p in LORE.rglob("*.md") if p.name not in SKIP)
    parsed = {}
    for path in paths:
        fm, body = front_matter(path.read_text(encoding="utf-8"))
        article_id = fm.get("id") or path.stem
        parsed[article_id] = {"path": path, "fm": fm, "body": body}

    by_path = {str(v["path"].resolve()): k for k, v in parsed.items()}
    unresolved = []

    def make_resolver(source):
        def resolve(target):
            if target.startswith(("http://", "https://", "#")):
                return None
            candidate = (source.parent / target.split("#")[0]).resolve()
            found = by_path.get(str(candidate))
            if not found:
                unresolved.append({"from": str(source.relative_to(ROOT)), "link": target})
            return found
        return resolve

    articles, aliases, skipped, problems = {}, {}, [], []
    for article_id, entry in parsed.items():
        fm = entry["fm"]
        status = fm.get("status", "")
        publishable = status == PUBLISHABLE_STATUS
        if not publishable and not include_drafts:
            skipped.append({"id": article_id, "status": status or "unknown"})
            continue

        article_aliases = fm.get("aliases") or []
        if isinstance(article_aliases, str):
            article_aliases = [article_aliases]

        parsed_blocks = blocks(entry["body"], make_resolver(entry["path"]), article_id)
        block_ids = [b["id"] for b in parsed_blocks]
        articles[article_id] = {
            "id": article_id,
            "title": fm.get("title", article_id),
            "kind": fm.get("kind", ""),
            "host": fm.get("host", ""),
            "status": status,
            "publication": fm.get("publication", ""),
            "aliases": article_aliases,
            "source": str(entry["path"].relative_to(ROOT)),
            "layout": [],   # filled in below, from codex-layout.json
            "blocks": parsed_blocks,
        }
        for name in [fm.get("title", "")] + article_aliases:
            if name:
                aliases[name] = article_id

    library_block_ids = []
    for article_id, entry in parsed.items():
        if article_id in articles:
            library_block_ids += [b["id"] for b in articles[article_id]["blocks"]]
        else:
            library_block_ids += [b["id"] for b in blocks(entry["body"], lambda _t: None, article_id)]

    for article_id, items in directives(library_block_ids, problems).items():
        if article_id in articles:
            articles[article_id]["layout"] = items

    if problems:
        print("layout overrides have problems; not writing:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    codex = {
        "generated": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": "drafts-included" if include_drafts else "approved-only",
        "publishable": not include_drafts,
        "counts": {"included": len(articles), "withheld": len(skipped), "in_library": len(parsed)},
        "withheld": sorted(skipped, key=lambda s: s["id"]),
        "unresolved_links": unresolved,
        "aliases": dict(sorted(aliases.items())),
        "articles": dict(sorted(articles.items())),
    }

    out = ROOT / ("codex.draft.json" if include_drafts else "codex.json")
    out.write_text(json.dumps(codex, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"{out.name}  {codex['mode']}")
    all_overrides = [d for a in articles.values() for d in a["layout"]]
    missing_art = [d["art"] for d in all_overrides if d.get("missing")]
    print(f"  {codex['counts']['included']} article(s) in, {codex['counts']['withheld']} withheld, "
          f"{len(aliases)} alias(es), {len(all_overrides)} override(s)")
    if missing_art:
        print(f"  {len(missing_art)} artwork file(s) not yet in lore/approved-artwork/, "
              f"each rendering as a holding box:")
        for name in missing_art:
            print(f"    {name}")
    if unresolved:
        print(f"  {len(unresolved)} unresolved cross-reference(s):")
        for u in unresolved:
            print(f"    {u['from']} -> {u['link']}")
    if include_drafts:
        print("\n  Draft preview. Not committable, and nothing reads it but you.")
    elif not articles:
        print("\n  No article is approved yet, so the codex is empty by design.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
