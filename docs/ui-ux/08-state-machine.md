# 08 — UI State Machine

This file defines ArchiveCord's GUI as a strict state machine. It exists to prevent the redesign from becoming a set of loosely connected pages.

A developer must use these states and transitions as the source of truth for what is visible, enabled, disabled, or blocked.

## 1. State names

Use these canonical state names in code, tests, comments, and docs where practical.

| State | Meaning |
|---|---|
| `DISCONNECTED` | App is open but no usable Discord session is loaded. |
| `CONNECTING` | User submitted a token and conversations/account data are loading. |
| `CONNECTED_EMPTY` | Connected successfully, but no conversations are selected. |
| `SELECTOR_OPEN` | Conversation selector drawer is open over the current workflow state. |
| `READY_TO_EXPORT` | Connected, at least one conversation selected, export can be reviewed. |
| `EXPORTING` | One or more export jobs are running, queued, or finalizing. |
| `EXPORT_COMPLETE` | All requested exports completed successfully. |
| `EXPORT_PARTIAL_FAILURE` | Some exports completed and one or more failed/cancelled. |
| `EXPORT_FAILED` | No export completed successfully. |
| `SETTINGS_OPEN` | Settings surface is open over or instead of the current workflow state. |

`SELECTOR_OPEN` and `SETTINGS_OPEN` are overlay/surface states. They must preserve the underlying workflow state.

Example:

```text
READY_TO_EXPORT + SELECTOR_OPEN
EXPORTING + SETTINGS_OPEN
```

Do not destroy underlying state when opening these surfaces.

## 2. State data model

The UI state must be derived from explicit data, not scattered widget visibility guesses.

Recommended state object:

```python
@dataclass
class UiWorkflowState:
    connection_state: ConnectionState
    workflow_state: WorkflowState
    selector_open: bool
    settings_open: bool
    selected_targets: list[ExportTargetViewModel]
    export_options: ExportOptionsViewModel
    export_jobs: list[ExportJobViewModel]
    last_result: ExportRunResultViewModel | None
    active_error: UiErrorViewModel | None
```

Exact names may vary, but the concept must exist: one place computes the visible UI state.

## 3. Primary action by state

Each state gets one dominant action.

| State | Primary action | Button text |
|---|---|---|
| `DISCONNECTED` | Submit token/connect | `Connect` |
| `CONNECTING` | None; connection is in progress | disabled `Connecting...` or spinner |
| `CONNECTED_EMPTY` | Open selector | `Select conversations` |
| `READY_TO_EXPORT` | Start export | `Export` |
| `EXPORTING` | No primary blue action; use cancel as destructive secondary | `Cancel all` secondary/destructive |
| `EXPORT_COMPLETE` | Open output folder | `Open folder` |
| `EXPORT_PARTIAL_FAILURE` | Retry failed jobs | `Retry failed` |
| `EXPORT_FAILED` | Retry export or change destination | `Try again` |
| `SETTINGS_OPEN` | Save only if settings are not immediate-apply | `Save changes` |

Do not show two blue primary actions in one state.

## 4. Visibility matrix

| UI surface/element | DISCONNECTED | CONNECTING | CONNECTED_EMPTY | READY | EXPORTING | COMPLETE | PARTIAL/FAILED |
|---|---:|---:|---:|---:|---:|---:|---:|
| Top bar | yes | yes | yes | yes | yes | yes | yes |
| Account cluster | disconnected | connecting | connected | connected | connected | connected | connected |
| Token input in main workspace | yes | yes disabled | no | no | no | no | no |
| Conversation selector button | no or disabled | disabled | yes | yes | optional/limited | yes | yes |
| Selector drawer | overlay only | no | overlay | overlay | overlay only if safe | overlay | overlay |
| Export summary rows | no | no | no | yes | compact | optional summary | optional summary |
| Export button | no | no | no | yes | no | optional `Export again` secondary | optional |
| Activity tray | no | no | no | no | yes | optional/collapsed | yes |
| Completion summary | no | no | no | no | no | yes | yes |
| Settings | overlay/surface | overlay/surface if safe | overlay/surface | overlay/surface | restricted | overlay/surface | overlay/surface |
| Logs/diagnostics | hidden | hidden | hidden | hidden | details only | details only | details available |

## 5. Transition table

### Connection transitions

| From | Event | To | Notes |
|---|---|---|---|
| `DISCONNECTED` | user clicks `Connect` with valid-looking token | `CONNECTING` | Token field disabled while connecting. |
| `CONNECTING` | connection succeeds, no selection | `CONNECTED_EMPTY` | Show `Select conversations`. |
| `CONNECTING` | connection succeeds and persisted selection is valid | `READY_TO_EXPORT` | Only if selection persistence is implemented and validated. |
| `CONNECTING` | connection fails | `DISCONNECTED` | Show inline error and keep token field. |
| any connected state | user disconnects | `DISCONNECTED` | Clear active conversation data and selection unless explicitly preserving local drafts. |

### Selection transitions

| From | Event | To | Notes |
|---|---|---|---|
| `CONNECTED_EMPTY` | open selector | `CONNECTED_EMPTY + SELECTOR_OPEN` | Drawer opens, workspace remains stable. |
| `READY_TO_EXPORT` | `Change selection` | `READY_TO_EXPORT + SELECTOR_OPEN` | Preserve summary behind drawer. |
| `SELECTOR_OPEN` | user selects at least one target and clicks Done | `READY_TO_EXPORT` | Summary updates. |
| `SELECTOR_OPEN` | user clears all selection and clicks Done | `CONNECTED_EMPTY` | Show empty state. |
| `SELECTOR_OPEN` | user closes drawer with X/Esc | underlying state | Keep current selection. |

### Export transitions

| From | Event | To | Notes |
|---|---|---|---|
| `READY_TO_EXPORT` | user clicks Export and preflight passes | `EXPORTING` | Lock export settings for this run. |
| `READY_TO_EXPORT` | preflight fails | `READY_TO_EXPORT` | Show row-specific error. |
| `EXPORTING` | all jobs complete | `EXPORT_COMPLETE` | Show success state. |
| `EXPORTING` | some jobs fail/cancel and some complete | `EXPORT_PARTIAL_FAILURE` | Show retry/recovery. |
| `EXPORTING` | all jobs fail | `EXPORT_FAILED` | Show clear recovery actions. |
| `EXPORTING` | user cancels remaining jobs | `EXPORT_PARTIAL_FAILURE` or `EXPORT_FAILED` | Depends on completed jobs. Do not mark cancellation as app error. |

### Settings transitions

| From | Event | To | Notes |
|---|---|---|---|
| any state | user opens Settings | same state + `SETTINGS_OPEN` | Underlying workflow preserved. |
| `SETTINGS_OPEN` | user closes Settings | previous state | No selection loss. |
| `EXPORTING + SETTINGS_OPEN` | user tries destructive account action | blocked or confirm | Must explain effect on active exports. |

## 6. State-specific disabled rules

### Export disabled if

- no connection
- no selected targets
- no export format selected
- output destination is not writable
- an export is already running

If disabled, visible copy must explain why.

### Selector disabled if

- app is connecting
- conversations are not loaded
- opening it during export would corrupt active job state

If disabled during export, use tooltip/copy:

- `Selection can be changed after the current export finishes.`

If selection changes during export are safe, selection changes apply only to the next export, not the active run.

### Disconnect disabled/confirmed if

- export is running

Copy:

- `Disconnecting will stop active exports.`

## 7. Locked export run snapshot

When the user clicks Export, create a run snapshot. The export run must use this snapshot even if the user changes settings later.

Snapshot must include:

- selected targets
- output root
- export label
- date range
- format choices
- attachment setting
- TXT details settings
- run started timestamp

This prevents settings changes during export from mutating active jobs.

## 8. Error model

Errors must be represented as structured UI errors.

Recommended fields:

```python
@dataclass
class UiErrorViewModel:
    scope: Literal["connection", "destination", "export", "job", "settings"]
    title: str
    message: str
    suggested_action: str | None
    technical_details: str | None
```

Visible UI uses `title`, `message`, and `suggested_action`.

`technical_details` is hidden behind Details.

## 9. State restoration

On app start:

- restore theme
- restore output folder
- restore default export settings
- restore saved token if available
- do not automatically start export
- do not automatically open selector unless no selection and UX intentionally chooses to prompt selection after connection

If saved token exists and auto-connect is implemented later, show `Connecting...` clearly.

## 10. QA scenarios for state machine

Minimum scenarios:

1. Open app with no saved token: `DISCONNECTED`.
2. Enter invalid token: `CONNECTING` then `DISCONNECTED` with error.
3. Enter valid token: `CONNECTED_EMPTY`.
4. Open selector, select one DM, Done: `READY_TO_EXPORT`.
5. Change selection and clear all: `CONNECTED_EMPTY`.
6. Export one target successfully: `EXPORTING` then `EXPORT_COMPLETE`.
7. Export three targets with one failure: `EXPORTING` then `EXPORT_PARTIAL_FAILURE`.
8. Cancel before queued jobs start: completion state says stopped/partial, not generic failure.
9. Open settings during ready state, close: return to ready state unchanged.
10. Open settings during export, close: export continues and activity remains accurate.