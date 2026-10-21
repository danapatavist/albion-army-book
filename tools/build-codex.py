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

# ---------------------------------------------------------------------------
# Publication safety: an allowlist, not a blacklist.
#
# A lore entry is a working document. It holds the fiction, and alongside it the
# notes that made the fiction: art direction, pointers to the creator's private
# reference images, unsettled rules, working names. Only the fiction is published.
#
# Deciding that by naming what to strip would be a blacklist, and a blacklist is
# wrong for this job: the next heading nobody thought of is published by default.
# So the rule is inverted. A section is set in the book only if its heading is named
# in codex-sections.json. Anything else - a new heading, a renamed one, a typo, a
# whole new entry - is withheld until someone admits it deliberately. A missing
# allowlist publishes nothing at all.
#
# The allowlist governs whole sections. A private reference can also sit inside an
# otherwise publishable sentence, which no heading can catch, so the text that
# survives the allowlist is scanned as well, and a publishable build that still
# carries one fails rather than shipping it.
# ---------------------------------------------------------------------------
SECTIONS_FILE = ROOT / "codex-sections.json"
OPENING = "(opening)"        # the prose before an entry's first heading

PRIVATE_IN_PRINT = [
    (re.compile(r"\bprivate\b[^.]{0,60}?\b(archive|artwork|art|collection|concept|"
                r"images?|folder|reference)\b", re.I), "a pointer to private material"),
    (re.compile(r"\bconcept (art|artwork|images?|sculpts?|miniature)\b", re.I),
     "a reference to concept art"),
    (re.compile(r"\b(miniature|visual|art) (reference|direction|development)\b", re.I),
     "a production note"),
    (re.compile(r"`[^`]*\.(png|jpe?g|webp|gif|psd|zip|docx?)`", re.I), "a source file path"),
    (re.compile(r"\bnot yet (one )?final approved\b", re.I), "an approval note"),
]

PLACES = {"spread", "full", "half", "column", "ink", "boxout", "marginal", "omit"}
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


def heading_key(text):
    """Headings are compared loosely, so punctuation or case cannot smuggle one past."""
    return re.sub(r"\s+", " ", text.strip().lower()).strip(".:;,—- ")


def allowlist(problems):
    """Read codex-sections.json: the sections that may be set in the book.

    Returns (allowed everywhere, allowed in one named article, withheld from one
    named article). An unreadable or absent file is not a reason to fall back to
    publishing everything, so it returns an empty allowlist, and an empty allowlist
    publishes nothing.

    `denyIn` narrows the allowlist for a single entry: it is how one entry's
    "Established lore" is held back when it carries something private, without
    stripping that heading from the twenty other entries that use it. It can only
    take away, never give, so the default stays deny.
    """
    if not SECTIONS_FILE.exists():
        problems.append("codex-sections.json is missing. Nothing can be published "
                        "without it: the publication allowlist is the gate.")
        return set(), {}, {}
    try:
        data = json.loads(SECTIONS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        problems.append(f"codex-sections.json is not valid JSON: {exc}")
        return set(), {}, {}

    def keys(headings):
        return {heading_key(h) for h in headings}

    everywhere = keys(data.get("allow", []))
    per_article = {a: keys(h) for a, h in (data.get("allowIn") or {}).items()}
    denied = {a: keys(h) for a, h in (data.get("denyIn") or {}).items()}
    for article, headings in denied.items():
        if "*" in headings:                      # the whole entry, whatever it holds
            denied[article] = everywhere | per_article.get(article, set())
    return everywhere, per_article, denied


def admit(article_id, blocks, everywhere, per_article, denied):
    """Split an entry into sections at its H2s and keep only the admitted ones.

    Block ids are not renumbered. They are handles for editorial overrides, and an
    override must not quietly move to a different paragraph because a section above
    it was withheld.
    """
    permitted = (everywhere | per_article.get(article_id, set())) - denied.get(article_id, set())
    kept, withheld = [], []
    in_opening, ok = True, heading_key(OPENING) in permitted
    for block in blocks:
        if block["type"] == "heading" and block.get("level") == 2:
            in_opening = False
            ok = heading_key(block["text"]) in permitted
            if not ok:
                withheld.append(block["text"])
        elif in_opening and not ok and OPENING not in withheld:
            withheld.append(OPENING)
        if ok:
            kept.append(block)
    return kept, withheld


def block_text(block):
    """Everything a block would print, as one string, for scanning."""
    if block.get("text"):
        return block["text"]
    if block.get("spans") is not None:
        return "".join(s.get("text", "") for s in block["spans"])
    return " ".join("".join(s.get("text", "") for s in item)
                    for item in block.get("items", []))


def private_references(blocks):
    """Private or production material surviving inside an otherwise public section."""
    found = []
    for block in blocks:
        text = block_text(block)
        for pattern, why in PRIVATE_IN_PRINT:
            hit = pattern.search(text)
            if hit:
                found.append((block["id"], why, hit.group(0).strip()))
                break
    return found


def spans(text, resolve, bold=False, italic=False):
    """Split a line into text, cross-reference, bold and italic spans.

    Inline markup nests: **[Honey Dragon](../artefacts/honey-dragon.md)** is a bold
    cross-reference, not a literal pair of brackets. So emphasis is not a span kind of
    its own; it is a flag carried by the spans inside it, and the parser recurses.
    """
    def mark(span):
        if bold:
            span["b"] = True
        if italic:
            span["i"] = True
        return span

    out, pos = [], 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            out.append(mark({"text": text[pos:m.start()]}))
        label, target, strong, em = m.groups()
        if label is not None:
            ref = resolve(target)
            out.append(mark({"ref": ref, "text": label} if ref else {"text": label}))
        elif strong is not None:
            out += spans(strong, resolve, True, italic)
        else:
            out += spans(em, resolve, bold, True)
        pos = m.end()
    if pos < len(text):
        out.append(mark({"text": text[pos:]}))
    return [s for s in out if s.get("text") != "" or "ref" in s]


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
    everywhere, per_article, denied = allowlist(problems)
    withheld_sections, emptied, private_hits = {}, [], []

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
        parsed_blocks, withheld = admit(article_id, parsed_blocks,
                                        everywhere, per_article, denied)
        if withheld:
            withheld_sections[article_id] = withheld
        private_hits += [(article_id,) + hit for hit in private_references(parsed_blocks)]
        if not parsed_blocks:
            # every section was withheld; an entry with nothing to set is not a page
            emptied.append(article_id)
            continue

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

    # Overrides are checked against the whole library, unfiltered: an override may
    # legitimately name a block the allowlist withholds today and admits tomorrow,
    # and it must not be reported as anchoring at nothing.
    library_block_ids = []
    for article_id, entry in parsed.items():
        library_block_ids += [b["id"] for b in blocks(entry["body"], lambda _t: None, article_id)]

    for article_id, items in directives(library_block_ids, problems).items():
        if article_id in articles:
            kept_ids = {b["id"] for b in articles[article_id]["blocks"]}
            articles[article_id]["layout"] = [d for d in items if d["at"] in kept_ids]

    if problems:
        print("the build cannot go ahead:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    # A private reference can hide inside a section the allowlist admits, so the text
    # that survived is scanned too. In a publishable build that is a hard stop.
    if private_hits and not include_drafts:
        print("private or production material in publishable text; not writing:", file=sys.stderr)
        for article_id, block_id, why, snippet in private_hits:
            print(f"  - {block_id}: {why} — {snippet!r}", file=sys.stderr)
        print("\nEdit the entry, or withhold its section in codex-sections.json.", file=sys.stderr)
        return 1

    codex = {
        "generated": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": "drafts-included" if include_drafts else "approved-only",
        "publishable": not include_drafts,
        "counts": {"included": len(articles), "withheld": len(skipped), "in_library": len(parsed)},
        "withheld": sorted(skipped, key=lambda s: s["id"]),
        "withheld_sections": {k: withheld_sections[k] for k in sorted(withheld_sections)},
        "withheld_entirely": sorted(emptied),
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
    no_alt = [d["art"] for d in all_overrides if d.get("art") and not d.get("alt")]
    if no_alt:
        print(f"  {len(no_alt)} artwork slot(s) with no alt text. A plate nobody can see is a "
              f"plate nobody can read:")
        for name in no_alt:
            print(f"    {name}")
    if missing_art:
        print(f"  {len(missing_art)} artwork file(s) not yet in lore/approved-artwork/, "
              f"each rendering as a holding box:")
        for name in missing_art:
            print(f"    {name}")
    if unresolved:
        print(f"  {len(unresolved)} unresolved cross-reference(s):")
        for u in unresolved:
            print(f"    {u['from']} -> {u['link']}")

    held = sum(len(v) for v in withheld_sections.values())
    if held:
        print(f"\n  {held} section(s) withheld by the publication allowlist, "
              f"across {len(withheld_sections)} entr(y/ies):")
        for article_id in sorted(withheld_sections):
            for name in withheld_sections[article_id]:
                print(f"    {article_id}: {name}")
    if emptied:
        print(f"\n  {len(emptied)} entr(y/ies) had no admitted section and are not set "
              f"at all: {', '.join(emptied)}")
    if private_hits:
        print(f"\n  {len(private_hits)} private or production reference(s) inside admitted "
              f"text. These would stop a publishable build:")
        for article_id, block_id, why, snippet in private_hits:
            print(f"    {block_id}: {why} — {snippet!r}")
    if include_drafts:
        print("\n  Draft preview. Not committable, and nothing reads it but you.")
    elif not articles:
        print("\n  No article is approved yet, so the codex is empty by design.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
