# Coding Contract Addendum: PDA Dashboard Filter Collapse

**Status:** Frozen — Authorized for Implementation
**Version:** 1.1.0
**Approved:** 2026-09-24
**Scope:** Filter area in the Inbound, Outbound, and Temperature Record PDA dashboards
**Base CC:** [Coding_Contract_PDA_Record_Dashboard_Filter.md](./Coding_Contract_PDA_Record_Dashboard_Filter.md)

## 1. Objective

Reduce visual clutter on PDA history dashboards by collapsing the filter area
after the dashboard loads, while allowing the user to expand it whenever filter
criteria need to be entered or changed.

## 2. Contract

### CC-PDA-FILTER-COLLAPSE-001 — Default state

The filter area must be collapsed by default when a PDA history dashboard opens.

The collapsed state must show a clearly labelled upward/downward arrow control:

- downward arrow when the filter area is closed;
- upward arrow when the filter area is open.

The arrow control must retain an accessible label:

- `Show filters` when closed;
- `Hide filters` when open.

The control must be usable on desktop and narrow PDA screens without horizontal
scrolling. The arrow is the visible affordance; the text label need not be
visually displayed.

### CC-PDA-FILTER-COLLAPSE-002 — Expand and collapse

Clicking `Show filters` must reveal the existing date, document number, status,
`Filter`, and `Clear` controls.

Clicking `Hide filters` must hide those controls without changing the current
filter values or reloading the record list.

The expand/collapse control must expose its state through an accessible
`aria-expanded` value.

### CC-PDA-FILTER-COLLAPSE-003 — Applied-filter visibility

If one or more filter criteria are active, the collapsed area must provide a
visible indication that filters are applied, such as `Filters applied`.

The user must be able to expand the area and inspect the retained values.

### CC-PDA-FILTER-COLLAPSE-004 — Filter actions

The existing filter behavior remains unchanged:

- `Filter` applies all non-empty criteria with AND semantics;
- `Clear` empties all criteria and reloads the newest-first unfiltered list;
- invalid date ranges remain visible as validation errors;
- empty `From` and `To` values remain valid.

After `Filter` successfully applies the criteria, the area must automatically
collapse. The collapsed area must still show the active-filter indication.

`Clear` must keep the area open so the user can see that all values were emptied
and can immediately enter new criteria.

### CC-PDA-FILTER-COLLAPSE-005 — Navigation

Returning from a record must continue to show the empty, newest-first,
unfiltered dashboard defined by the base CC. The filter area must return to its
default collapsed state.

### CC-PDA-FILTER-COLLAPSE-006 — Responsive behavior

At the existing 390px PDA viewport:

- the collapsed control remains fully visible;
- the expanded filter controls stack or wrap without horizontal overflow;
- the record cards remain readable;
- opening or closing the filter area does not change the record selection rules.

## 3. Acceptance

- All three PDA dashboards open with filters collapsed.
- `Show filters` expands the complete filter area.
- `Hide filters` collapses it without losing entered values.
- Active filters are visibly indicated while collapsed.
- `Filter` and `Clear` retain the base CC behavior.
- The interaction is usable at desktop and 390px narrow-screen widths.

## 4. Verification

Automated verification must cover default collapsed state, expand/collapse,
`aria-expanded`, retained values, active-filter indication, Filter/Clear
behavior, navigation reset, and narrow-screen layout.

Human verification must confirm that a PDA user can discover, expand, use, and
collapse the filter area without losing filter criteria.

## 5. Out of Scope

- Changes to the filter fields or matching semantics defined by the base CC.
- Changes to Web list/form views.
- Saved filters, advanced search, pagination, or bulk actions.
- Changes to PDA record permissions or workflow state behavior.
