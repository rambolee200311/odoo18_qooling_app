# PDA Record Identity Automated Test Record (ATR)

> Document status: Partial; Static and XML Checks Passed; Browser Run Pending
> Intent ID: `INTENT-PDA-RECORD-IDENTITY`
> CC: [Coding_Contract_PDA_Record_Identity.md](../intent/Coding_Contract_PDA_Record_Identity.md) `v1.0.0 Frozen`
> IHR: [IHR_INTENT-PDA-RECORD-IDENTITY.md](./IHR_INTENT-PDA-RECORD-IDENTITY.md)
> Module: `wd_qooling_app`

## 1. Execution Metadata

| Field | Value |
|---|---|
| Environment | Odoo 18 / `http://127.0.0.1:18087` |
| Test framework | Node syntax, project Python XML parse, `git diff --check` |
| Code baseline | Commit `520904f` |
| Execution date | 2026-09-23 |
| Executed by | Copilot |

## 2. Test Contract Coverage

| CC acceptance | Automated coverage | Result |
|---|---|---|
| Inbound header renders `name` | XML/template inspection | PASS |
| Outbound header renders `name` | XML/template inspection | PASS |
| Temperature header renders `name` | XML/template inspection | PASS |
| Draft fields include persisted `name` | JavaScript source inspection | PASS |
| New record refreshes generated `name` | JavaScript source inspection | PASS |
| Number remains visible across steps | Browser interaction | NOT RUN |

## 3. Test Run History

### ATR-RUN-001

| Field | Value |
|---|---|
| Scope | PDA JavaScript syntax |
| Invocation | `node --check` for Inbound, Outbound, and Temperature PDA files |
| Result | PASS |
| Evidence | All three commands exited with status 0 |

### ATR-RUN-002

| Field | Value |
|---|---|
| Scope | PDA XML syntax |
| Invocation | Project `venv/bin/python` with `xml.etree.ElementTree` over all `*_pda.xml` files |
| Result | PASS |
| Evidence | All three PDA XML files parsed successfully |

### ATR-RUN-003

| Field | Value |
|---|---|
| Scope | Working tree integrity |
| Invocation | `git diff --check` |
| Result | PASS |
| Evidence | No whitespace errors |

## 4. Handoff

Static and XML checks passed. Browser verification of the visible generated number is
not recorded as automated evidence yet and must not be treated as PASS.
