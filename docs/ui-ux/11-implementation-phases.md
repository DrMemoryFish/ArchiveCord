# 11 — Implementation Phases

This file defines a safe phased implementation plan for the ArchiveCord UI/UX redesign.

Do not attempt the whole redesign in one uncontrolled pass. The current app already works. The redesign must preserve working behavior while improving structure and usability.

## Phase rules

1. Each phase must leave the app runnable.
2. Each phase must preserve export functionality.
3. Each phase must have a clear verification checklist.
4. Do not start attachment thumbnail previews until activity state and worker events are reliable.
5. Do not remove old UI surfaces until their replacement works.
6. Prefer small PRs/commits over one giant rewrite.

## Phase 0 — Documentation and planning

Status: documentation-only.

### Goals

- Add UI/UX specs.
- Add state machine.
- Add component contracts.
- Add migration map.
- Add QA plan.

### Files

- `docs/ui-ux/*`

### Do not change

- app runtime code
- backend export logic

### Verification

- docs exist
- docs are linked from README or project docs if desired
- no runtime behavior changed

## Phase 1 — Theme tokens and top bar cleanup

### Goals

- Create shared styling tokens.
- Start moving toward the new top bar.
- Group connection state with account.
- Avoid permanent token dominance after connection where possible.

### Suggested files

- `app/ui/theme.py`
- `app/ui/top_bar.py`
- `app/ui/account_status_cluster.py`
- update `app/ui/main_window.py`

### Work

1. Add centralized color/spacing/radius constants matching `00-design-system.md`.
2. Create a reusable top bar component or top bar builder.
3. Move connected/disconnected display into right-side account cluster.
4. Preserve token input behavior for disconnected state if full connect panel is not ready yet.
5. Ensure existing connect flow still works.

### Do not do yet

- remove conversation tree
- remove tabs
- build activity tray
- implement thumbnails

### Verification

- app launches
- token connect still works
- saved token loading still works
- connected status appears with account/top-right cluster
- no export behavior changed
- `python -m compileall app tests`
- existing tests pass

## Phase 2 — Main workspace shell and connect/empty states

### Goals

- Introduce `MainWorkspace` state rendering.
- Create disconnected/connect panel.
- Create connected/no-selection panel.
- Keep old export controls temporarily if needed behind the same app.

### Suggested files

- `app/ui/main_workspace.py`
- `app/ui/connect_panel.py`
- `app/ui/empty_selection_panel.py`
- `app/ui/view_models.py`

### Work

1. Create explicit workflow state enum or equivalent.
2. Render `DISCONNECTED`, `CONNECTING`, and `CONNECTED_EMPTY` states through `MainWorkspace`.
3. Move token entry out of permanent top bar into `ConnectPanel` for disconnected state.
4. Keep account/settings access in top bar.
5. Ensure connect errors display inline in connect panel.

### Do not do yet

- replace all export summary UI
- move full tree to drawer unless ready

### Verification

- disconnected launch shows connect panel
- invalid token shows error without crashing
- valid token loads conversations
- after connection and no selection, user sees `Choose conversations to export`
- selection still possible through current tree if drawer not implemented yet

## Phase 3 — Export summary panel

### Goals

- Replace visible form-heavy export page with ready summary rows.
- Keep detailed controls available through row edit/advanced options.

### Suggested files

- `app/ui/export_summary_panel.py`
- `app/ui/summary_row.py`
- update `main_workspace.py`

### Work

1. Build `ExportSummaryPanel` for `READY_TO_EXPORT`.
2. Add rows: selected conversations, format, date range, destination, advanced options.
3. Add primary `Export` button.
4. Wire row actions to existing controls or simple editors.
5. Keep advanced details collapsed by default.
6. Keep export preflight checks.

### Do not do yet

- remove current tree if selector drawer is not ready
- implement activity tray replacement unless phase 5 is ready

### Verification

- selecting one/multiple targets shows ready summary
- Export button works
- output folder can be changed
- date filters can still be configured
- TXT/JSON/attachments settings still affect export
- existing export tests pass

## Phase 4 — Conversation selector drawer

### Goals

- Move conversation tree from permanent left panel into drawer.
- Preserve selection behavior.
- Keep workspace stable when drawer opens.

### Suggested files

- `app/ui/conversation_selector_drawer.py`
- `app/ui/conversation_tree.py`

### Work

1. Extract current tree construction/selection logic into reusable selector component.
2. Add drawer overlay behavior.
3. Add search input inside drawer.
4. Add All/DMs/Servers segmented filter.
5. Add pinned footer with selected count and Done.
6. Wire `Change selection` and top bar selector button to open drawer.
7. Remove permanent tree from default ready/exporting/complete layout only after drawer works.

### Critical preservation

- tri-state parent behavior
- disabled/unavailable rows
- icon loading/cache
- keyboard Space/Enter behavior
- selected target data structure

### Verification

- drawer opens/closes without losing selection
- search filters without clearing selection
- All/DMs/Servers filters work
- selected count updates
- Done closes drawer
- ready summary updates
- opening drawer does not shove workspace around

## Phase 5 — Activity tray and completion panels

### Goals

- Replace generic progress area with activity tray.
- Show per-job status rows.
- Add completion panel.

### Suggested files

- `app/ui/activity_tray.py`
- `app/ui/activity_job_row.py`
- `app/ui/completion_panel.py`

### Work

1. Create job view model adapter from current export worker/batch worker signals.
2. Render `EXPORTING` state with activity tray.
3. Show queued/running/complete/failed rows.
4. Add truthful cancel behavior based on backend.
5. Render success completion state.
6. Render partial failure and failed states.
7. Add Open folder, Retry failed, Details actions where supported.

### Backend caution

If current backend only runs one job at a time, UI must say:

- `1 running · N queued`

Do not say multiple jobs are active unless true.

### Verification

- single export progress appears as job row
- batch export shows queued/current/complete rows
- failed item does not stop remaining batch unless backend does
- cancel copy matches actual behavior
- completion state opens output folder
- logs still captured in diagnostics

## Phase 6 — Settings and diagnostics migration

### Goals

- Move token management and logs into settings/diagnostics.
- Remove Logs as a primary tab.

### Suggested files

- `app/ui/settings_view.py`
- `app/ui/diagnostics_view.py`

### Work

1. Build Settings with sections: Account, Appearance, Export defaults, Activity & previews, Diagnostics, About.
2. Move token update/reveal/remember controls into Account.
3. Move default export folder/format defaults into Export defaults.
4. Embed or reuse current `LogTab` in Diagnostics.
5. Preserve current log filtering/copy/clear behavior.
6. Keep settings state from disrupting active export.

### Verification

- token can be managed in Settings
- saved token behavior preserved
- theme mode setting works if implemented
- logs visible under Diagnostics
- logs no longer primary tab by default
- closing settings returns to previous workflow state

## Phase 7 — Attachment preview support

### Goals

- Add optional recent attachment previews inside expanded activity job rows.

### Required backend readiness

Do not start this phase until the backend/UI adapter can provide:

- attachment saved event
- attachment id
- filename
- local file path
- mime type or previewability
- status: saving/saved/failed/skipped

### Work

1. Add thumbnail generation worker/thread.
2. Generate low-resolution thumbnails only.
3. Add temporary cache with cleanup.
4. Add `AttachmentPreviewStrip` in expanded job rows.
5. Add settings controls for live previews/cache.
6. Ensure UI thread does not block.

### Verification

- exporting image attachments does not freeze UI
- recent thumbnails appear only when row is expanded or latest preview is shown
- non-previewable files show file icons
- cache clears after export by default
- large images do not spike memory

## Phase 8 — Polish, accessibility, and regression QA

### Goals

- Tighten visual consistency.
- Validate keyboard and screen-reader behavior.
- Remove old unused UI code.

### Work

1. Remove old permanent tree layout if fully replaced.
2. Remove primary Logs tab if diagnostics replacement works.
3. Verify focus order.
4. Verify dark mode if implemented.
5. Add manual QA checklist to release notes or test docs.
6. Clean dead code.

### Verification

- QA checklist in `12-qa-acceptance-tests.md` passes
- existing backend tests pass
- compileall passes
- app can complete a real export

## Suggested commit structure

Recommended PR/commit sequence:

1. `Add UI theme tokens and top bar components`
2. `Add workflow state shell`
3. `Add export summary workspace`
4. `Move conversation tree into selector drawer`
5. `Add export activity tray and completion state`
6. `Move logs and token management into settings`
7. `Add optional attachment preview support`
8. `Polish accessibility and remove old UI scaffolding`

## Stop conditions

Stop and ask for review if:

- a phase requires backend behavior that does not exist
- moving the tree breaks selection correctness
- cancellation behavior cannot match the proposed UI
- thumbnail generation risks freezing UI
- app cannot complete a basic export after a phase

Do not cover these up with UI polish.