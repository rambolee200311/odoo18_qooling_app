# Coding Contract: PDA Record Dashboard

**Status:** Frozen — Authorized for Implementation
**Version:** 1.0.0
**Approved:** 2026-09-23
**Scope:** Inbound, Outbound, and Temperature Record PDA entry actions

## 1. Objective

Provide a PDA landing dashboard so users can select an existing business record
instead of entering a form without knowing which document they are editing.

## 2. Contract

1. Each PDA entry action opens a record dashboard for its model:
   - Inbound records;
   - Outbound records;
   - Temperature records.
2. The dashboard lists records the current user is allowed to read, ordered by
   newest record first.
3. Each row displays at minimum:
   - document number (`name`);
   - record status;
   - a useful date field;
   - the primary business reference when available.
4. The dashboard provides a clear action to create a new PDA record.
5. Selecting an existing draft opens that record in the existing PDA workflow and
   allows editing under the current server-side permissions.
6. Selecting a submitted record opens the existing PDA workflow in read-only mode;
   it must not enable draft-only writes, media changes, signatures, or submission.
7. The dashboard must provide an explicit way to return to the Qooling dashboard.
8. Record loading and opening must use Odoo ORM/action context; no direct database
   access or client-side permission bypass is introduced.
9. Web list/form behavior and existing document numbering remain unchanged.
10. Empty lists and load failures must show clear user-facing states.

## 3. Acceptance

- Inbound PDA shows a historical record list and can open a draft or create new.
- Outbound PDA shows a historical record list and can open a draft or create new.
- Temperature PDA shows a historical record list and can open a draft or create new.
- Submitted records are visible when readable but are read-only.
- Draft records can be resumed and retain their document number.
- The dashboard never silently opens an arbitrary record.

## 4. Out of Scope

- Changing model ACLs or record rules.
- Changing Web list views.
- Adding search, pagination, filters, or bulk actions beyond what is required for
  the initial usable record list.
- Changing submission, signature, inventory, release, quarantine, or notification
  business rules.

## 5. Verification

Automated verification must cover action routing, record loading, draft resume,
submitted read-only behavior, empty/error states, and the three PDA entry points.
Human verification must confirm that a user can identify and select the intended
document before editing.
