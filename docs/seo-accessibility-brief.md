# Albion codex — SEO and accessibility acceptance criteria (draft implementation)

The project owner wants the fan-made Albion army book to be discoverable by people searching for **Warhammer Albion**, not only visually impressive once opened. This is a **development brief**, not permission to merge or publish.

## Indexability and document architecture
- Audit how the 1920×1080 interactive viewer exposes content to crawlers. Navigation inside a canvas/JS book alone is insufficient.
- Give each approved chapter, character, creature and unit a **stable crawlable HTML URL**, meaningful page `<title>`, unique meta description, visible `<h1>` and logical heading structure, with semantic text (not text rendered solely in canvas/images).
- Provide canonical URLs, human-readable internal links, XML sitemap, robots.txt that does not unintentionally block approved pages, and verify Google can fetch rendered content.
- Do not publish or index unapproved draft entries or the draft-preview export. Do not let SEO metadata leak draft text.
- Add relevant structured data accurately (e.g. CreativeWork or Article and BreadcrumbList where appropriate). No invented reviews, ratings or affiliation.
- Describe the project clearly as an **unofficial, fan-made Warhammer Fantasy Albion army book**, with no endorsement implied. Avoid keyword stuffing and misleading claims about official Games Workshop products.

## Image accessibility and search
- Images require accurate, concise descriptive alt text as data in the chapter/artwork configuration, and captions where meaningful. Decorative art may use empty alt text.
- Example for the Plaid Men engraving: `Blaewen Plaid Men wearing full bronze helmets and moustaches, tartan trousers beneath short kilts, advancing with spears and round shields through a smoky battle.`
- Use real text for image captions, descriptive filenames, dimensions/aspect ratios, modern formats and responsive loading that preserves legibility.
- Include image discoverability in sitemap/image data where supported; do not expose private or unapproved concept art.

## Technical quality
- Make first page load informative without requiring interaction; use server-rendered or prerendered/static HTML for the canonical landing and article views.
- Ensure descriptive link labels, keyboard navigation, responsive layout, appropriate contrast, correct image alt usage and good Core Web Vitals.
- Verify in a local draft-only audit that every approved article has accessible HTML and metadata. Report any limitations honestly.

## Publishing gate
Keep all changes on `albion-canon-library` until explicit owner approval. Changes to tags/templates are not approval for any `status: draft` lore or artwork. Share the audit and proposed architecture before large changes.
