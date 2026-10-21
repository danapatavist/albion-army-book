# Claude handoff — codex integration review (draft only)

**Status:** implementation brief; NOT approval to publish or merge.
**Branch:** `albion-canon-library`.
**Live site:** `main` / GitHub Pages.

## Objective
Make a reviewable preview of the newer structured lore in the existing 6th-edition-style interactive Albion army book, while preserving the present live website and its 1920×1080 spreads (two text columns per page).

## Current state
- The draft branch contains `lore/**/*.md`, `CLAUDE.md`, `CODEX-LAYOUT.md`, `codex-layout.json`, `codex-chapters.json`, and tools including `build-codex.py` and `canon-check.py`.
- `lore/hosts/blue-host.md` still uses the old provisional heading **Blue Host** while `lore/characters/alfran-longbritches.md` establishes **Blaewen Ridings** as the preferred name. Keep the old term as alias/navigation label if useful; flag this editorial inconsistency rather than silently rewriting.
- Draft entries require individual approval. **Do not promote `status: draft` or `publication: requires-approval` to approved.**
- Some existing site text may be unverified demo copy. Do not treat it as canonical merely because it already appears in `index.html`.

## Requested work — propose first, then build a draft-only preview if approved
1. Review `CLAUDE.md`, `lore/README.md`, `lore/CONTRIBUTING.md`, `CODEX-LAYOUT.md`, current `index.html`, and the canon/build pipeline before editing.
2. Inventory the chapter map and draft lore against the existing site. Separate **already live**, **in draft canon**, and **not yet documented or still unresolved**.
3. Propose integration through the existing approved-only `codex.json` / local draft-preview separation, with page templates and editorial artwork slots. Avoid leaking draft content to GitHub Pages from a default build.
4. Preserve selectable HTML text, proper spreads, keyboard/page navigation, and the established visual style. Confirm no draft-only files are emitted to the deployable output.
5. Create a small, reviewable, non-published prototype on the draft branch ONLY after owner approval; report files changed and preview instructions.
6. Surface canon conflicts, artwork gaps and editorial questions; do not fill them by invention.

## Blaewen Ridings: fiction-only review checklist
- Alfran Longbritches, styled **Lord Excalibar of the Blaewen Ridings**; Sword in the Stone transported intact on a wagon rather than drawn.
- Alfran's modernization and creation of new Earls; barrow treasure and enclosure consequences.
- Northern Empress and her **Seventeen Standards** (concept image labelled Fourteen is an error).
- Alfran's mount Shaggy: an old bull **Oc'nesse**, a Warhammerian plesiosaur; a generic noble/hero Oc'nesse mount is a developing game/design concept, distinct from named Alfran on Shaggy.
- The Three: three tapestry-weaving knotwitches. Great Druid 'Old Berrick of the Barrel' is *provisional*, not established canon.
- Elfred Sidesaddle and the Court of Antlers, the Beast, Waiting Guard, war musicians and ram chariots: inventory what's documented, and list gaps for creator review. Do not expand or invent details.
- All four hosts have orchestras, a recent development to check with the creator before canon publication.

## Privacy and art boundaries
This is a **public repository, including this draft branch**. Do not upload original/private source images, unpublished ZIP collections, personal background, private jokes, behind-the-scenes explanations or raw conversation transcripts. Do not infer creator biography from fictional characters. Use only individually approved public-facing art/assets; use labelled placeholders for everything else.

## Hard stop
**No merge to `main`, no live deploy, no artwork upload, no publication-status changes without explicit owner approval.**
