# PDA Record Dashboard Filter Collapse Automated Test Record (ATR)

> Document status: Automated Checks Passed
> Intent ID: `INTENT-PDA-RECORD-DASHBOARD-FILTER-COLLAPSE`
> CC: [Coding_Contract_PDA_Record_Dashboard_Filter_Collapse.md](../intent/Coding_Contract_PDA_Record_Dashboard_Filter_Collapse.md) `v1.0.0 Frozen`
> IHR: [IHR_INTENT-PDA-RECORD-DASHBOARD-FILTER-COLLAPSE.md](./IHR_INTENT-PDA-RECORD-DASHBOARD-FILTER-COLLAPSE.md)
> Module: `wd_qooling_app`

## 1. Execution Metadata

| Field | Value |
|---|---|
| Environment | Odoo 18 / `http://127.0.0.1:18087` |
| Test framework | Node syntax, XML parse, `git diff --check`, shared-browser Playwright |
| Code baseline | Commit `a77cbd6` |
| Execution date | 2026-09-24 |
| Executed by | Copilot |

## 2. Test Run History

### ATR-RUN-001

| Field | Value |
|---|---|
| Scope | Default and expanded filter states |
| Result | PASS |
| Evidence | Dashboard opened with `Show filters`, no filter form visible; expanding showed the complete filter form and `aria-expanded="true"` |

### ATR-RUN-002

| Field | Value |
|---|---|
| Scope | Filter collapse and Clear behavior |
| Result | PASS |
| Evidence | Filtering document number `156` returned one row and collapsed the area with `aria-expanded="false"` and `Filters applied`; expanding and clearing restored 10 rows while leaving the area open |

### ATR-RUN-003

| Field | Value |
|---|---|
| Scope | Narrow-screen collapse layout |
| Invocation | Shared browser Playwright at 390x844 |
| Result | PASS |
| Evidence | Collapsed control width 99.875px; collapsed and expanded body width remained 390px; expanded filter width was 366px |

### ATR-RUN-004

| Field | Value |
|---|---|
| Scope | Arrow expand/collapse control |
| Invocation | Shared browser Playwright |
| Result | PASS |
| Evidence | Collapsed control rendered `fa-chevron-down` with `aria-label="Show filters"` and `aria-expanded="false"`; expanded control rendered `fa-chevron-up` with `aria-label="Hide filters"` and `aria-expanded="true"` |

## 3. Evidence Boundary

These are automated and Playwright execution results. They do not constitute
real-device or human verification.
