# PDA Record Dashboard Automated Test Record (ATR)

> Document status: Automated Checks Passed
> Intent ID: `INTENT-PDA-RECORD-DASHBOARD`
> CC: [Coding_Contract_PDA_Record_Dashboard.md](../intent/Coding_Contract_PDA_Record_Dashboard.md) `v1.0.0 Frozen`
> IHR: [IHR_INTENT-PDA-RECORD-DASHBOARD.md](./IHR_INTENT-PDA-RECORD-DASHBOARD.md)
> Module: `wd_qooling_app`

## 1. Execution Metadata

| Field | Value |
|---|---|
| Environment | Odoo 18 / `http://127.0.0.1:18087` |
| Test framework | Node syntax, project Python XML parse, Python compile, `git diff --check` |
| Code baseline | Commit `717ec66` |
| Execution date | 2026-09-23 |
| Executed by | Copilot |

## 2. Test Contract Coverage

| CC acceptance | Automated coverage | Result |
|---|---|---|
| Three PDA dashboard actions are defined | XML and manifest inspection | PASS |
| Dashboard uses ORM record loading | JavaScript inspection | PASS |
| Draft and submitted states are routed | JavaScript inspection | PASS |
| New record routing clears stale draft context | JavaScript inspection | PASS |
| Dashboard opens the intended record | Playwright interaction | PASS |
| Submitted record is visibly read-only | Playwright interaction | PASS |

## 3. Test Run History

### ATR-RUN-001

| Field | Value |
|---|---|
| Scope | Dashboard and PDA JavaScript syntax |
| Invocation | `node --check` for dashboard and all PDA files |
| Result | PASS |
| Evidence | All commands exited with status 0 |

### ATR-RUN-002

| Field | Value |
|---|---|
| Scope | Dashboard, action, and PDA XML syntax |
| Invocation | Project `venv/bin/python` with `xml.etree.ElementTree` |
| Result | PASS |
| Evidence | Dashboard view, dashboard template, and all PDA XML files parsed |

### ATR-RUN-003

| Field | Value |
|---|---|
| Scope | Dashboard model/action regression test source |
| Invocation | Project `venv/bin/python -m py_compile tests/test_qooling_dashboard.py` |
| Result | PASS |
| Evidence | Test source compiled successfully |

### ATR-RUN-004

| Field | Value |
|---|---|
| Scope | Working tree integrity |
| Invocation | `git diff --check` |
| Result | PASS |
| Evidence | No whitespace errors |

### ATR-RUN-005

| Field | Value |
|---|---|
| Scope | PDA dashboard Playwright verification |
| Invocation | Shared browser Playwright against `http://127.0.0.1:18087` |
| Executed | Inbound, Outbound, and Temperature history lists; Draft open; Submitted read-only; New record |
| Result | PASS |
| Evidence | Inbound 10 rows; Outbound 3 rows; Temperature 6 rows; Draft `INB/00156` opened; Submitted `INB/00148` read-only; New Inbound displayed `New` |

### ATR-RUN-006

| Field | Value |
|---|---|
| Scope | Narrow-screen PDA dashboard layout |
| Invocation | Shared browser Playwright at 390x844 viewport |
| Executed | Inbound PDA history dashboard |
| Result | PASS |
| Evidence | 10 mobile cards rendered; desktop table hidden; card width 358px; body width matched 390px viewport with no horizontal overflow |

## 5. Findings and Resolution

- Initial browser run used stale assets and could not find the new dashboard action
  registry key; Odoo was restarted to rebuild assets.
- Module upgrade initially exposed the Inbound attachment relation column mismatch;
  the existing `inbound_id` schema was restored and the upgrade then succeeded.

## 4. Handoff

Static checks and Playwright verification passed for the executed dashboard scope.
