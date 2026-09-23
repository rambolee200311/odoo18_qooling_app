# Coding Contract: PDA Record Identity

**Status:** Frozen — Authorized for Implementation  
**Version:** 1.0.0  
**Approved:** 2026-09-23
**Scope:** Inbound, Outbound, and Temperature Record PDA screens

## 1. Objective

Ensure that a PDA user can identify the current business record while moving through
the workflow.

## 2. Contract

1. Each PDA header must display the record type and its Odoo document number.
2. The document number must come from the model `name` field and must be loaded when
   an existing draft is restored.
3. After the first save or submit creates a record, the generated document number
   must be refreshed and displayed without requiring a page reload.
4. A new unsaved form may display `New` as a temporary placeholder.
5. The same identity must remain visible on every PDA step, including Evidence and
   Signature.
6. Web form behavior and document numbering are unchanged.
7. No new business workflow, permission, sequence, or automatic submission behavior
   is introduced.

## 3. Acceptance

- Inbound PDA displays its `name`.
- Outbound PDA displays its `name`.
- Temperature Record PDA displays its `name`.
- Restored drafts show their persisted number.
- Newly saved drafts show the generated number immediately.
- The number remains visible while navigating all PDA steps.

## 4. Out of Scope

- Changing sequence definitions or document numbering rules.
- Adding a separate search or document selection flow.
- Changing Web form titles or layouts.
