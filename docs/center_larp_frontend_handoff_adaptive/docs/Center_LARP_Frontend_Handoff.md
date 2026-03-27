# Center LARP Front-end Handoff

## 1. Project framing

This handoff is for the **public-facing front end** of the LARP site at `center.larp.co.il`.

The site should combine the two provided references into one coherent language:

- The uploaded HTML brings a **dark editorial rhythm**: narrow measure, restrained typography, thin dividers, faction rows, quiet animation, and a literary tone.
- The uploaded poster brings a **printed Tel Aviv broadside**: parchment paper, skyline line art, ribbon/banner framing, centered title composition, and sun-faded ink.

The result should feel like:

> **A municipal occult poster for Tel Aviv — printed on paper, haunted by agreements, and still rooted in the city.**

This is **not** medieval fantasy, **not** cyberpunk, and **not** a glossy event-product landing page.

## 2. Design north star

### Working style name
**Paper, Asphalt, and Salt**

### One-line brief
A secret agreement between the city and the supernatural, presented as a Tel Aviv cultural poster, a city notice, and a magical contract at the same time.

### Core qualities

- Urban
- Literary
- Local
- Airy
- Slightly archival
- Slightly official
- Slightly haunted
- Restrained rather than ornamental

### Things to avoid

- Generic dark fantasy UI
- Neon / cyberpunk treatment
- Medieval ornament
- SaaS gradients and pill buttons
- Stock fantasy imagery
- Overdesigned “magical” effects

## 3. Visual translation of the source material

### Keep from the current HTML
- Narrow editorial reading column
- Strong vertical rhythm
- Thin rules and dividers
- Faction list as disciplined rows
- Quote interlude
- Serious, literary typographic tone
- Subtle motion only

### Add from the poster
- Warm paper background
- Centered hero composition
- Ribbon / banner motif
- Skyline line art at the foot of the hero
- Marginalia: clouds, birds, wave lines, stamp-like details
- Printed-ephemera feel instead of all-dark noir

### Final balance
The site should be **light-first with dark undertones**.

Use paper as the main field. Use charcoal or night tones as accents, insets, or emphasis blocks rather than the default page background.

## 4. Brand keywords and tonal rules

### Keywords
- Municipal occult
- Coastal noir
- Literary urban fantasy
- Tel Aviv broadside
- Hidden agreements
- Cultural poster
- Paper archive
- Sea air, concrete, and ink

### Tone of voice for UI copy
- Direct
- Elegant
- Sparse
- Hebrew-first
- Specific
- Slightly poetic, never melodramatic

### UI writing rules
- Prefer short declarative labels.
- Metadata should read like program notes or noticeboard labels.
- Use mystery through implication, not exposition.
- Error/success messaging should stay calm and precise.

## 5. Exact design tokens

### 5.1 Color system

| Token | Value | Use |
|---|---:|---|
| `--clr-paper-0` | `#f5efe5` | Main page background |
| `--clr-paper-1` | `#ede2d3` | Elevated paper cards / light blocks |
| `--clr-paper-2` | `#d8ccb9` | Paper edge / warm contrast |
| `--clr-ink-0` | `#332c26` | Primary text |
| `--clr-ink-1` | `#5c5349` | Secondary text |
| `--clr-ink-2` | `#81776a` | Muted metadata |
| `--clr-sea-0` | `#71868d` | Main accent, links, selected states |
| `--clr-sea-1` | `#8fa1a7` | Soft accent, divider tint |
| `--clr-night-0` | `#171b1f` | Rare dark panels / footer / CTA emphasis |
| `--clr-night-1` | `#242a30` | Hovered dark surfaces |
| `--clr-rust-0` | `#9b6f5a` | Stamps / rare emphasis / poetic accent |
| `--clr-success-0` | `#556b5b` | Success / confirmed |
| `--clr-warning-0` | `#8a6b46` | Awaiting / caution |
| `--clr-error-0` | `#8c5c56` | Failure / unavailable |
| `--line-soft` | `rgba(51, 44, 38, 0.16)` | Hairlines / dividers |
| `--line-strong` | `rgba(51, 44, 38, 0.28)` | Stronger rules / control borders |
| `--wash-sea` | `rgba(113, 134, 141, 0.10)` | Tinted backgrounds |
| `--wash-night` | `rgba(23, 27, 31, 0.06)` | Heavy emphasis without full dark panels |

### 5.2 Typography

Use **Hebrew-first sans**. Default recommendation:

- Primary: `Alef`
- Acceptable alternative: `Assistant`
- Fallback: system sans

#### Type scale

| Token | Value | Use |
|---|---:|---|
| `--fs-display-2xl` | `clamp(3.5rem, 10vw, 6.5rem)` | Hero title |
| `--fs-display-xl` | `clamp(2.8rem, 7vw, 4.6rem)` | Page title / large state title |
| `--fs-display-lg` | `clamp(2rem, 5vw, 3.1rem)` | Major section titles |
| `--fs-h1` | `clamp(1.65rem, 3vw, 2.25rem)` | Section heading |
| `--fs-h2` | `1.25rem` | Card/row title |
| `--fs-body-lg` | `1.05rem` | Lead text / intro paragraph |
| `--fs-body` | `0.96rem` | Default paragraph |
| `--fs-body-sm` | `0.88rem` | Secondary body |
| `--fs-meta` | `0.78rem` | Labels / microcopy |
| `--fs-micro` | `0.68rem` | Metadata / badges |

#### Weight rules
- `400`: body
- `700`: headings, important labels
- `800/900`: hero title, price, very rare emphasis

#### Tracking rules
- Labels, dates, metadata, and divider text can use `0.12em`–`0.28em`.
- Do **not** over-track paragraphs or long Hebrew headings.

### 5.3 Spacing scale

| Token | Value |
|---|---:|
| `--space-2xs` | `0.25rem` |
| `--space-xs` | `0.5rem` |
| `--space-sm` | `0.75rem` |
| `--space-md` | `1rem` |
| `--space-lg` | `1.5rem` |
| `--space-xl` | `2rem` |
| `--space-2xl` | `3rem` |
| `--space-3xl` | `4.5rem` |
| `--space-4xl` | `6rem` |

### 5.4 Radius / border / shadow rules

| Token | Value | Use |
|---|---:|---|
| `--radius-sm` | `6px` | Inputs and small tags |
| `--radius-md` | `12px` | Soft cards |
| `--radius-lg` | `18px` | Large inset paper blocks, rarely |
| `--border-hairline` | `1px solid var(--line-soft)` | Default boundary |
| `--border-strong` | `1px solid var(--line-strong)` | Inputs / key cards |
| `--shadow-paper` | `0 12px 40px rgba(51, 44, 38, 0.08)` | Elevated paper card |
| `--shadow-panel` | `0 18px 50px rgba(23, 27, 31, 0.12)` | Dark emphasis block |

Rule: prefer **borders and contrast** over heavy shadows.

### 5.5 Motion

| Token | Value | Use |
|---|---:|---|
| `--dur-fast` | `160ms` | Hover / focus |
| `--dur-base` | `240ms` | Card hover / button |
| `--dur-slow` | `480ms` | Hero reveal / section fade |
| `--ease-standard` | `cubic-bezier(.2,.8,.2,1)` | Default easing |

Motion rules:
- Motion should feel like **ink settling** and **paper movement**, not software theatrics.
- Use opacity, translateY, and border-color changes.
- No parallax.
- No glow effects.
- Respect `prefers-reduced-motion`.

## 6. Layout system

### 6.1 Containers

| Container | Max width | Use |
|---|---:|---|
| `--container-wide` | `1180px` | Hero shell / wide sections |
| `--container-main` | `920px` | Main content shell |
| `--container-read` | `720px` | Editorial paragraphs |
| `--container-narrow` | `560px` | Forms, quotes, success states |

### 6.2 Breakpoints
- `480px` — small mobile
- `768px` — tablet
- `1024px` — desktop
- `1280px` — large desktop

### 6.3 Vertical rhythm
- Default section padding: `var(--space-3xl)` top and bottom
- Hero top padding: `var(--space-4xl)` or more
- Paragraph gaps: `var(--space-lg)`
- Section dividers: always intentional, never decorative filler

### 6.4 Page background model
Default background: `var(--clr-paper-0)` with a low-opacity grain layer and occasional wash panels.

Recommended base pattern:
- `body`: paper background
- `body::before`: fixed grain texture at `0.05`–`0.07`
- Section accents: thin rules, faded sea-tint blocks, optional line-art inserts

## 7. Component rules

## 7.1 Hero: poster-first composition

### Purpose
Immediately establish “Tel Aviv urban fantasy broadside.”

### Anatomy
1. Ribbon / notice line
2. Main title
3. Subtitle / premise line
4. Date + location line
5. Primary CTA
6. Skyline line art anchored to the bottom edge

### Styling
- Center the hero composition.
- Use the biggest type on the whole site here.
- Hero background should remain mostly paper.
- The skyline is an anchor, not a decorative sticker.
- Optional clouds/birds can live in corners at very low prominence.

### Notes
The hero should feel closer to the uploaded poster than to the current dark HTML.

## 7.2 Ribbon / notice band

### Purpose
Frame the hero with a printed-artifact gesture.

### Rules
- Use once in the hero, maybe once more for a small section marker if needed.
- Should feel like an illustration or inline SVG, not a glossy badge.
- Text inside should be short — one line only.

## 7.3 Logistics strip

### Purpose
Present date, time, and location in a disciplined way.

### Anatomy
- 3 cells desktop
- 1 column mobile
- Small label + stronger value

### Styling
- Printed-panel feel, not dashboard widgets.
- Use paper-deep or sea-wash background, not pure white.
- Hairline separators only.

## 7.4 Editorial lore block

### Purpose
Carry the core setting copy.

### Rules
- Use the reading container.
- Body text should be comfortable, open, and literary.
- Keep maximum line length narrow.
- Use a small tracked section label above.

## 7.5 Divider

### Purpose
Create a formal pause between narrative sections.

### Rules
- Thin line left/right with small uppercase-like tracked Hebrew label in the middle.
- Use sparingly.
- Should feel like a chapter break.

## 7.6 Faction ledger

### Purpose
Present factions like archived files or entries in a city ledger.

### Anatomy
- Optional monogram
- Faction title
- Two to four lines of text

### Styling
- Prefer bordered rows or softly separated cards.
- Use paper or paper-deep backgrounds by default.
- On hover, deepen the wash or border, not the saturation.

### Interaction
- If rows become clickable later, use subtle elevation + border tint only.

## 7.7 Quote block

### Purpose
Insert a lyrical pause.

### Styling
- Keep it restrained.
- Use a right border in accent color.
- Text should be larger than body but not display-sized.
- Citation should be tiny, tracked, and muted.

## 7.8 Price / CTA block

### Purpose
Provide the registration conversion point without breaking tone.

### Styling
- Price can be bold and large.
- CTA button should feel like a printed notice or stamped registration command.
- Avoid rounded, glossy, app-style buttons.

### Button rules
Primary button:
- dark fill on paper OR outline with dark hover fill
- rectangular or slightly softened corners only
- generous horizontal padding
- no bright gradients

Secondary button:
- outlined
- paper background
- strong focus ring

## 7.9 Dossier form

### Purpose
Make the application feel like a registration sheet or file, not a generic SaaS form.

### Form shell
- Use a narrow or medium-width paper card with stronger border and light shadow.
- Group fields visually with spacing, not too many boxes.

### Inputs
- Strong label above field
- Helper text below where needed
- Border-based styling
- Focus state uses `--clr-sea-0`
- Error state uses `--clr-error-0`

### Textarea
- Larger vertical space
- Comfortable line-height
- Resize allowed vertically only

### Checkboxes / radios
- Square or circle controls with strong border
- Checked state should use accent fill or dark checkmark
- Labels sit close to control

### Submission area
- Show privacy/processing note in small muted text
- CTA button should be prominent but not loud

## 7.10 Public roster entry

### Purpose
Show published players as entries on a noticeboard or registry.

### Anatomy
- Display name (always shown)
- Optional character name
- Optional faction name
- Optional short line or tag if approved later
- Never paid status

### Styling
- Bordered entries with modest paper contrast
- Character/faction lines should feel subordinate
- List can be 1 column mobile, 2 columns desktop

### Empty state
- Calm, matter-of-fact language
- Example: “הרשימה תתעדכן לאחר תחילת האישורים.”

## 7.11 Payment / status panel

### Purpose
Handle the return from Cardcom without promising final success before verification.

### States
- Processing / verifying
- Confirmed
- Failed / cancelled

### Styling
- A centered narrow panel with title, short explanation, next step, and action buttons.
- Each state uses the same structure, with only accent/border/icon color changing.

### Tone rules
Processing:
- “התשלום התקבל ונמצא בבדיקה”
- calm, transitional

Confirmed:
- “התשלום אושר”
- optionally mention that a document will be sent separately

Failed:
- “לא הושלם תשלום”
- give one clear retry path and one support path

## 8. Page-by-page art direction

## 8.1 `/` Landing page

### Goal
Sell the atmosphere and make registration feel inevitable.

### Structure
1. Poster-style hero
2. Logistics strip
3. About / premise block
4. Divider
5. Faction ledger
6. Quote block
7. Price + registration CTA
8. Footer / practical links

### Art direction
- Hero should be bright, airy, and iconic.
- Middle sections become more editorial and textural.
- CTA can introduce a stronger dark tone to increase visual gravity.

### Optional decorative assets
- Skyline line art
- small cloud drawings
- wave lines near the bottom of the hero
- faint stamp or seal behind a section title

## 8.2 `/apply/` Application form

### Goal
Feel like filling a registration dossier.

### Structure
1. Compact page header with mini skyline or ribbon
2. Intro text
3. Main form card
4. Support note / contact line
5. Submission CTA

### Art direction
- Narrower than landing page
- Less decorative than hero
- Very readable
- Form card should feel slightly more formal than the rest of the site

### UX notes
- Required fields clearly marked
- Validation text should appear directly under the field
- The page must feel calm, not bureaucratically heavy

## 8.3 `/apply/thanks/`

### Goal
Confirm that the application was received.

### Structure
1. Status title
2. One short confirmation paragraph
3. “What happens next” list or short paragraph
4. Return to main page button

### Art direction
- Use the same shell as payment states
- Add a faint stamp or check motif if desired
- Keep the page minimal and reassuring

## 8.4 `/players/` Public roster

### Goal
Show the published list as a living public register, without exposing process details.

### Structure
1. Page header
2. Short explanatory note
3. Roster grid or list
4. Optional last-updated line
5. Back to main page button

### Art direction
- Should feel like a noticeboard or cultural program roster
- No paid status
- Character and faction lines appear only when data exists
- Keep hierarchy clear: display name first, everything else secondary

### Sorting recommendation
- Alphabetical by display name for v1
- Do not visually imply internal process state

## 8.5 `/payment/return/success/`

### Goal
Acknowledge return from Cardcom while preserving backend truth.

### Required behavior
- Initial state should be **processing / verifying**
- Only show confirmed language if the backend renders a verified success state

### Structure
1. Status label
2. Title
3. Clarifying paragraph
4. Next step
5. Return button

### Copy guidance
Processing:
- “התשלום התקבל ונמצא כעת בבדיקה.”
- “אם הכול תקין, אישור ומסמך יישלחו אליכם בנפרד.”

Confirmed:
- “התשלום אושר.”
- “מסמך יישלח אליכם לאחר עיבוד התשלום.”

## 8.6 `/payment/return/failure/`

### Goal
Make retrying easy without panic.

### Structure
1. Failure title
2. One-line explanation
3. Retry CTA
4. Contact/support secondary action

### Art direction
- Same shell as success state
- Use a warmer border tone, not a screaming red treatment

## 9. Visual motifs and decorative system

### Approved motifs
- Skyline line art
- Ribbon / banner
- Cloud sketches
- Birds
- Wave or shoreline lines
- Margin notes
- Archival stamp shapes
- Faction monograms
- Diagrammatic symbols that feel half-legal, half-magical

### Rules
- Decorative elements should feel printed, sketched, or stamped.
- Keep opacity low for background motifs.
- Use monochrome or near-monochrome line art.

### Do not use
- Glowing sigils
- Fire/smoke particles
- 3D fantasy effects
- Holographic UI patterns
- Ornate faux-ancient borders

## 10. Asset requirements for design/dev handoff

The front-end should expect these assets to be prepared or exported as SVG/WebP:

1. `skyline-tel-aviv.svg`
2. `hero-ribbon.svg`
3. `cloud-cluster-left.svg`
4. `cloud-cluster-right.svg`
5. `wave-divider.svg`
6. `grain-paper.webp` or inline SVG grain
7. `stamp-ring.svg` (optional)
8. `faction-monograms.svg` or separate SVG files

### Technical rules
- Use SVG for line art.
- Avoid raster PNG unless the texture requires it.
- Decorative assets should remain subtle and compress well.

## 11. Responsive behavior

### Mobile
- Preserve poster feel in the hero, but simplify spacing.
- Logistics strip stacks to one column.
- Faction ledger remains one column.
- Buttons go full width when needed.
- Forms use one column only.

### Tablet
- Keep reading width narrow.
- Roster may move to two columns.

### Desktop
- Hero can breathe horizontally.
- Roster may use two columns.
- Decorative motifs can expand into margins.

## 12. Accessibility and implementation rules

### Accessibility
- Keep body text at or above comfortable contrast on paper.
- Minimum control touch target: `44px`
- Visible focus state on all links and controls
- Respect reduced motion
- Do not rely on color alone for statuses
- All decorative assets must be hidden from screen readers unless they convey meaning

### RTL
- Entire site should be `dir="rtl"`
- Right borders and alignments are first-class, not mirrored afterthoughts
- Quotes, labels, and metadata must be tested in Hebrew on mobile

### Performance
- Keep decorative assets lightweight
- Avoid large background videos or canvas effects
- Prefer CSS and SVG over runtime-heavy animation

## 13. Suggested implementation approach

### CSS architecture
Use a token-first approach:
- `:root` design tokens
- base styles
- layout primitives
- section styles
- component classes
- state modifiers

### Framework neutrality
This package works with:
- plain HTML/CSS
- Django templates
- React / Next
- Vue / Nuxt
- Astro

### Recommendation
Build the public site with semantic HTML and light JS only. Nothing in this visual direction requires a heavy front-end runtime.

## 14. Acceptance checklist for front-end signoff

- The site reads as **Tel Aviv urban fantasy**, not generic fantasy.
- The hero clearly borrows from the poster composition.
- The editorial body still preserves the restraint of the existing HTML.
- Paper is the dominant surface.
- Accent colors feel coastal/municipal, not neon.
- Buttons and forms feel like notices/dossiers, not app UI.
- The public roster never exposes payment information.
- Payment states clearly distinguish processing, confirmed, and failed.
- All pages are comfortable in RTL on mobile.

## 15. Build order

1. Implement tokens and shell
2. Build hero and landing sections
3. Build CTA styles
4. Build form styles and validation states
5. Build roster entries and empty states
6. Build payment status panels
7. Add decorative assets
8. Final responsive + accessibility pass

## 16. Files in this package

- `tokens/design-tokens.css`
- `tokens/design-tokens.json`
- `examples/style-tile.html`
- `examples/landing-page-wireframe.html`
- `examples/application-and-states-wireframe.html`
- `checklists/Frontend_Implementation_Checklist.md`
- `references/landing_page_reference.html`
- `references/poster_reference.jpeg`