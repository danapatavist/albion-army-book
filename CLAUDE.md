# Albion Army Book — Claude Working Instructions

## Project
An unofficial fan-made Warhammer Fantasy Albion army book, presented as an interactive, battered **6th-edition-inspired army book**. The website looks like a physical codex, while the underlying information is a structured, navigable wiki.

## Branch and publication safety
- **Work on `albion-canon-library` for canon integration and experiments.**
- Do **not** merge into `main`, deploy unpublished lore, or alter the live website without explicit approval from the project owner.
- This repository is public; a draft branch is **not private**. Only fictional, shareable material belongs here.
- No personal details, raw chats, private experiences, or information about the creator may be introduced from external conversations.
- Draft lore files are not publication approval. Respect `publication: requires-approval`.

## Canon source of truth
- Read `lore/README.md`, `lore/CONTRIBUTING.md`, and individual `lore/**/*.md` entries.
- Stable IDs identify fictional subjects; do not derive identity or relationships from mutable display names.
- Canon entries distinguish established facts, developing ideas and unresolved questions.
- **Do not invent** characters, relationships, units, statistics, dates, places or background to fill gaps.
- Existing demo copy in `index.html` may be placeholder material; don't automatically treat it as canon.
- Preserve aliases and meaningful cross-references when names change.
- Suggest corrections and editorial changes for approval, rather than silently rewriting lore.

## Editorial and design contract
- Maintain the fixed **1920 × 1080 (16:9) design stage** that scales proportionally in the browser.
- Inside spreads are **two independent pages** separated by a visible gutter.
- **Default: two text columns per page** (four across a spread), not full-width body paragraphs.
- Allow headline spans, small inset illustrations, column art, ink drawings, half-page images, full-page plates, double-page spreads and maps.
- Keep text rendered as accessible, selectable HTML rather than rasterising entire pages.
- Visual direction: weathered parchment, 6th-edition Warhammer Fantasy army book, vintage print illustrations, legible editorial typography, restrained print wear.
- Asset names and their placements should be data-driven; artwork is separate from lore text.

## Wiki-to-book architecture
- Each lore article is a structured source, **not automatically a single physical page**.
- Build reusable codex page layouts to paginate or curate articles across spreads.
- Names and cross-references should link to the correct canonical entries, with navigation, chapter index and ultimately search.
- Avoid duplicating canonical article prose inside static HTML; plan a content loader/build pipeline suitable for GitHub Pages.
- The present website is a single `index.html` without a build step. Propose any architectural change before implementing it.
- Do not assume Markdown files are available on the published site until a loader/build/export step deliberately makes them available.

## How to coordinate with ChatGPT and the owner
- ChatGPT contributes draft fictional lore and asset direction to GitHub; Claude handles site implementation when requested.
- Read the latest commits on the draft branch before editing; don't overwrite parallel changes.
- Before broad changes, show a plan, identify impacted files, and request approval.
- Never commit directly to `main` as part of an unreviewed request.
- Share a brief summary of what changed and any unresolved editorial questions.

## Current next step
**Propose** a way to render the existing `lore/` articles as navigable, two-column codex pages on the draft branch, without breaking the current book. Do not implement until requested.
