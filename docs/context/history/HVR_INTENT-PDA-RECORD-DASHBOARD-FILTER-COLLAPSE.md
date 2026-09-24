# PDA Record Dashboard Filter Collapse Human Verification Record (HVR)

> Document status: Pending Human Verification
> Intent ID: `INTENT-PDA-RECORD-DASHBOARD-FILTER-COLLAPSE`
> CC: [Coding_Contract_PDA_Record_Dashboard_Filter_Collapse.md](../intent/Coding_Contract_PDA_Record_Dashboard_Filter_Collapse.md) `v1.0.0 Frozen`
> IHR: [IHR_INTENT-PDA-RECORD-DASHBOARD-FILTER-COLLAPSE.md](./IHR_INTENT-PDA-RECORD-DASHBOARD-FILTER-COLLAPSE.md)
> ATR: [ATR_INTENT-PDA-RECORD-DASHBOARD-FILTER-COLLAPSE.md](./ATR_INTENT-PDA-RECORD-DASHBOARD-FILTER-COLLAPSE.md)

## 1. Verification Status

| Field | Value |
|---|---|
| Human verification required | Yes |
| Status | Pending |
| Verification date | Not yet recorded |
| Human verifier | Not yet recorded |
| Result | Not run |

## 2. Required Scenarios

### HVR-SCN-001 — Default collapsed state

- Open each PDA history dashboard.
- Confirm the filter area is collapsed and `Show filters` is visible.

### HVR-SCN-002 — Expand and retain values

- Expand the filter area.
- Enter filter values, collapse it, and expand it again.
- Confirm the values remain visible.

### HVR-SCN-003 — Filter auto-collapse

- Apply a valid filter.
- Confirm the filter area automatically collapses.
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

## 3. Evidence Rules

This HVR remains Pending until the user confirms the required scenarios. Automated
or Playwright-simulated results must not be described as real human verification.
