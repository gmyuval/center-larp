# Front-end Implementation Checklist

## Foundations

- [ ] Site root is RTL by default
- [ ] `design-tokens.css` is imported globally
- [ ] Paper background and grain overlay are implemented
- [ ] Typography stack uses Hebrew-first sans
- [ ] Max-width containers are implemented

## Landing page

- [ ] Poster-style hero is implemented
- [ ] Ribbon / notice element is included
- [ ] Skyline anchor exists at the hero base
- [ ] Logistics strip is responsive
- [ ] Mixed-direction values (hours, numbers) render LTR within RTL context (`unicode-bidi: isolate` or `<bdi>`)
- [ ] About block uses readable line length
- [ ] Faction ledger rows are implemented
- [ ] Quote block is styled
- [ ] Price + CTA block is implemented

## Apply page

- [ ] Form shell uses dossier styling
- [ ] Labels, helper text, and error text are styled
- [ ] Inputs, textarea, checkboxes, and radios have focus states
- [ ] Submit CTA is prominent
- [ ] Mobile spacing feels calm and readable

## Thanks / payment states

- [ ] A shared status-panel component exists
- [ ] Processing state exists
- [ ] Confirmed state exists
- [ ] Failure state exists
- [ ] Copy does not promise success before backend verification

## Public roster

- [ ] Display name is the primary line
- [ ] Character and faction are optional secondary lines
- [ ] No payment information appears anywhere
- [ ] Empty state is implemented
- [ ] Responsive 1-column / 2-column behavior is implemented

## Accessibility

- [ ] Focus states are visible on links, buttons, and form controls
- [ ] Decorative images are marked `aria-hidden="true"` where appropriate
- [ ] Color is not the only status indicator
- [ ] `prefers-reduced-motion` is respected
- [ ] Hit areas are at least 44px where applicable

## Visual QA

- [ ] Overall site feels paper-first, not dark-first
- [ ] Accent colors feel coastal and muted
- [ ] Decorative assets are subtle
- [ ] Buttons do not look like SaaS components
- [ ] The site feels local to Tel Aviv
