# PDA Record Dashboard Filter Automated Test Record (ATR)

> Document status: Automated Checks Passed
> Intent ID: `INTENT-PDA-RECORD-DASHBOARD-FILTER`
> CC: [Coding_Contract_PDA_Record_Dashboard_Filter.md](../intent/Coding_Contract_PDA_Record_Dashboard_Filter.md) `v1.0.0 Frozen`
> IHR: [IHR_INTENT-PDA-RECORD-DASHBOARD-FILTER.md](./IHR_INTENT-PDA-RECORD-DASHBOARD-FILTER.md)
> Module: `wd_qooling_app`

## 1. Execution Metadata

| Field | Value |
|---|---|
| Environment | Odoo 18 / `http://127.0.0.1:18087` |
| Test framework | Node syntax, XML parse, `git diff --check`, shared-browser Playwright |
| Code baseline | Commit `605e519` |
| Execution date | 2026-09-24 |
| Executed by | Copilot |

## 2. Test Run History

### ATR-RUN-001

| Field | Value |
|---|---|
| Scope | PDA dashboard filter implementation |
| Result | PASS |
| Evidence | JavaScript syntax, XML parsing, and whitespace checks passed; Inbound fuzzy number filtering returned `INB/00156`; Clear restored 10 records; Draft status returned 8 records; inclusive same-day filtering returned 8 records; invalid date order showed a validation message; combined number plus Draft filtering returned 5 records |

### ATR-RUN-002

| Field | Value |
|---|---|
| Scope | Three PDA dashboard filter surfaces |
| Invocation | Shared browser Playwright |
| Result | PASS |
| Evidence | Inbound loaded 10 records with filter controls; Outbound loaded 3 records with filter controls; Temperature loaded 6 records with filter controls and statuses Draft, Submitted, Exception pending, and Closed |

### ATR-RUN-003

| Field | Value |
|---|---|
| Scope | Narrow-screen filter layout |
| Invocation | Shared browser Playwright at 390x844 |
| Result | PASS |
| Evidence | Temperature dashboard rendered 6 cards, hid the table, kept filter width within the viewport, and reported `body.scrollWidth = 390` |

## 3. Evidence Boundary

These are automated and Playwright execution results. They do not constitute
real-device camera, touch, or human verification.
