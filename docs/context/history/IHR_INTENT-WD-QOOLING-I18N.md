# wd_qooling_app Internationalization Implementation History Record (IHR)

> Document status: Implementation Complete; ATR Recorded; HVR Pending
> Intent ID: `INTENT-WD-QOOLING-I18N`
> Module: `wd_qooling_app`
> Implementation date: 2026-09-24

## 1. Execution Metadata

| Field | Value |
|---|---|
| Branch | `agents/docs-review-summary` |
| Implementation commits | `1deb0a9`, `48245a1`, `0e11f3b`, `540f7c8` |
| Default language | English source strings and English fallback |
| Added languages | Dutch (`nl_NL`), Simplified Chinese (`zh_CN`) |
| Status | Implementation Complete; ATR Recorded; HVR Pending |

## 2. Implementation Records

### IHR-001

| Field | Content |
|---|---|
| Phase | Catalog |
| Action | Exported the module translation catalog from Odoo and created Dutch and Simplified Chinese PO files |
| Reason | Provide complete module-level translation resources without changing English source defaults |
| Files | `i18n/nl.po`; `i18n/zh_CN.po` |
| Result | Completed |

### IHR-002

| Field | Content |
|---|---|
| Phase | Frontend |
| Action | Connected PDA dashboard and PDA step labels to Odoo frontend `_t` translation |
| Reason | Ensure dynamic JavaScript labels use the selected language instead of bypassing i18n |
| Files | `pda_record_dashboard.js`; `inbound_pda.js`; `outbound_pda.js`; `temperature_pda.js` |
| Result | Completed |

### IHR-003

| Field | Content |
|---|---|
| Phase | PDA field coverage |
| Action | Added translations for all visible Inbound, Outbound, and Temperature Web/PDA field labels, options, checks, evidence controls, signatures, and navigation actions |
| Reason | Ensure the selected language applies consistently to the complete user-facing form surface |
| Files | `static/src/xml/inbound_pda.xml`; `static/src/xml/outbound_pda.xml`; `static/src/xml/temperature_pda.xml`; `static/src/js/outbound_pda.js`; `static/src/js/temperature_pda.js`; `i18n/nl.po`; `i18n/zh_CN.po` |
| Result | Completed |

### IHR-004

| Field | Content |
|---|---|
| Phase | Odoo catalog loading |
| Action | Preserved Odoo module metadata and marked dynamic frontend messages with the `odoo-javascript` translation marker |
| Reason | Make JavaScript `_t` messages available to the Odoo web client instead of falling back to English |
| Result | Completed |

## 3. Language Boundary

- English remains the source language and fallback when no translation is
  available.
- The module does not force a global user language; Odoo user language settings
  select Dutch or Simplified Chinese.
- No Odoo official code or direct database access was changed.
