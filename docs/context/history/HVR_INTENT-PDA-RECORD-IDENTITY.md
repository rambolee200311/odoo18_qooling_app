# PDA Record Identity Human Verification Record (HVR)

> Document status: Pending Human Verification
> Intent ID: `INTENT-PDA-RECORD-IDENTITY`
> CC: [Coding_Contract_PDA_Record_Identity.md](../intent/Coding_Contract_PDA_Record_Identity.md) `v1.0.0 Frozen`
> IHR: [IHR_INTENT-PDA-RECORD-IDENTITY.md](./IHR_INTENT-PDA-RECORD-IDENTITY.md)
> ATR: [ATR_INTENT-PDA-RECORD-IDENTITY.md](./ATR_INTENT-PDA-RECORD-IDENTITY.md)

## 1. Verification Status

| Field | Value |
|---|---|
| Human verification required | Yes |
| Status | Pending |
| Verification date | Not yet recorded |
| Human verifier | Not yet recorded |
| Result | Not run |

## 2. Required Scenarios

### HVR-SCN-001 — Inbound PDA identity

- Open an existing Inbound PDA draft.
- Confirm the header shows the persisted document number.
- Move through Details, Checks, ADR, Evidence, and Signature.
- Confirm the same number remains visible.

### HVR-SCN-002 — Outbound PDA identity

- Open an existing Outbound PDA draft.
- Confirm the header shows the persisted document number.
- Move through all Outbound PDA steps.
- Confirm the same number remains visible.

### HVR-SCN-003 — Temperature PDA identity

- Open an existing Temperature Record PDA draft.
- Confirm the header shows the persisted document number.
- Move through Details, Temperatures, Checks, Evidence, and Signature.
- Confirm the same number remains visible.

### HVR-SCN-004 — Newly created draft

- Start a new PDA record and confirm the temporary label is `New`.
- Save the draft.
- Confirm the generated document number appears immediately without reloading.

## 3. Evidence Rules

Until the user confirms these scenarios, this HVR must remain Pending and must not be
described as passed.
