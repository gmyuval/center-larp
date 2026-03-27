# Center LARP - Front-End Design Handoff

## Purpose

This package is a front-end handoff for the public-facing site of the Tel Aviv urban fantasy LARP. It translates the two current references into a concrete design language, a reusable token system, and page/component guidance that a front-end developer can implement directly.

The design must synthesize:

1. the current HTML reference's narrow editorial layout, restrained typography, faction list, quote treatment, and muted steel-blue accents
2. the poster reference's parchment base, skyline line art, central hero composition, ribbon banner, and printed cultural-poster tone

The result should feel like **an occult cultural broadside from Tel Aviv** rather than a generic fantasy site or a glossy event microsite.

---

## Creative direction in one sentence

**A secret agreement between the city and the supernatural, printed like a Tel Aviv cultural poster and annotated like an old municipal notice.**

Internal shorthand for the team:

- **Paper, Asphalt, and Salt**
- **Municipal Occult**

Both names describe the same art direction.

---

## What the site should feel like

The site should sit between two atmospheres:

### Daylight Tel Aviv
- paper
- salt air
- faded print
- old notices
- line drawings
- city horizon
- culture poster energy

### Night Tel Aviv
- hidden agreements
- occult politics
- hushed tension
- literary noir undertones
- steel-blue shadow
- private pacts beneath public space

The page should therefore be **light-first with dark undertones**.

That is the important distinction. This is not a black fantasy site with gold ornaments. It is a **bright Tel Aviv paper world carrying dark magical pressure underneath**.

---

## Design pillars

### 1. Urban, not medieval
The world is built out of Tel Aviv concrete, shoreline light, printed matter, city memory, and public space. Avoid imported fantasy signals such as ornate medieval frames, pseudo-ancient glyph systems, swords-and-scrolls UI, and over-decorated fantasy typography.

### 2. Literary, not gamified
The current copy and structure already support a literary tone. Preserve that. The site should feel authored and typeset, not app-like or product-like.

### 3. Local, not generic
Everything should hint at Tel Aviv: the sea horizon, the skyline, cultural poster language, taped notices, receipt paper, institutional layout, old café mythology, and municipal geometry.

### 4. Printed, not glossy
The visual world should be driven by typography, paper texture, line art, and thin rules. Surfaces should feel printed or stamped, never slick or heavily UI-polished.

### 5. Calm surface, hidden tension
The page should remain composed and readable. The fantasy layer appears through atmosphere, symbols, annotations, and tone rather than special-effects spectacle.

---

## Reference synthesis

## From the current HTML reference, keep
- narrow editorial content width
- restrained Hebrew sans typography
- strong hierarchy through scale and spacing
- thin ruled dividers
- faction list / ledger rhythm
- muted cool accent color
- quiet fade-up motion
- serious tone over playful marketing language

## From the poster reference, keep
- warm parchment base
- centered hero composition
- large title with smaller metadata below
- skyline line art as a grounding horizon
- ribbon / banner language
- hand-drawn clouds, birds, and illustrative margin motifs
- archival / printed-poster atmosphere

## Combined outcome
The site should open like a poster, then read like an editorial dossier.

**Poster first. Editorial after.**

---

## Tone board

### Keywords
- parchment
- seawind
- municipal
- occult
- literary
- urban folklore
- annotated
- hand-drawn
- archival
- coastal noir

### Avoid
- cyberpunk
- neon magic
- medieval fantasy
- polished startup UI
- maximalist gothic decoration
- generic dark-event microsite aesthetics

---

## Color system

The palette should combine paper warmth from the poster with the cooler ink-and-steel accents already present in the current HTML.

### Core palette

| Token | Hex | Usage |
|---|---:|---|
| Paper | `#F5F0E7` | main background |
| Paper Deep | `#ECE5D8` | cards, ribbons, subtle contrast surfaces |
| Paper Aged | `#D8CFBF` | borders, aged fills, chips |
| Ink | `#352D26` | primary text, rules, illustrations |
| Ink Soft | `#5E554B` | body copy, secondary copy |
| Ink Faint | `#8E8479` | muted metadata |
| Night | `#15181D` | rare dark sections, return states, overlays |
| Night Soft | `#20262D` | dark surface variant |
| Sea Steel | `#8B9AA6` | accent lines, buttons, UI emphasis |
| Patina | `#70848E` | secondary accent, hover fill |
| Stamp Rust | `#9B6E5A` | rare emphasis, stamps, special metadata |
| Rule | `rgba(53,45,38,0.16)` | default lines and borders |
| Rule Strong | `rgba(53,45,38,0.28)` | stronger dividers |

### Color behavior
- The page background is paper, not black.
- Ink colors should do most of the expressive work.
- Sea Steel and Patina are accents, not the base.
- Rust is rare and intentional.
- Dark sections should be sparse and strategic, so they feel like nocturnal interruptions rather than the main theme.

### Recommended gradients
Use gradients only as very subtle printed fades. Avoid digital-looking neon or glossy gradients.

Allowed example:
- hero rule fade: transparent -> Sea Steel -> transparent
- paper wash: Paper -> Paper Deep at very low contrast

Not allowed:
- saturated multicolor gradients
- glossy metallic gradients
- spotlight gradients

---

## Typography

## Primary rule
Use modern, readable Hebrew type. Do not introduce faux-fantasy fonts.

### Preferred stack
- **Primary / body / UI**: Alef, Assistant, or Heebo
- **Display**: same family in heavier weights
- **Optional editorial secondary**: a restrained Hebrew serif for quotations only, if the team already has one and it performs well in production. If not, keep everything in the sans family.

### Typography roles

#### Display title
- large
- tightly set
- low line-height
- high contrast against paper
- centered in hero

#### Section label / eyebrow
- small caps feel via tracking
- generous letter spacing
- muted accent color
- used for metadata and navigation cues

#### Body copy
- comfortable leading
- readable paragraph widths
- editorial, not dense
- keep long lore copy within a restrained reading measure

#### Quote copy
- slightly larger than body
- quieter color
- treated as a literary pause, not a testimonial widget

### Type scale

```text
Display XL: clamp(3.6rem, 10vw, 6.8rem)
Display LG: clamp(2.8rem, 7vw, 4.8rem)
H1:         clamp(2.3rem, 5vw, 3.4rem)
H2:         clamp(1.65rem, 3vw, 2.2rem)
H3:         1.25rem
Body:       1rem
Small:      0.92rem
Meta:       0.72rem
Micro:      0.65rem
```

### Tracking
- labels: `0.18em`
- banner copy: `0.08em`
- avoid over-tracking large Hebrew headings

---

## Texture and surface treatment

Texture is important, but it must remain subtle.

### Required
- soft paper grain across the overall page or hero
- small print imperfections or faint archival noise
- line-art illustration treatment
- thin rules and outline boxes

### Optional
- faint stamp textures
- handwritten or annotated margin marks
- map-like marks or circles around specific details

### Avoid
- strong parallax texture
- fake burnt edges
- overbearing noise layers
- visibly repeating low-quality texture tiles
- fog or particle effects

---

## Illustration language

The illustration layer is a major part of the identity.

### Use
- skyline line art
- shoreline / wave lines
- clouds
- birds
- ribbon / banner artwork
- thin monochrome emblem work
- archival marks
- diagrammatic notes

### Style rules
- single-ink or near-single-ink line drawing
- consistent line weight family
- slightly imperfect hand-drawn quality is welcome
- illustrations should behave like printed inserts, not like fantasy concept art

### Magic treatment
Magic should be expressed as **annotations on the city**, not as a separate high-fantasy visual system.

Good:
- seals
- signatures
- diagram-like marks
- contract clauses
- archive stamps
- coded notes
- faction monograms

Bad:
- glowing spell circles
- floating particles
- generic runes
- crystal-ball fantasy tropes

---

## Layout system

### Overall structure
The page should have two different modes:

1. **Poster hero mode**
2. **Editorial reading mode**

### Container widths
- hero max width: `64rem`
- main content max width: `46rem`
- reading measure: `38rem`

### Spacing rhythm
Use large vertical spacing. Let the page breathe.

Suggested spacing scale:
- 4px
- 8px
- 12px
- 16px
- 24px
- 32px
- 48px
- 64px
- 96px
- 128px

### Alignment logic
- hero: centered
- body copy: mostly right-aligned / RTL natural flow
- metadata strips: grid-based
- section intros: aligned to content column
- quote and CTA: slightly offset from the repeated rhythm so they feel like interludes

### Shape language
- mostly square or softly rounded corners
- thin rules
- outlined boxes
- quiet shadows
- no pill-heavy SaaS components
- no glassmorphism

---

## Motion and interaction

Motion should be minimal and atmospheric.

### Good motion
- soft fade-up on initial load
- line draw or reveal on thin rules
- subtle hover lift or fill shift
- light opacity shifts on illustration overlays

### Bad motion
- heavy parallax
- large scroll transforms
- magical glows
- pulsing effects
- animated smoke or particles

### Motion specs
- fast: 160ms
- base: 240ms
- slow: 420ms
- easing: `cubic-bezier(0.2, 0.7, 0, 1)`

---

## Component guidance

## 1. Hero
The hero should be rebuilt around the poster composition.

### Required hero pieces
- ribbon / banner with short atmospheric line
- large centered title
- supporting subtitle or category line
- date and location line
- skyline illustration anchoring the lower edge
- optional small decorative clouds / birds in upper corners

### Hero behavior
- full-viewport or near-full-viewport on desktop
- compressed but still ceremonial on mobile
- title and metadata remain centered
- skyline remains visible without dominating the first fold

### Do not
- push everything into a conventional left-aligned marketing hero
- place a giant button directly under the title if it breaks the poster feel
- use a photographic hero background

## 2. Logistics strip
This is the site’s first strong information block after the hero.

### Visual direction
- ledger / notice-board feel
- thin outer border
- individual cells separated by rules
- paper surface or faint aged fill
- more printed than dashboard-like

### Content
- date
- time
- location
- optional price

### Responsive behavior
- 3 or 4 columns on desktop
- stacked cells on small screens
- keep labels small and tracked

## 3. About section
This is editorial copy, not marketing bullets.

### Direction
- narrow reading column
- generous paragraph spacing
- optional highlighted first paragraph or opening line
- optional faint side note or marginal marker

## 4. Faction ledger
Do not make this look like character cards from a game site.

### Preferred treatment
- archival ledger rows or understated cards
- faction glyph / monogram in a dedicated narrow column
- faction title
- faction description with good line-height
- optional faint faction seal in the background

### Interaction
- small hover state only
- no flip cards
- no carousel
- no overdesigned tabs

## 5. Quote block
Treat quotations like literary intermissions.

### Direction
- generous whitespace above and below
- right-border or inline rule
- quieter text color
- citation line below

## 6. CTA block
The CTA should feel stamped or printed, not promotional.

### Recommended content
- ticket / registration price
- one primary action button
- optional short note below

### Button style
- outlined by default
- filled on hover
- ink / patina palette
- strong typography
- no glossy gradients
- no oversized rounded corners

## 7. Application form
The form should feel like a **registration sheet / dossier**, not a SaaS form.

### Form styling
- strong labels
- clear vertical rhythm
- grouped sections
- generous input height
- subtle borders
- paper-toned surfaces
- clear error states

### Inputs
- avoid ultra-rounded fields
- use either full subtle border or strong bottom border with enough contrast
- placeholder text must not carry meaning alone
- labels always visible

### Section framing
- each form section can behave like a paper panel
- use microcopy like notes, not tooltips whenever possible

## 8. Public roster
The public roster should feel like a published notice board or event broadside appendix.

### Direction
- clean list or quiet card grid
- public display name as the primary unit
- character and faction appear only when configured
- no payment language anywhere
- quiet secondary typography
- optional divider rhythm between people

## 9. Empty / state pages
The payment return page, thank-you page, and error pages should still live within the same art direction.

### Examples
- success: paper + seal / stamp accent
- waiting for verification: paper + calm note
- failure: paper + darker rule, but no alarmist neon or red-heavy UI
- maintenance: like a printed notice temporarily pinned to the wall

---

## Page-by-page direction

## Landing page
### Order
1. poster hero
2. logistics strip
3. about / premise
4. factions
5. quote
6. price + CTA

### Key experience
The landing page should move from **ceremonial invitation** into **editorial explanation** and end with a clear registration action.

## Application page
### Order
1. smaller hero header
2. brief intro text
3. application form
4. expectations / next steps note
5. submit

### Key experience
The player should feel like they are submitting themselves to a city process, not merely filling out a checkout form.

## Thank-you page
- warm and calm
- confirm receipt
- explain GM review and approval flow
- optionally include a short atmospheric line

## Public roster page
- headline + intro
- list / grid of published players
- optional counts or filters only if truly needed
- must stay readable and quiet

## Payment state pages
- keep short
- visually consistent
- avoid turning these into generic payment templates

---

## Accessibility and RTL requirements

### Accessibility
- semantic landmarks: header, main, section, footer
- all decorative illustrations marked appropriately
- sufficient text contrast over paper surfaces
- visible keyboard focus
- reduced-motion preference support
- accessible form labels and error messages
- no critical information conveyed by color alone

### RTL
- design native-first for RTL, not mirrored as an afterthought
- spacing, borders, and quote rules should respect RTL flow
- icon placement should be intentional in RTL context
- test with real Hebrew copy, not lorem ipsum

### Responsive
- build mobile-first
- protect the centered hero composition on small screens
- allow the skyline artwork to crop gracefully
- keep body copy measure comfortable on all widths

---

## Asset requests for the visual design

If the art side can provide these, the front-end result will become much stronger:

1. **clean vector skyline**
2. **ribbon / banner as SVG**
3. **cloud and bird doodles as SVG**
4. **paper grain texture tile**
5. **faction monograms / initials**
6. **optional stamp / seal marks**
7. **optional marginal notation assets**

If those are unavailable, the front-end build can still start with the current poster as a visual guide and stub assets.

---

## Practical build guidance

### Build strategy
- centralize design tokens as CSS custom properties
- build a small set of reusable primitives
- prefer SVG illustrations
- use very little JS
- lean on typography and spacing over effects
- keep the public site mostly static in feel, even if rendered through a backend

### Core primitives to implement first
1. page container
2. hero container
3. eyebrow / label
4. title styles
5. rules / dividers
6. button
7. card / ledger row
8. form field
9. quote block
10. roster item

### Recommended implementation order
1. tokens and global styles
2. poster hero
3. editorial sections
4. faction ledger
5. CTA
6. form styling
7. roster styling
8. state pages

---

## Visual anti-patterns

Do not let the implementation drift into any of these:

- black-and-gold occult cliché
- neon urban fantasy
- medieval manuscript fantasy
- generic startup event page
- stock-photo city marketing site
- over-animated story page
- over-ornamented magical UI chrome

---

## Acceptance checklist for front-end review

The build is on track when the page:
- reads as Tel Aviv before it reads as fantasy
- feels bright, printed, and coastal rather than dark and heavy
- carries hidden tension without visible spectacle
- looks literary and editorial
- uses typography and illustration more than UI ornament
- remains readable and calm on mobile
- makes the form feel like a dossier, not checkout
- keeps the public roster understated and public-safe

---

## Quick art-direction summary

If the team needs a single paragraph to remember the whole system:

**Build the site like a Tel Aviv cultural poster that gradually turns into an occult dossier. Start with parchment, skyline line art, and centered ceremonial typography. Move into narrow editorial reading sections with thin rules, faction ledgers, literary quotations, and stamped calls to action. Keep the magic in seals, annotations, and atmosphere, not effects. Keep the city present at all times.**
