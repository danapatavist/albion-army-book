# Myth, Barrows and Bronze

An interactive fan-made **Warhammer Fantasy army book for Albion**, built as a digital
codex rather than a website: a battered box lid that opens into two-page parchment
spreads you turn like a real book.

**Read it:** https://danapatavist.github.io/albion-army-book/

## What's in it

- The Isle — a map of Albion, and the history the stones remember
- The Four Hosts — Blue, Red, Green and Grey, seated at the Antler Throne, the Bronze Barrow, the Drowned Oak and Carn Dhu
- Characters — Gwyth Antlerborn, Maddoc Greystone, the Hag of Nine Teeth
- Monsters of Albion, with profiles
- The army list, points and army special rules
- A page of empty frames waiting for miniature photographs

Navigate by the fore-edge tabs, the contents page, the red cross-references in the
prose, the page edges, or the arrow keys.

## Build

There is no build step for the site. `index.html` is the single source of truth: one
self-contained page, which is exactly what GitHub Pages serves. Open the file, or
serve the folder.

The same page is also published as a Claude Artifact, whose viewer supplies its own
doctype, `<head>` and `<body>`. `tools/artifact-body.py` writes a copy with that
wrapper stripped and everything else byte-identical, so the two can never drift:

    python3 tools/artifact-body.py /path/to/fragment.html

Edit `index.html` and nothing else; the fragment is always generated, never kept.

## Disclaimer

This is an unofficial fan project. It is not a Games Workshop product and has no
connection to, or endorsement from, Games Workshop Limited.

Warhammer, Albion, Truthsayers, Dark Emissaries, Fenbeasts and all associated names,
marks and imagery are trademarks of Games Workshop Limited, used here without
permission and without challenge to their status. Nothing here is for sale.

The cover painting and the plates taken from it are AI-generated. The army, its four
hosts, its characters and its rules are invented for this book.
