#!/usr/bin/env python3
"""Strip index.html down to the fragment the Claude Artifact viewer wants.

index.html is the single source of truth and a complete standalone page: it is what
GitHub Pages serves. The artifact viewer supplies its own doctype, <html>, <head> and
<body>, so publishing the same file twice would nest two documents. This writes a
copy with the wrapper removed and everything else byte-identical.

    python3 tools/artifact-body.py <output-path>
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "index.html"

# Everything the viewer injects itself, and the reset that only the standalone page needs.
DROP_PREFIXES = (
    "<!doctype html>", "<html", "</html>", "<head>", "</head>",
    "<body>", "</body>", '<meta charset=', '<meta name="viewport"',
    '<meta name="description"',
)
DROP_EXACT = ('<style>html,body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>',)


def body_only(text: str) -> str:
    kept = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped in DROP_EXACT:
            continue
        if stripped.lower().startswith(DROP_PREFIXES):
            continue
        kept.append(line)
    return "\n".join(kept).strip() + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    if not SOURCE.exists():
        print(f"no source page at {SOURCE}", file=sys.stderr)
        return 1
    out = pathlib.Path(sys.argv[1])
    out.parent.mkdir(parents=True, exist_ok=True)
    result = body_only(SOURCE.read_text(encoding="utf-8"))
    if "<title>" not in result:
        print("refusing to write: the fragment lost its <title>", file=sys.stderr)
        return 1
    out.write_text(result, encoding="utf-8")
    print(f"{out}  {len(result)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
