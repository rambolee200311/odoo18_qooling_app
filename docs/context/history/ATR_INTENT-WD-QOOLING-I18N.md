# wd_qooling_app Internationalization Automated Test Record (ATR)

> Document status: Automated Checks Passed
> Intent ID: `INTENT-WD-QOOLING-I18N`
> IHR: [IHR_INTENT-WD-QOOLING-I18N.md](./IHR_INTENT-WD-QOOLING-I18N.md)
> Module: `wd_qooling_app`

## 1. Execution Metadata

| Field | Value |
|---|---|
| Environment | Odoo 18 / module worktree |
| Execution date | 2026-09-24 |
| Code baseline | Commit `540f7c8` |
| Executed by | Copilot |

## 2. Test Run History

### ATR-RUN-001

| Field | Value |
|---|---|
| Scope | Dutch and Simplified Chinese PO syntax |
| Invocation | GNU `msgfmt --check` |
| Result | PASS |
| Evidence | Both PO catalogs passed syntax validation |

### ATR-RUN-002

| Field | Value |
|---|---|
| Scope | Frontend translation integration |
| Invocation | `node --check` for PDA dashboard, Inbound PDA, Outbound PDA, Temperature PDA, and quick-entry JavaScript |
| Result | PASS |
| Evidence | All JavaScript files passed syntax validation |

### ATR-RUN-003

| Field | Value |
|---|---|
| Scope | English fallback and catalog completeness |
| Invocation | Catalog inspection |
| Result | PASS |
| Evidence | English source strings remain unchanged; Dutch and Chinese catalogs contain the extracted module messages and frontend dynamic messages |

### ATR-RUN-004

| Field | Value |
|---|---|
| Scope | Odoo translation catalog import |
| Invocation | `odoo-bin -c odoo.conf -d odoo18ce -u wd_qooling_app --stop-after-init --http-port=18088` |
| Result | PASS |
| Evidence | Module upgrade completed successfully after preserving module metadata and JavaScript translation markers |

### ATR-RUN-005

| Field | Value |
|---|---|
| Scope | Chinese Inbound PDA field display |
| Invocation | Playwright reload of the active `zh_CN` PDA page |
| Result | PASS |
| Evidence | Inbound location, date, supervisor, reference, container/shipment number, goods status, unloading permission, navigation, and step labels displayed in Chinese |

## 3. Evidence Boundary

These checks do not constitute human verification of language display in a
browser. HVR remains pending until a user confirms the selected languages.
