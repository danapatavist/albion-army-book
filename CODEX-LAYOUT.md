# Editorial overrides

The book is art-directed. Text flows into columns automatically, but any page can be
taken over by hand, and the hand always wins.

An override is one line in an entry's `layout:` front matter, anchored to a block id.
Block ids come from the build (`blue-host:7`) and follow document order, so they are
stable while wording changes and only move when blocks are added or removed.

```yaml
layout:
  - at=blue-host:1 place=spread art=spread-blue-court.webp caption="Alfran's court"
  - at=blue-host:4 place=half art=half-h-ram-riders.webp caption="Javelin ram riders"
  - at=blue-host:6 place=column art=column-war-dog.png
  - at=blue-host:7 break=page
```

Each line is `key=value` pairs. Values with spaces take double quotes. Order does not
matter; the build sorts directives by the position of the block they anchor to.

## Keys

| key | values | meaning |
|---|---|---|
| `at` | a block id | the block the directive attaches to. Required. |
| `place` | `spread` `full` `half` `column` `ink` | where artwork sits relative to that block |
| `art` | a filename | the artwork, from `lore/approved-artwork/`. Omit it and the slot renders as a marked holding box naming what is wanted. |
| `caption` | text | printed under the art |
| `break` | `page` `spread` | start the next page, or the next spread, before this block |

`place` and `break` can appear on the same line: the break happens first, then the
art is placed at the top of the new page.

## What each placement does

- **`spread`** — the next two facing pages are one painting. Body text resumes after
  it. Use for a chapter opener or a set piece.
- **`full`** — the artwork takes a whole page. The facing page keeps its two columns.
- **`half`** — the artwork spans both columns of its page; text continues beneath.
- **`column`** — the artwork sits in one column at that point and the text flows past.
- **`ink`** — as `column`, but printed flat into the paper: no frame, monochrome,
  multiplied into the parchment.

## Rules the build enforces

- An `at` that names no real block is an error, not a warning. A renamed or deleted
  block breaks the build rather than silently losing its art.
- `place` and `break` must be one of the listed values.
- Artwork is referenced, never embedded. A missing file is a holding box, never a
  broken image.
- Overrides are editorial, so they live with the entry they affect. The chapter map
  decides what order articles appear in; it does not decide how a page looks.

## Chapters

`codex-chapters.json` lists chapters and the article ids each one runs, in order.
This is the file to edit to re-order the book.

```json
{
  "chapters": [
    { "id": "four-hosts", "title": "The Four Hosts", "tab": "The Hosts",
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

All of it only ever moves blocks between the two columns of the same page, so reading
order is never disturbed.
