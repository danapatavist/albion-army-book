# Open editorial questions

Things the build or the review has turned up that the creator or ChatGPT needs to
settle. Nothing here is acted on unilaterally: the site flags, it does not rewrite
canon. Last swept 21 October 2026 against 33 draft entries.

## For ChatGPT to address

### Robin Antlers has no entry
`lore/cultures/court-of-antlers.md` introduces **Robin Antlers**, Elfred Sidesaddle's
husband, and is careful to distinguish him from **Robin Fair** of Field and Fenn. He
is at present the only named character in the library without a file of his own, so
nothing can link to him and the book cannot cross-reference him. He wants
`lore/characters/robin-antlers.md`.

### `lore/units/` is not a documented category
`lore/units/ram-chariots.md` sits in a folder that `lore/README.md` does not list
under **Proposed categories**. The build does not care — it reads the whole tree —
but the category list should either gain `units/` or the entry should move to an
existing folder. Worth settling before more unit entries are written.

### "Blue Host" and "Blaewen Ridings"
`lore/hosts/blue-host.md` is still titled **Blue Host**, while
`lore/characters/alfran-longbritches.md` establishes **Blaewen Ridings** as the
chosen name and calls Blue Host "the provisional label". The entry's own text says
older Blue Host references remain useful as a working cross-reference, so this may
be deliberate. If the Ridings is now the name, the entry wants renaming and
`aliases: [Blue Host]` adding so existing links keep working.

## Blocking a publishable build

These are sentences inside sections the publication allowlist admits, so no heading
can withhold them. While they stand, the moment any of these entries is approved,
`tools/build-codex.py` refuses to write `codex.json`. Each needs either rewording in
the entry, or its section withholding in `codex-sections.json`.

| block | what the scanner caught |
|---|---|
| `blinding-brass:4` | "The Green **concept artwork** shows…" |
| `alfran-longbritches:10` | "Three **private** miniature **concept** images depict her…" |
| `alfran-longbritches:18` | a **private concept** reference |
| `ocnesse:3` | "the existing Alfran-and-Shaggy miniature concept is the **visual reference**" |
| `ocnesse:7` | a second **visual reference** note |
| `host-orchestras:2` | "depicted in **private** Blaewen **concept** artwork" |
| `field-and-fenn-units:30` | a **concept art** reference |

The pattern in every case is the same: a note about *how the thing was designed* set
in prose that otherwise describes *the thing*. The fix is usually to describe the
subject and drop the sentence about the reference image.

## Settled

- **"Loch Ness-like".** `blue-host.md` and `alfran-longbritches.md` describe Shaggy
  as "a Loch Ness-like creature" where `ocnesse.md` names the species. The creator
  has ruled (21 Oct 2026) that this is descriptive shorthand for an Oc'nesse, not
  conflicting canon. No change needed in any entry.
