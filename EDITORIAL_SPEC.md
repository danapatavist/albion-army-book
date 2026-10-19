# Warhammer: Albion — Editorial and Artwork Specification v1.1

## Project intent
Create an unofficial fan-made Albion army book as an interactive website that feels like a physically opened Warhammer Fantasy **6th-edition-era** army book. This is a nostalgic editorial experience, not a modern website with a fantasy skin. All artwork and lore must be original to this project; don't reproduce existing Games Workshop page artwork or assets. Display clear fan-project and AI-generated-artwork disclosures.

## Canvas and book behaviour
- Author each **two-page spread on a 1920 × 1080 (16:9) design canvas**.
- Scale the complete spread proportionally in browsers; don't require users to have a 1920 × 1080 display.
- Treat left and right pages as **independent pages**, with a centre gutter, binding shadow, visible page edges and consistent margins.
- Keep important faces, labels and body text out of the gutter.
- The landing view resembles a slightly damaged vintage cardboard box cover; entering opens the book.
- Navigation via chapter tabs, page-turn controls and keyboard arrows. Transitions restrained.

## NON-NEGOTIABLE TYPESETTING RULE
**Ordinary editorial pages use TWO text columns PER PAGE: FOUR total across the open spread.**
- Do not set lore paragraphs in one long full-page-width line.
- Each page has its own two-column text flow; do not flow text continuously across the gutter.
- A heading may span both columns *of its own page*.
- Images may sit in a single column, span the two columns on a page, or replace most/all of a page.
- Text should reflow around or above/below embedded art and marginal illustrations.
- Full-page art, maps, tables, army rosters and chapter openers are intentional exceptions to the standard two-column editorial grid.
- Avoid over-regularity: printed books alternate dense lore spreads, miniatures, diagrams, paintings and quiet spaces.

## Visual direction
- Reference mood: Warhammer Fantasy 6th-edition-era army books (roughly early 2000s), especially their editorial density and juxtaposition of paintings and monochrome sketches.
- Weathered cream parchment, muted inks, rust-red labels, dark serif body copy, archaic decorative display lettering, delicate borders, printed-on-paper texture and mild foxing.
- Occasional faded images, rough ink and slight misregistration; never sacrifice readability.
- A convincing page gutter and book depth, but no overpowering skeuomorphic effects.
- Art should feel printed *into* the page, not like floating web cards.
- Typeset all functional text in HTML/CSS, never embed it in generative artwork.

## Art production matrix
| Asset | Suggested aspect | Editorial use | Example Albion subject |
|---|---|---|---|
| Double-spread painting | 16:9 | Chapter opener / spectacle; protect centre gutter | Wild Hunt over the barrows |
| Full-page illustration | Approx 8:9 per page / responsive to real page box | Major hero or monster | Robin Fair, Old Shannok, Big Gul |
| Horizontal half-page | Approx 2:1 | Units, battlefield, regional scenes | Fennfolk reed boats |
| Vertical half-page | Approx 3:4 | Individual figure / standard | Hag, druid trio, Shriker |
| Column inset | Approx 1:1 or 3:4 | In-text support | Fox mask, bronze dagger, relic |
| Black-and-white ink drawing | Flexible; preferably transparent | Editorial illustration, anatomy, artefact study | Fimir brood, pylon, chariot |
| Spot illustration / marginalia | Flexible; transparent | Dividers, small accents | Reeds, wolves, knots, eggs |
| Miniature showcase plate | Flexible | Model range, captions, unit lineup | Host unit miniatures |
| Maps / diagrams | Page or inset | Geography and explanatory lore | Albion regions, pylon sites |
| Heraldry / symbols | Square / transparent | Chapter tabs, headings, marginalia | Four host emblems |
| Paper / page decorations | Full canvas or tiling | Paper, borders, gutter, printing wear | Base book treatment |

## Asset naming convention
Use descriptive lowercase kebab-case names prefixed by format and subject, for example:
- `spread-wild-hunt-barrows.webp`
- `page-robin-fair-portrait.webp`
- `half-h-fennfolk-reed-boats.webp`
- `half-v-druid-trio.webp`
- `column-robin-fox-mask.png`
- `ink-fimir-brood-mother.png`
- `spot-wolf-head.png`
- `heraldry-blue-host.png`
- `texture-parchment.webp`

Use PNG with alpha for cutouts, heraldry and ink illustration when needed; WEBP for large painted assets, with originals archived separately. Exact page-image dimensions should follow the measured usable page area in the implementation; crop/focal alignment is controlled in CSS.

## Editorial layout patterns
1. **Standard lore spread:** four text columns total (two per page), a two-column heading within one page, small ink spot art and one column inset.
2. **Illustrated lore spread:** left page two columns with interspersed ink art; right page painted half-page piece above two text columns.
3. **Character profile:** portrait taking most of one page; other page has two text columns, a small artefact sketch and a pull quote.
4. **Chapter opener:** dramatic full spread painting, little or no body text, large title carefully placed away from gutter.
5. **Unit entry:** two-column descriptions with a miniature plate, a rules box and a small equipment drawing.
6. **Map spread:** map on one page, two text columns on the opposite page with labels and diagram insets.

## Content and canon safeguard
The site must represent **the user's established Albion lore**, not improvise new canon. Named characters, host affiliations, histories, equipment and social customs require approval or a supplied lore bible. Until then, use unmistakable `LORE PENDING` placeholders. Never invent named heroes or statistics to fill a page. In particular, do not silently substitute invented characters for Robin Fair, Alfran Longbritches, Maddoc the Flame, Old Shannok or the known Albion roster.

## Transparency / legal
Include plainly visible copy equivalent to: `Unofficial fan-created fictional army book. Not affiliated with or endorsed by Games Workshop. Includes AI-generated illustrations.` Keep any official marks/trademarks acknowledged appropriately; don't imply a commercial licensed product.

## Immediate instructions to Claude
1. Preserve the existing live website's structure and working navigation unless changes are explicitly approved.
2. Implement and demonstrate the **two-column-per-page rule** on standard lore layouts.
3. Prepare reusable templates for the six editorial patterns above.
4. Make an asset manifest with filenames, roles, crop notes and missing/ready status.
5. Do not create or modify lore without the separate Albion canon handoff.
6. Use real page typography and replaceable external art assets; avoid baking page copy into backgrounds.
