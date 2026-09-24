# PDA Record Dashboard Filter Human Verification Record (HVR)

> Document status: Pending Human Verification
> Intent ID: `INTENT-PDA-RECORD-DASHBOARD-FILTER`
> CC: [Coding_Contract_PDA_Record_Dashboard_Filter.md](../intent/Coding_Contract_PDA_Record_Dashboard_Filter.md) `v1.0.0 Frozen`
> IHR: [IHR_INTENT-PDA-RECORD-DASHBOARD-FILTER.md](./IHR_INTENT-PDA-RECORD-DASHBOARD-FILTER.md)
> ATR: [ATR_INTENT-PDA-RECORD-DASHBOARD-FILTER.md](./ATR_INTENT-PDA-RECORD-DASHBOARD-FILTER.md)

## 1. Verification Status

| Field | Value |
|---|---|
| Human verification required | Yes |
| Status | Pending |
| Verification date | Not yet recorded |
| Human verifier | Not yet recorded |
| Result | Not run |

## 2. Required Scenarios

### HVR-SCN-001 — Inbound filters

- Open the Inbound PDA dashboard.
- Apply date, fuzzy document number, and status filters.
- Confirm the result identifies the intended records.
- Confirm Draft opens editable and Submitted opens read-only.

### HVR-SCN-002 — Outbound filters

- Open the Outbound PDA dashboard.
- Apply date, fuzzy document number, and status filters.
- Confirm the result list and actions remain correct.

### HVR-SCN-003 — Temperature filters

- Open the Temperature Record PDA dashboard.
- Confirm the status dropdown includes the statuses supported by the model.
- Apply filters and confirm the result list remains correct.

### HVR-SCN-004 — Clear and validation

- Leave `From` and `To` blank and confirm the unfiltered list loads.
- Enter an invalid date range and confirm a visible validation message.
- Use `Clear` and confirm all controls empty and the newest-first list returns.

### HVR-SCN-005 — Narrow PDA layout

- Use a narrow PDA viewport.
- Confirm all filter controls and both buttons are usable without horizontal
  scrolling.
- Confirm filtered cards remain readable.

## 3. Evidence Rules

This HVR remains Pending until the user confirms the required scenarios. Automated
or Playwright-simulated results must not be described as real human verification.
