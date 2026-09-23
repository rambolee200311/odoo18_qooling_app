# PDA Record Dashboard Human Verification Record (HVR)

> Document status: Pending Human Verification
> Intent ID: `INTENT-PDA-RECORD-DASHBOARD`
> CC: [Coding_Contract_PDA_Record_Dashboard.md](../intent/Coding_Contract_PDA_Record_Dashboard.md) `v1.0.0 Frozen`
> IHR: [IHR_INTENT-PDA-RECORD-DASHBOARD.md](./IHR_INTENT-PDA-RECORD-DASHBOARD.md)
> ATR: [ATR_INTENT-PDA-RECORD-DASHBOARD.md](./ATR_INTENT-PDA-RECORD-DASHBOARD.md)

## 1. Verification Status

| Field | Value |
|---|---|
| Human verification required | Yes |
| Status | Pending |
| Verification date | Not yet recorded |
| Human verifier | Not yet recorded |
| Result | Not run |

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

## 3. Evidence Rules

Until the user confirms these scenarios, this HVR must remain Pending and must not be
described as passed.
