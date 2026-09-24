# PDA Record Dashboard Filter Collapse Human Verification Record (HVR)

> Document status: Human Verification Passed
> Intent ID: `INTENT-PDA-RECORD-DASHBOARD-FILTER-COLLAPSE`
> CC: [Coding_Contract_PDA_Record_Dashboard_Filter_Collapse.md](../intent/Coding_Contract_PDA_Record_Dashboard_Filter_Collapse.md) `v1.0.0 Frozen`
> IHR: [IHR_INTENT-PDA-RECORD-DASHBOARD-FILTER-COLLAPSE.md](./IHR_INTENT-PDA-RECORD-DASHBOARD-FILTER-COLLAPSE.md)
> ATR: [ATR_INTENT-PDA-RECORD-DASHBOARD-FILTER-COLLAPSE.md](./ATR_INTENT-PDA-RECORD-DASHBOARD-FILTER-COLLAPSE.md)

## 1. Verification Status

| Field | Value |
|---|---|
| Human verification required | Yes |
| Status | Passed |
| Verification date | 2026-09-24 |
| Human verifier | User-confirmed manual verification |
| Result | Passed |

## 2. Required Scenarios

### HVR-SCN-001 — Default collapsed state

- Open each PDA history dashboard.
- Confirm the filter area is collapsed and a downward arrow control is visible.
- Confirm the control is announced as `Show filters`.

### HVR-SCN-002 — Expand and retain values

- Expand the filter area using the arrow control.
- Enter filter values, collapse it, and expand it again.
- Confirm the values remain visible.

### HVR-SCN-003 — Filter auto-collapse

- Apply a valid filter.
- Confirm the filter area automatically collapses.
- Confirm the upward/downward arrow changes with the state.
- Confirm the active-filter indication remains visible.

### HVR-SCN-004 — Clear remains open

- Expand the filter area and apply values.
- Click `Clear`.
- Confirm all values are empty, the list is unfiltered, and the filter area
  remains open.

### HVR-SCN-005 — Narrow PDA layout

- Use a 390px PDA viewport.
- Confirm the expand/collapse control and expanded filter fields are usable
  without horizontal scrolling.

## 3. Verification Run History

### HVR-RUN-001

| Field | Value |
|---|---|
| Timestamp | 2026-09-24 |
| Verification type | Manual human verification |
| Environment | Odoo 18 PDA in the shared browser |
| Scenarios | HVR-SCN-001 through HVR-SCN-005 |
| Result | PASS |
| Evidence | User confirmed the PDA filter area collapse/expand behavior, arrow controls, filtering interaction, Clear behavior, and narrow-screen usability |

## 4. Evidence Rules

This HVR records the user's manual confirmation in HVR-RUN-001. It does not claim
additional device-specific behavior beyond the stated verification.
