# Albion canon library

The source of record for Albion lore. Entries here are written and approved by the
creator; the interactive army book reads from them later. Nothing in this folder is
published to the site by being written — only by being approved and then deliberately
pulled in.

## Status lifecycle

Every entry carries a `status` in its front matter.

| status | meaning | may appear on the site |
|---|---|---|
| `draft` | being written or discussed; may be wrong | no |
| `review` | complete, waiting on the creator | no |
| `approved` | the creator has signed it off | yes |
| `superseded` | replaced by another entry; kept for the record | no |

`draft` is the default. An entry is only ever promoted by the creator, by hand.
No tool in this repo may change a status.

## Writing an entry

Copy `TEMPLATE.md` into the right folder, name the file in lowercase kebab-case after
the subject (`alfran-longbritches.md`, `the-small-hearth.md`), and fill it in.

Keep the four confidence levels from the bible — ESTABLISHED, DEVELOPING, UNKNOWN,
REJECTED — against individual facts, not just whole entries. A mostly-settled
character can still have an unsettled parent.

Where something is not known, write `[CANON TO CONFIRM: …]` and leave it. Do not fill
a gap with something plausible.

## What must not go in here

- Personal information of any kind: real names, addresses, emails, phone numbers,
  handles, employers, locations.
- Transcripts or excerpts of private conversations, from any tool or person. Write the
  decision that came out of a conversation, not the conversation.
- Anything copied from a published Games Workshop product. This project's lore is
  original to it.

`tools/canon-check.py` enforces the front matter and scans for the obvious shapes of
personal data. It is a safety net, not a substitute for reading what you commit.

## Folders

| folder | holds |
|---|---|
| `characters/` | named people and Ancients |
| `hosts/` | the four hosts as factions |
| `creatures/` | named beasts, monsters and kinds |
| `places/` | regions, coasts, sites |
| `history/` | events, ages, sequences |
| `cultures/` | institutions, customs, trade, sport, society |
| `magic/` | the pylons, druidic craft, how magic works |
| `artefacts/` | objects, relics, equipment |
| `approved-artwork/` | artwork the creator has approved for use |
