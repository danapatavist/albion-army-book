# Editorial overrides

The book is art-directed. Text flows into columns automatically, but any page can be
taken over by hand, and the hand always wins.

Overrides live in `codex-layout.json`, not in the lore entries. `lore/CONTRIBUTING.md`
keeps artwork and layout independent of the canon text, so the book can be
re-art-directed without touching a word of canon.

Each override is anchored to a block id. Block ids come from the build
(`blue-host:7`) and follow document order, so they are stable while wording changes
and only move when blocks are added or removed.

```json
{
  "overrides": [
    { "at": "blue-host:1", "place": "spread", "art": "spread-blue-court.webp",
      "caption": "Alfran's court" },
    { "at": "blue-host:4", "place": "half", "art": "half-h-ram-riders.webp" },
    { "at": "blue-host:6", "place": "column", "art": "column-war-dog.png" },
    { "at": "blue-host:9", "place": "boxout", "label": "The Waiting Guard" },
    { "at": "blue-host:11", "place": "marginal", "label": "Awaiting the creator" },
    { "at": "blue-host:13", "place": "omit" }
  ]
}
```

Order does not matter; the build sorts directives by the position of the block they
anchor to. Any key beginning with `_` is a comment and is ignored.

## Keys

| key | values | meaning |
|---|---|---|
| `at` | a block id | the block the directive attaches to. Required. |
| `place` | `spread` `full` `half` `column` `ink` `boxout` `marginal` `omit` | what happens at that block |
| `art` | a filename | the artwork, from `lore/approved-artwork/`. Omit it and the slot renders as a marked holding box naming what is wanted. |
| `caption` | text | printed under the art |
| `label` | text | the heading on a boxout or a margin note. Defaults to the passage's own heading. |
| `open` | `false` | a margin note set as settled rather than as an open question |
| `break` | `page` `spread` | start the next page, or the next spread, before this block |

`place` and `break` can appear in the same override: the break happens first, then
the placement is made at the top of the new page.

## What each placement does

- **`spread`** — the next two facing pages are one painting. Body text resumes after
  it. Use for a chapter opener or a set piece.
- **`full`** — the artwork takes a whole page. The facing page keeps its two columns.
- **`half`** — the artwork spans both columns of its page; text continues beneath.
- **`column`** — the artwork sits in one column at that point and the text flows past.
- **`ink`** — as `column`, but printed flat into the paper: no frame, monochrome,
  multiplied into the parchment.
- **`boxout`** — a framed panel of related text. Unlike the art placements, a boxout
  takes the passage itself: the heading named by `at` and everything under it until
  the next heading of the same rank or higher. Those blocks are set in the panel and
  do not also appear in the running text.
- **`marginal`** — the same passage, hung instead in the outer margin as a note. The
  rail is a margin, not a third column: the page still carries two columns of text.
  Notes are dashed by default, which reads as an open question; `open=false` sets one
  as settled.
- **`omit`** — the passage is not set at all. For production notes that belong to the
  library rather than to the book: art direction for the illustrator, pointers to
  private source material, working notes between the creator and the editors.

### Where a boxout ends up

A boxout is tried first as a panel inside the column, where the reader meets it. That
wastes no paper and keeps the passage in its place. A passage too deep for a column is
promoted to a whole page, still set in two columns inside the frame. Only a passage
too long even for that falls back to running text, with a warning on the console. A
boxout is never cropped.

### Where a margin note ends up

A rail narrows the text, so it has to be hung before anything flows onto the page. A
note is therefore declared for its article and hung on the first page of that article
with room for it, filling the rail in order; the rest wait for the next page. If a
page is later given over to a plate or a full-page boxout, its notes are handed back
and hang on the page after.

## Rules the build enforces

- An `at` that names no real block is an error, not a warning. A renamed or deleted
  block breaks the build rather than silently losing its art.
- `place` and `break` must be one of the listed values.
- Nothing is ever cropped to make a placement work. A boxout too long for a panel is
  promoted or demoted; a list or a paragraph longer than a column is continued in the
  next one, as a printed book does it.
- Artwork is referenced, never embedded. A missing file is a holding box, never a
  broken image.
- Overrides are editorial, so they live in `codex-layout.json`, away from the canon.
  The chapter map decides what order articles appear in; it does not decide how a
  page looks.

## Chapters

`codex-chapters.json` lists chapters and the article ids each one runs, in order.
This is the file to edit to re-order the book.

```json
{
  "chapters": [
    { "id": "four-hosts", "title": "The Four Hosts", "tab": "Four Hosts",
      "articles": ["four-hosts", "blue-host", "red-host", "green-host", "grey-host"] }
  ]
}
```

An article is content, not a page. A chapter is paginated into as many spreads as its
text and its overrides need.

## What the book does on its own

Overrides are the hand. Everything the hand does not specify is composed
automatically, once the text has been measured:

- **Folios.** Every page is numbered by its position, front matter in roman and the
  body in arabic. Inserting a chapter renumbers what follows; nothing is written into
  the markup.
- **Column balance.** A page the text did not fill has its two columns evened up, so
  an article does not end with one full column beside an empty one.
- **Orphan control.** A heading is never left stranded at the foot of a column.
- **Tailpieces.** A page where an article *ends* short is closed with an ornament
  rather than trailing off into blank paper. A page whose text continues overleaf
  gets nothing — a tailpiece means "this ends here".
- **Blank pages.** A facing page with nothing on it takes a centred ornament and its
  folio, the way a printed book does.
- **The thumb index.** Each chapter's `tab` becomes one tab on the table beside the
  book. The lane is 120px wide, so the index runs in up to two banks and never covers
  a page. Keep tabs short: they are set vertically.

All of it only ever moves blocks between the two columns of the same page, so reading
order is never disturbed.

## Links into the book

A bare fragment opens a chapter, an article or a page:

```
index.html#blaewen                     a chapter tab
index.html#alfran-longbritches         an article
index.html#43                          page 43 of the book
index.html?codex=1                     the approved codex, on top of the hand-set book
index.html?codex=1&drafts=1            the local draft preview (never published)
```
