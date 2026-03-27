# Adaptive Theme and Responsive Addendum

## 1. Why this addendum exists

The original front-end handoff defined the core visual language: **Paper, Asphalt, and Salt**. This addendum extends that language into two adaptive dimensions:

1. **Night / day theme support**
2. **Responsive and mobile-specific behavior**

The goal is not to create two separate brands or a reduced “mobile version.” The goal is to create one coherent system that:

- keeps the Tel Aviv urban-fantasy identity intact in all modes
- feels light and printed by day, shadowed and municipal-occult by night
- remains legible and atmospheric on small screens without collapsing into generic app UI

## 2. Adaptive design principles

### 2.1 One brand, two light conditions

The site should feel like the **same poster, in different lighting**.

- **Day theme** = sun-faded paper, sea air, noticeboard, literary broadside
- **Night theme** = asphalt, moonlit paper, sodium lamps, hidden agreements

Night mode is **not** a full inversion and **not** pure black. It should still preserve paper, ink, stamp, and archival cues.

### 2.2 Mobile is not a simplified fallback

On mobile, the site should still feel like an artifact. The system should preserve:

- poster-like hero hierarchy
- narrow editorial pacing
- skyline and line-art cues
- faction/archive rhythm
- ceremonial CTA feeling

What changes on mobile is composition, density, and interaction model.

### 2.3 Responsive rules by priority

When trade-offs are necessary, prioritize in this order:

1. Legibility of Hebrew content
2. Clear CTA and form completion flow
3. Brand texture and atmosphere
4. Decorative detail density

If an ornamental element makes the page harder to use on mobile, reduce or reposition it.

## 3. Theme strategy

## 3.1 Theme modes

Support three theme modes in the front end:

- `auto`
- `day`
- `night`

### Recommended default behavior

- Default to `auto`
- In `auto`, follow `prefers-color-scheme`
- If no system preference is available, fall back to `day`
- Persist manual selection in local storage

### Theme attribute contract

Apply the mode on the root node:

```html
<html dir="rtl" lang="he" data-theme="auto">
```

Allowed values:

- `data-theme="auto"`
- `data-theme="day"`
- `data-theme="night"`

## 3.2 Theme switcher UX

### Placement

- Desktop: top header utility area or hero top corner
- Mobile: compact icon+label button in header; optional placement inside quick menu if header is crowded

### Interaction model

Recommended cycle:

- Auto -> Day -> Night -> Auto

### Copy

Use explicit labels, not just icons.

Suggested Hebrew labels:

- אוטומטי
- יום
- לילה

### Switcher styling

The switcher should feel like a **small printed control**, not a floating glossy gadget:

- hairline border
- paper or asphalt inset background, depending on theme
- icon optional, label required
- no neon highlight

## 4. Semantic token model

The original package used mostly physical tokens. For implementation, layer **semantic tokens** on top so the same components can switch themes cleanly.

### 4.1 Core semantic surfaces

| Semantic token | Day | Night | Notes |
|---|---|---|---|
| `--surface-page` | warm paper | dark asphalt | Main background |
| `--surface-page-alt` | lighter paper wash | darker asphalt wash | Alternating sections |
| `--surface-card` | elevated paper | charcoal card | Cards, inputs, list rows |
| `--surface-card-soft` | pale paper | moonlit charcoal | Soft inset blocks |
| `--surface-contrast` | dark ink panel | pale paper panel | Rare contrast hero/CTA blocks |
| `--surface-overlay` | translucent paper fog | translucent night wash | Fixed overlays, menus |

### 4.2 Text tokens

| Semantic token | Day | Night | Notes |
|---|---|---|---|
| `--text-primary` | deep ink | warm paper text | Main text |
| `--text-secondary` | softened ink | muted paper text | Body/supporting copy |
| `--text-muted` | grey-brown metadata | dusty warm metadata | Labels and small hints |
| `--text-on-contrast` | warm paper | dark ink | Text on `--surface-contrast` |

### 4.3 Border and accent tokens

| Semantic token | Day | Night | Notes |
|---|---|---|---|
| `--border-soft` | faded ink line | pale ink line | Default borders |
| `--border-strong` | stronger ink line | stronger pale line | Inputs, cards |
| `--accent-primary` | sea-steel | moonlit sea-steel | Links, selected states |
| `--accent-secondary` | soft patina | desaturated cool accent | Secondary emphasis |
| `--accent-rust` | stamp rust | warmer ember rust | Rare accent only |
| `--focus-ring` | steel accent glow | pale sea glow | Keyboard focus |

## 4.4 Theme emotion rules

### Day theme emotion

- airy
- poster-like
- sun-bleached
- open margins
- clear silhouettes
- visible paper grain

### Night theme emotion

- close
- hidden
- sodium-lit
- interior corridors
- deeper contrast
- cooler shadows with retained paper warmth

## 5. Component behavior by theme

## 5.1 Hero

### Day

- paper field
- dark ink title
- ribbon in warm light paper
- skyline as sepia or ink line drawing
- clouds and marginalia lightly visible

### Night

- page background shifts to asphalt
- hero content may sit on a slightly lighter inset field if contrast needs help
- ribbon becomes charcoal or moonlit paper depending on surrounding section
- skyline line art should remain visible, but reduce ornamental density slightly to avoid visual noise

### Important

The hero title should never lose its poster quality in dark mode. Avoid making it look like a generic app splash screen.

## 5.2 Section dividers and labels

- Keep dividers in both modes
- In night mode, use lower-opacity pale lines, not bright white rules
- Labels should remain tracked and editorial, never become button-like pills

## 5.3 Logistics strip

### Desktop

- three columns on wide layouts
- maintain printed information-panel feeling

### Mobile

- convert to stacked cards or a single-column vertical strip
- keep clear label/value separation
- use generous padding; do not compress into a tight dashboard

### Night mode

- cards become charcoal surfaces
- use cool accent lines and pale labels
- preserve strong value contrast

## 5.4 Faction cards / archive rows

### Day

- paper rows with thin dividers
- monogram treated as an archival seal

### Night

- dark rows with pale ink text and soft borders
- monogram can pick up a slightly brighter sea-steel tint
- avoid glowing sigils; keep it typographic and archival

### Mobile

- monogram can move above title or into the leading edge
- row becomes stacked card
- keep text alignment and rhythm clean; do not rely on side-by-side dense layouts

## 5.5 Buttons and CTAs

The CTA should feel like a **ceremonial printed action**.

### Default button behavior

- Day: paper or contrast block with hairline frame
- Night: moonlit or pale-paper button against asphalt background
- hover: slight lift or border strengthening only
- focus: visible ring
- active: subtle press, not glossy shine

### Mobile CTA

On mobile landing pages, a **sticky bottom CTA** is recommended when registration is open.

Rules:

- only on mobile/tablet
- height large enough for thumb use
- use site-safe area inset
- visually coherent with printed language
- should not obscure critical content or legal copy

## 5.6 Forms

### Day form language

- registration-sheet feeling
- light paper fields, hairline frames
- generous vertical spacing

### Night form language

- darker field surfaces with pale text
- keep form borders clear
- placeholder text must remain readable
- never rely on low-contrast greys in night mode

### Mobile form rules

- one-column only
- input height at least `44px`
- clear label above field
- helper text always below label or below field, not side aligned
- primary submit action full-width
- validation states should be visible without color alone

## 5.7 Public roster

### Desktop

- can be list-based or masonry-lite only if it remains orderly
- prefer archive table/card hybrid over playful grid

### Mobile

- simple stacked cards
- display name first
- character/faction if present below in muted hierarchy
- no tiny metadata columns

### Theme behavior

Roster must feel consistent across themes. Avoid switching from archive feel by day to “social app cards” at night.

## 5.8 Payment and result states

Payment return states should feel ceremonial, not transactional boilerplate.

States:

- awaiting verification
- payment received
- payment failed
- application received
- payment link sent

### Mobile

- keep narrow measure
- single-column state card
- important action or contact link near top
- status iconography optional; text clarity is primary

## 6. Responsive system

## 6.1 Breakpoints

Use these breakpoints consistently:

- `0-479px`: small mobile
- `480-767px`: large mobile
- `768-1023px`: tablet
- `1024-1279px`: desktop
- `1280px+`: wide desktop

## 6.2 Responsive density rules

| Element | Small mobile | Large mobile | Tablet | Desktop |
|---|---|---|---|---|
| Hero top padding | smaller | medium | medium-large | large |
| Section padding | compact | compact-medium | medium | full |
| Decorative marginalia | minimal | limited | moderate | full |
| Grid columns | 1 | 1 | 2 where sensible | full layout |
| Sticky CTA | yes | yes | optional | no |
| Hover-only affordances | none | none | optional | yes |

## 6.3 Mobile-first layout rules

- Build components mobile-first
- Add columns only when content benefits
- Keep reading measure comfortable for Hebrew on small screens
- Avoid large ornamental left/right gutters on small devices
- Favor top-to-bottom information order

## 6.4 Spacing rules by breakpoint

### Small mobile

- section padding: `2rem` to `2.5rem`
- content gap: `0.75rem` to `1rem`
- card padding: `1rem` to `1.25rem`

### Large mobile / tablet

- section padding: `2.5rem` to `3rem`
- card padding: `1.25rem` to `1.5rem`

### Desktop

- use original spacing scale from the main handoff

## 7. Page-specific responsive rules

## 7.1 Landing page

### Mobile hero

- allow title to wrap naturally into 2-3 lines
- ribbon may wrap into two lines if needed
- reduce skyline height and center crop it
- move CTA into first viewport if possible
- keep event meta directly under the title, not separated by excess ornament

### Mobile content order

Recommended order:

1. Hero
2. CTA
3. One-paragraph premise
4. Logistics
5. Factions / key setting sections
6. Registration details
7. Footer

### Desktop hero

- retain more poster composition
- skyline can breathe wider
- decorative clouds and marginalia can appear more freely

## 7.2 Application page

### Mobile

- one-column form only
- no paired fields unless extremely short and obvious
- persistent progress indicator optional, but keep it discreet
- submit action anchored after final field and optionally repeated as sticky footer when form is long

### Desktop

- may use two-column layout only for short administrative fields
- all narrative or long-answer fields remain full width

## 7.3 Public roster

### Mobile

- stacked archive cards
- optional filters collapse into a drawer or a top sheet
- avoid chips explosion
- keep published character/faction lines short and clearly labeled

### Desktop

- filters may sit inline or in a side rail if needed
- roster can use a two-column card grid or disciplined list

## 7.4 Payment / confirmation states

### Mobile

- state title at top
- explanatory copy immediately below
- contact/help action visible without long scrolling
- if showing next steps, keep them as 2-4 short bullets maximum

## 8. Asset behavior across themes and breakpoints

## 8.1 Texture

- Keep grain subtle in both themes
- Reduce texture opacity slightly on mobile to avoid muddy rendering
- In night mode, use texture sparingly so text contrast stays strong

## 8.2 Skyline and line art

- Use the skyline as a grounding motif, not a heavy illustration block
- On mobile, reduce its vertical footprint
- On night mode, lighten strokes or use tinted overlays instead of full inversion

## 8.3 Decorative ornaments

- Clouds, birds, wave marks, marginalia, and stamp-like notes can be present
- Reduce ornament count on small screens
- Never allow ornaments to push CTA or body copy below the fold unnecessarily

## 9. Accessibility requirements

- color contrast must remain accessible in both themes
- do not communicate states using color alone
- focus styles must be visible in both themes
- hit area minimum: `44px`
- respect `prefers-reduced-motion`
- if using theme icons, include readable labels or `aria-label`
- sticky mobile CTA must not cover form errors, cookie banners, or footer essentials

## 10. Front-end implementation contract

## 10.1 CSS architecture

Recommended structure:

1. **Physical palette tokens**
2. **Semantic theme tokens**
3. **Component tokens**
4. **Component styles**
5. **Responsive overrides**

Do not style components directly from raw palette values where avoidable.

## 10.2 Theme implementation

Recommended approach:

- root `data-theme` attribute
- `auto` maps to `prefers-color-scheme`
- localStorage persistence
- optional server-side rendering of saved preference if available

## 10.3 Responsive implementation

- mobile-first CSS
- use CSS Grid/Flex only where content warrants it
- keep RTL behavior verified at all breakpoints
- test typography wraps in Hebrew, especially hero title, ribbon text, and long button labels

## 11. QA matrix

### Theme QA

- day / auto-day / night / auto-night
- fresh session vs saved preference
- theme toggle after page load
- focus states in both themes
- illustrations and hairlines visible in both themes

### Responsive QA

- 360px
- 390px
- 430px
- 768px
- 1024px
- 1440px

### Page QA

Test each breakpoint and theme combination on:

- landing page
- application page
- public roster
- payment sent state
- payment success state
- payment failure state

## 12. Final recommendation to the front-end team

Treat this as a **mode-aware editorial system**, not a utility interface.

By day, the site should feel like a printed Tel Aviv cultural poster. By night, it should feel like the same poster under streetlights and hidden agreements. On mobile, it should feel like the poster folded into a pocket-sized dossier, not stripped down into generic product UI.
