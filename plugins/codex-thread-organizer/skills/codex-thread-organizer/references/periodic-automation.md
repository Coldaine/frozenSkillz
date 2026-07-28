# Periodic Codex Automation

## Mechanism

The organizer is a Codex skill. Continuous maintenance is a periodic Codex automation that explicitly invokes `$codex-thread-organizer`; it is not a background daemon inside the skill.

The frozenSkillz source is active only in its dedicated Codex plugin package. A Codex-targeted synchronization or native Codex install may install it; the package must remain absent from Claude, Cursor, and Gemini catalogs. Repository landing or installation alone does not create an automation.

## Safe Default Run

Unless the automation definition contains a narrower pre-authorized mutation scope:

On the first run, after checkpoint loss, or whenever no valid checkpoint exists, perform a full inventory. Keep the previous checkpoint if a run fails before its frozen manifest and audit report are successfully generated. Persist the next checkpoint only after successful report generation, and after mutation read-back when the run includes authorized writes.

1. inventory tasks changed since the previous successful run;
2. read the changed bodies and any related family members needed for context;
3. propose sparse title or relationship updates;
4. write or return a frozen manifest;
5. make no title, archive, pin, delete, or content mutation.

If title mutations are pre-authorized, the automation must still freeze the manifest, check for concurrent changes, enforce the title-length limit, apply with native Codex operations, and independently read back every result.

Archive and pin changes are never implied by title authorization.

## Suggested Cadence

Use an incremental frequent pass for newly changed tasks and a less frequent repository-family review for supersession. Cadence is an operator decision recorded in the automation definition, not hard-coded in the skill.

Every run should report:

- inventory and coverage totals;
- changed, unchanged, inaccessible, and ambiguous tasks;
- proposals and applied mutations as separate counts;
- exact verification results for applied mutations;
- whether any task was skipped due to concurrent change;
- the next review boundary or unresolved owner decision.
