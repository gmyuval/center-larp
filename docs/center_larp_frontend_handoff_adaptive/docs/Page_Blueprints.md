# Center LARP - Page Blueprints

## Purpose

This document translates the design language into page-level blueprints. It is intended for the front-end developer implementing templates and responsive behavior.

---

## Shared page rules

### Every public page should include
- paper background
- subtle grain
- restrained top-level header treatment
- centered or editorially aligned Hebrew typography
- thin dividing rules
- visual continuity through the same token system

### Every page should avoid
- generic app chrome
- default framework form styling
- bright system-blue buttons
- overly dark full-screen backgrounds
- decorative clutter that competes with copy

---

## 1. Landing page blueprint

## Desktop structure

```text
[hero / poster composition]
  ribbon
  title
  subtitle
  date + location
  skyline illustration

[logistics strip]
  date | time | location | optional price

[about section]
  section label
  2-4 paragraphs

[divider]

[factions intro]
  small section label
  short intro

[faction ledger]
  row
  row
  row
  row

[quote block]

[CTA block]
  price
  registration button
  optional note
```

## Hero spec
- full-height or near-full-height
- centered content
- title stays above the skyline
- skyline touches or nearly touches bottom of hero
- optional decorative clouds/birds sit in the corners and do not interfere with text

## Mobile hero spec
- keep ribbon visible
- reduce skyline height before shrinking the title too much
- maintain generous top and bottom breathing room
- date and location can wrap into two lines if needed

## Landing page notes
- The hero is the most poster-like part of the experience.
- The rest of the page should feel quieter and more editorial.
- Avoid making every section visually unique; repetition and consistency are part of the tone.

---

## 2. Application page blueprint

## Structure

```text
[compact hero]
  page title
  short intro

[application form]
  identity section
  contact section
  concept / interest section
  optional logistics or consent section

[next steps note]

[submit footer]
  primary submit button
  short process explanation
```

## Visual behavior
- Keep the compact hero consistent with the landing page, but smaller and simpler.
- The form should sit inside a paper panel or quiet editorial layout.
- Group fields into meaningful sections.

## Form field spec
Each field group should contain:
- label
- optional help text
- input / textarea / select
- validation message area

## Recommended form widths
- single-column on mobile
- one column on desktop unless there is a compelling reason to split
- short paired fields are allowed only for obvious pairs, such as phone + email if they remain readable

## Form style notes
- Inputs should feel like printed registration fields.
- Focus states should be visible but restrained.
- Error states should use contrast and text, not only red outlines.

---

## 3. Thank-you page blueprint

## Structure

```text
[header]
  title
  short confirmation line

[message body]
  application received
  review process note
  expected next step

[secondary action]
  back to main page or roster
```

## Tone
Calm, respectful, and slightly atmospheric. This is not a checkout confirmation page.

## Visual guidance
- one quiet paper panel
- optional seal or stamp accent
- no celebratory confetti logic

---

## 4. Public roster page blueprint

## Structure

```text
[header]
  title
  intro line

[roster list]
  player item
  player item
  player item

[optional footer note]
```

## Recommended roster item structure

```text
display name
character name (conditional)
faction (conditional)
optional short public note (future-safe only)
```

## Layout options
Use one of these two patterns:

### Option A: editorial list
- best if the roster is text-heavy
- strong divider rhythm
- reads like a printed appendix

### Option B: quiet card grid
- best if the roster is short and visually balanced
- cards remain understated
- cards should not resemble game profile tiles

## Rule
Never show payment language or anything that implies payment status.

---

## 5. Payment return pages

## Pages
- payment success / received
- payment failed
- payment pending verification

## Shared structure

```text
[compact header]
  state title

[state note]
  short explanation
  next step

[secondary action]
  return to main page / contact note
```

## Visual direction
- same paper surface
- short messages
- no loud icons
- no generic payment-provider styling
- keep the site tone intact

## State styling
- success: use Patina or Sea Steel accents
- pending: use Ink Soft and calm microcopy
- failure: slightly stronger rules and clearer guidance, but still not alarmist

---

## 6. 404 / maintenance / generic info pages

Treat these as pinned notices.

## Structure

```text
[notice title]
[short explanation]
[action link]
```

## Style
- paper + rule + stamp feel
- minimal copy
- visually coherent with the rest of the site

---

## Section spacing guide

These are recommended default gaps. The developer can adjust slightly for the actual content, but the rhythm should stay generous.

| Context | Spacing |
|---|---:|
| hero title to subtitle | 24px |
| subtitle to date/location | 16px |
| hero content to skyline | 40-64px |
| section label to heading/body | 12-24px |
| paragraph to paragraph | 16-24px |
| section to section | 64-96px |
| ledger rows | 0px gap + ruled separation or 12px if card-based |
| quote block top/bottom | 64px |
| CTA top margin | 64-96px |

---

## Responsive notes

### Mobile priorities
- preserve hero composition
- preserve legibility
- keep metadata readable
- reduce decorative illustration before reducing content clarity
- keep faction rows easy to scan
- keep buttons full enough to tap comfortably

### Tablet
- maintain central alignment in hero
- keep the roster either single-column or two-column only if cards remain roomy
- logistics strip can stay multi-column

### Desktop
- allow the poster feel to breathe
- do not stretch reading copy too wide
- keep the editorial rhythm narrow and intentional

---

## Component state notes

## Buttons
States:
- default
- hover
- focus-visible
- disabled

Buttons should feel printed and intentional.

## Inputs
States:
- default
- hover
- focus
- invalid
- disabled

All states must remain accessible against paper surfaces.

## Faction rows
States:
- default
- hover
- optional selected / expanded in future

Hover should be subtle only.

---

## Front-end QA checklist

Before handoff back to product or design, confirm:

- the hero still reads like a poster on mobile
- the skyline does not collide with text at any breakpoint
- labels and metadata remain legible in Hebrew
- the faction list is comfortable to scan
- form labels never collapse into placeholder-only UX
- there is sufficient whitespace throughout
- focus states are visible
- public roster items do not visually imply missing hidden data
- the entire build feels like one system, not multiple page styles
