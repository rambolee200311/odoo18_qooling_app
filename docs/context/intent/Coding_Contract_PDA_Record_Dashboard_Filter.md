# Coding Contract: PDA Record Dashboard Filters

**Status:** Frozen — Authorized for Implementation
**Version:** 1.0.0
**Approved:** 2026-09-23
**Scope:** Inbound, Outbound, and Temperature Record PDA history dashboards
**Related CC:** [Coding_Contract_PDA_Record_Dashboard.md](./Coding_Contract_PDA_Record_Dashboard.md)

## 0. Document Governance

This document was reviewed, frozen, and explicitly authorized for implementation
on 2026-09-24.

This CC extends the existing PDA Record Dashboard contract. It changes only the
dashboard's record filtering experience; it does not change PDA form behavior,
document numbering, permissions, record state transitions, or Web list views.

## 1. Objective

Allow a PDA user to narrow the historical record list by date, document number,
and status before selecting a record to open.

## 2. Filter Contract

### CC-PDA-FILTER-001 — Filter area

Each Inbound, Outbound, and Temperature Record PDA history dashboard must show a
filter area above the record list.

The filter area must contain:

1. Date filter;
2. Document number filter;
3. Status filter;
4. A clearly labelled `Filter` button.

The filter area must be usable on both desktop and narrow PDA screens. Controls
must not require horizontal scrolling.

### CC-PDA-FILTER-002 — Date filter

The date filter must use the dashboard's configured primary date field:

| PDA dashboard | Date field |
|---|---|
| Inbound | `date` |
| Outbound | `date_arrival` |
| Temperature Record | `date` |

The approved design uses an optional inclusive date range with `From` and `To`
date inputs:

- Both `From` and `To` are optional and may be left blank.
- Both inputs empty: do not constrain by date.
- Only `From` entered: include records on or after that date.
- Only `To` entered: include records on or before that date.
- Both entered: include records within the inclusive range.

The user-facing date format must follow the active Odoo locale. Date comparison
must use the model date value, not a localized display string.

If `From` is later than `To`, the dashboard must show a clear validation message
and must not silently return an empty result.

### CC-PDA-FILTER-003 — Document number filter

The document number filter must match the record `name` field.

- Empty value: do not constrain by document number.
- Non-empty value: perform a fuzzy/contains match against the document number,
  case-insensitively.
- The entered value may match any part of the document number; an exact full
  document number is not required.
- Leading and trailing whitespace must be ignored.

The filter must not expose records the current user cannot read.

### CC-PDA-FILTER-004 — Status filter

The status filter must be a dropdown/select control. It must provide an empty
`All statuses` option and the statuses available for the current PDA model.

At minimum, the option values must support the states currently used by the
dashboard:

| Server value | English label | Chinese translation |
|---|---|---|
| empty | All statuses | 全部状态 |
| `draft` | Draft | 草稿 |
| `submitted` | Submitted | 已提交 |
| `exception_pending` | Exception pending | 异常待处理 |

`exception_pending` is shown only where supported by the model. The displayed
labels must use the translation system, with the English labels as the fallback.
The filter value must be compared against the server state value, not against
the translated label.

Selecting `All statuses` must remove the status constraint.

### CC-PDA-FILTER-005 — Filter action

Clicking `Filter` must apply all non-empty filter values together using AND
semantics.

The result list must:

- preserve the existing newest-first ordering;
- preserve the existing maximum record read limit;
- display the same fields and actions as the unfiltered dashboard;
- show a clear empty-result state when no record matches.

The dashboard must not navigate to a record merely because a filter was applied.

### CC-PDA-FILTER-006 — Filter state

When a filter is applied, the selected values must remain visible in the filter
area while the result list is displayed.

Opening a record and returning to the dashboard must not restore the previous
filter values. The filter controls must be empty and the newest-first,
unfiltered list must be loaded explicitly. Stale or misleading filtered results
are not allowed.

### CC-PDA-FILTER-007 — Clear behavior

The dashboard must provide a `Clear` action beside `Filter` to restore an
unfiltered list without manually removing each value. `Clear` must:

- empty the date, document number, and status controls;
- reload the newest-first unfiltered list;
- clear any filter validation message.

## 3. Data, Security, and Error Boundaries

1. Filtering must use Odoo ORM/search behavior and the current user's access
   rights and record rules.
2. The client must not fetch unrestricted records and then bypass permissions
   through client-side filtering.
3. Filter failures must show a user-facing error; the dashboard must not display
   a success-shaped empty list when loading failed.
4. Empty filters must preserve the existing dashboard behavior.
5. This CC does not change draft editing, submitted read-only behavior, document
   numbering, media, signatures, submission, or business validation rules.

## 4. Responsive and Accessibility Contract

1. Desktop layouts may use a horizontal filter row.
2. Narrow PDA layouts must stack controls or wrap them into readable rows.
3. The `Filter` button must remain visible without horizontal scrolling.
4. Each input must have a visible label or an equivalent accessible name.
5. Validation and empty-result messages must be associated with the filter area
   and understandable without relying on color alone.
6. Applying a filter must not reset the dashboard title, record type, or return
   navigation.

## 5. Acceptance Criteria

- Inbound PDA can filter by date, document number, and status.
- Outbound PDA can filter by date, document number, and status.
- Temperature Record PDA can filter by date, document number, and status.
- Multiple populated fields are combined with AND semantics.
- Fuzzy/contains document number matching works case-insensitively.
- Invalid date ranges are rejected with a visible message.
- No-match results are clearly distinguished from loading or failure states.
- Readable records remain subject to the existing draft/edit and submitted/read-
  only rules.
- The filter area is usable at the existing 390px PDA viewport without
  horizontal overflow.
- Empty criteria preserve the existing newest-first history list.

## 6. Verification Contract

### Automated verification

Automated verification must cover:

1. Filter controls render for all three PDA dashboards.
2. Date filtering with `From`, `To`, and both values.
3. Invalid date range validation.
4. Exact and partial document number matching.
5. Each supported status and `All statuses`.
6. Combined AND filtering.
7. Empty-result state.
8. ORM/access-controlled loading and load-failure notification.
9. Clear/reset behavior.
10. Desktop and 390px narrow-screen layout without horizontal overflow.

### Human verification

Human verification must confirm that a PDA user can:

1. identify the active record type;
2. enter date, document number, and status criteria;
3. apply the filter and understand the result;
4. recognize an empty result and a validation error;
5. open a Draft for editing and a Submitted record as read-only after filtering;
6. use the filter area on a narrow PDA screen.

Playwright simulation may be recorded as ATR/HVR only when it is actually
executed. It must not be described as real-device camera or touch verification.

## 7. Out of Scope

- Changes to Web list or form views.
- Changes to server-side permissions or record rules.
- Changes to record creation, submission, signatures, media, or document numbering.
- Pagination, bulk actions, export, saved filters, or advanced search domains.
- Replacing the existing PDA dashboard record cards/table.
- Client-side access-control bypass or direct database access.

## 8. Approved Decisions

1. Date filtering uses an inclusive `From`/`To` date range.
2. `Clear` is required beside `Filter`.
3. Status labels and Chinese translations are defined in
   CC-PDA-FILTER-004.
4. Filter values are not restored after returning from a record; the dashboard
   returns to an empty, newest-first list.
