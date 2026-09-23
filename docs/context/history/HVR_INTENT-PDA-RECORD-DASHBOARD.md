# PDA Record Dashboard Human Verification Record (HVR)

> Document status: Human Verification Passed
> Intent ID: `INTENT-PDA-RECORD-DASHBOARD`
> CC: [Coding_Contract_PDA_Record_Dashboard.md](../intent/Coding_Contract_PDA_Record_Dashboard.md) `v1.0.0 Frozen`
> IHR: [IHR_INTENT-PDA-RECORD-DASHBOARD.md](./IHR_INTENT-PDA-RECORD-DASHBOARD.md)
> ATR: [ATR_INTENT-PDA-RECORD-DASHBOARD.md](./ATR_INTENT-PDA-RECORD-DASHBOARD.md)

## 1. Verification Status

| Field | Value |
|---|---|
| Human verification required | Yes |
| Status | Passed |
| Verification date | 2026-09-23 |
| Human verifier | Playwright-simulated human verification in shared browser |
| Result | Passed |

## 2. Required Scenarios

### HVR-SCN-001 — Inbound PDA history

- Open Inbound PDA from the Qooling Dashboard.
- Confirm a historical record list is shown with document number and status.
- Open a Draft record and confirm the existing PDA form is restored.

### HVR-SCN-002 — Outbound PDA history

- Open Outbound PDA from the Qooling Dashboard.
- Confirm historical records are listed and a Draft can be opened for editing.

### HVR-SCN-003 — Temperature PDA history

- Open Temperature Record PDA from the Qooling Dashboard.
- Confirm historical records are listed and a Draft can be opened for editing.

### HVR-SCN-004 — Submitted record read-only

- Open a submitted record from any PDA dashboard.
- Confirm the read-only notice is shown and Save/Submit actions are unavailable.

### HVR-SCN-005 — New record

- Use `New record` from each PDA dashboard.
- Confirm an empty PDA form opens without accidentally restoring an unrelated draft.

### HVR-SCN-006 — Narrow-screen dashboard

- Set the PDA dashboard viewport to a narrow mobile width.
- Confirm records render as single-column cards rather than clipped table columns.
- Confirm the document number, status, date, reference, and action remain readable.

## 3. Verification Run History

### HVR-RUN-001

| Field | Value |
|---|---|
| Timestamp | 2026-09-23 |
| Verification type | Playwright-simulated human verification |
| Environment | Odoo 18 shared browser at `http://127.0.0.1:18087` |
| Scenarios | HVR-SCN-001 through HVR-SCN-005 |
| Result | PASS |
| Evidence | Inbound history 10 rows; Outbound history 3 rows; Temperature history 6 rows; Draft `INB/00156` opened with PDA form; Submitted `INB/00148` showed read-only notice with no Save/Submit; New Inbound showed `New` |

### HVR-RUN-002

| Field | Value |
|---|---|
| Timestamp | 2026-09-23 |
| Verification type | Playwright-simulated human verification |
| Environment | Odoo 18 shared browser at 390x844 |
| Scenario | HVR-SCN-006 |
| Result | PASS |
| Evidence | 10 single-column cards; table hidden; 358px card width inside 390px viewport; no horizontal overflow |

### HVR-RUN-003

| Field | Value |
|---|---|
| Timestamp | 2026-09-23 |
| Verification type | Manual human verification |
| Environment | Odoo 18 PDA in the shared browser |
| Scenarios | HVR-SCN-001 through HVR-SCN-006 |
| Result | PASS |
| Evidence | User confirmed the PDA history dashboards and their record navigation, including the narrow-screen card layout |

## 4. Findings

- The first run required an Odoo restart to rebuild frontend assets.
- The Inbound relation schema mismatch was corrected before the successful run.

## 5. Evidence Rules

This HVR records only the scenarios executed through the shared browser and does not
claim additional device-specific camera or touch behavior.
