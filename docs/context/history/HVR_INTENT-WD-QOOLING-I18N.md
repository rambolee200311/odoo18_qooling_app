# wd_qooling_app Internationalization Human Verification Record (HVR)

> Document status: Pending Human Verification
> Intent ID: `INTENT-WD-QOOLING-I18N`
> IHR: [IHR_INTENT-WD-QOOLING-I18N.md](./IHR_INTENT-WD-QOOLING-I18N.md)
> ATR: [ATR_INTENT-WD-QOOLING-I18N.md](./ATR_INTENT-WD-QOOLING-I18N.md)
> Module: `wd_qooling_app`

## 1. Verification Status

| Field | Value |
|---|---|
| Human verification required | Yes |
| Status | Pending |
| Verification date | Not yet recorded |
| Human verifier | Not yet recorded |
| Result | Not run |

## 2. Required Scenarios

### HVR-SCN-001 — English default

- Use English as the user language.
- Confirm the Qooling dashboard, Web forms, PDA forms, PDA record dashboards,
  filter controls, alerts, and actions display English source labels.

### HVR-SCN-002 — Dutch

- Switch the user language to Dutch (`nl_NL`).
- Confirm the Qooling dashboard, Web forms, PDA forms, PDA record dashboards,
  filter controls, statuses, alerts, and actions display Dutch translations.

### HVR-SCN-003 — Simplified Chinese

- Switch the user language to Simplified Chinese (`zh_CN`).
- Confirm the same surfaces display Simplified Chinese translations.

### HVR-SCN-004 — PDA filter interaction

- In English, Dutch, and Simplified Chinese, expand the PDA filter area.
- Confirm the arrow control, date labels, document-number label, status dropdown,
  Filter, Clear, empty-result, and validation messages use the selected language.

## 3. Evidence Rules

This HVR remains Pending until the user confirms all three language scenarios.
Automated catalog checks do not replace browser language verification.
