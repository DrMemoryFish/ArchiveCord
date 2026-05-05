# 09 — Component Contracts

This file defines the components needed for the ArchiveCord GUI redesign and the exact responsibilities of each component.

The goal is to prevent a new giant `MainWindow._build_ui()` that mixes state, styling, worker wiring, and layout in one place.

## 1. Component architecture rule

The final UI should be built from named components with clear responsibilities.

Do not implement the redesign as one long function that creates every widget directly.

Acceptable first pass:

- components may live in separate files under `app/ui/`
- components may be simple PySide `QWidget` subclasses
- shared styling may be QSS constants or helper functions

## 2. Required component list

Required or strongly recommended components:

| Component | Required | Purpose |
|---|---:|---|
| `TopBar` | yes | App identity, selector button, account cluster, settings access. |
| `AccountStatusCluster` | yes | Connection/account display and account menu. |
| `MainWorkspace` | yes | Owns workflow-state rendering below top bar. |
| `ConnectPanel` | yes | Token entry and first connection state. |
| `EmptySelectionPanel` | yes | Connected but no selected conversations. |
| `ExportSummaryPanel` | yes | Ready-to-export summary rows and Export action. |
| `SummaryRow` | yes | Reusable row for selected conversations, format, date, destination, advanced. |
| `ConversationSelectorDrawer` | yes | Temporary drawer for DMs/servers selection. |
| `ConversationTree` | yes | Tree/list widget for DMs/servers/channels. Can wrap current QTreeWidget logic. |
| `ActivityTray` | yes | Export activity header and job list. |
| `ActivityJobRow` | yes | One export job row with progress/actions/details. |
| `AttachmentPreviewStrip` | future/optional | Recent low-res thumbnails for expanded job rows. |
| `CompletionPanel` | yes | Export complete/partial/failure result state. |
| `SettingsView` | yes | Settings sections and content. |
| `DiagnosticsView` | yes | Logs/details moved out of primary workflow. |
| `Theme` / `StyleTokens` | yes | Central colors, spacing, typography, radius. |

## 3. View-model rule

Components should receive display-ready view models or simple values. They should not directly read random internal worker state.

Do not make visual components responsible for:

- Discord API calls
- export execution
- filesystem writes
- token storage
- log formatting internals

Components may emit signals/events upward.

## 4. TopBar contract

### Purpose

Global app shell header.

### Contains

- selector/menu button
- ArchiveCord icon
- ArchiveCord label
- spacer
- account status cluster
- settings button
- window controls if custom chrome exists

### Inputs

```python
@dataclass
class TopBarState:
    connection_state: str
    account_label: str | None
    account_avatar: QIcon | None
    selector_available: bool
    settings_available: bool
```

### Signals/events

- `selectorRequested`
- `settingsRequested`
- `accountMenuRequested`

### Must not

- contain token input after connection
- contain export settings
- contain logs
- center the connected badge randomly

## 5. AccountStatusCluster contract

### Purpose

Shows connection/account status in top-right.

### States

| State | Display |
|---|---|
| disconnected | gray dot + `Disconnected` |
| connecting | spinner + `Connecting` |
| connected | green dot + account label |
| failed | red dot + `Connection failed` |

### Optional menu actions

- Reconnect
- Disconnect
- Manage token
- Open settings

### Must not

- expose token value
- replace Settings view
- show long error details inline

## 6. MainWorkspace contract

### Purpose

Renders one workflow state at a time.

### Inputs

```python
@dataclass
class MainWorkspaceState:
    workflow_state: str
    selected_targets: list[ExportTargetViewModel]
    export_options: ExportOptionsViewModel
    export_jobs: list[ExportJobViewModel]
    last_result: ExportRunResultViewModel | None
    error: UiErrorViewModel | None
```

### Child panels by state

| Workflow state | Child panel |
|---|---|
| `DISCONNECTED` | `ConnectPanel` |
| `CONNECTING` | `ConnectPanel` with disabled input/loading |
| `CONNECTED_EMPTY` | `EmptySelectionPanel` |
| `READY_TO_EXPORT` | `ExportSummaryPanel` |
| `EXPORTING` | `ExportSummaryPanel` compact + `ActivityTray` |
| `EXPORT_COMPLETE` | `CompletionPanel` success |
| `EXPORT_PARTIAL_FAILURE` | `CompletionPanel` partial |
| `EXPORT_FAILED` | `CompletionPanel` failed |

### Must not

- directly build the conversation tree
- directly store token
- directly run export workers

## 7. ConnectPanel contract

### Purpose

First-connect and disconnected state.

### Contains

- title: `Connect to Discord`
- short explanation
- token input
- reveal/hide token button
- `Remember token securely`
- primary `Connect` button
- inline error if connection fails
- security note

### Signals

- `connectRequested(token, remember)`

### Must not

- be a giant welcome/marketing page
- show conversations/export controls before connection

## 8. EmptySelectionPanel contract

### Purpose

Connected state with no selected targets.

### Contains

- title: `Choose conversations to export`
- body: `Select DMs or server channels to create an export.`
- primary button: `Select conversations`

### Signals

- `selectorRequested`

### Must not

- show empty export summary rows
- show logs or advanced options

## 9. ExportSummaryPanel contract

### Purpose

Shows export-ready summary and starts export.

### Contains

- title: `Ready to export`
- subtitle
- summary container with `SummaryRow`s
- optional preview collapsed/secondary
- primary `Export` button

### Inputs

```python
@dataclass
class ExportSummaryViewModel:
    selected_summary: str
    selected_count: int
    format_summary: str
    date_range_summary: str
    destination_path: str
    advanced_summary: str
    export_enabled: bool
    export_disabled_reason: str | None
```

### Signals

- `changeSelectionRequested`
- `formatEditRequested`
- `dateRangeEditRequested`
- `destinationChangeRequested`
- `advancedOptionsRequested`
- `exportRequested`

### Must not

- contain full DMs/server tree
- show all advanced options expanded by default
- start export without preflight validation

## 10. SummaryRow contract

### Purpose

Reusable row in export summary.

### Inputs

```python
@dataclass
class SummaryRowModel:
    icon_name: str
    title: str
    value: str
    secondary_value: str | None
    action_label: str | None
    expandable: bool
    expanded: bool
    disabled: bool
    error: str | None
```

### Layout

```text
[icon] [title + value + optional error] [action or chevron]
```

### Must support

- hover state
- focus state
- disabled state
- inline row error
- tooltip for truncated value

## 11. ConversationSelectorDrawer contract

### Purpose

Temporary selection surface.

### Contains

- header with title and close button
- search input
- All/DMs/Servers segmented filter
- `ConversationTree`
- pinned footer with selected count, clear selection, Done

### Inputs

```python
@dataclass
class ConversationSelectorState:
    is_open: bool
    filter_mode: Literal["all", "dms", "servers"]
    search_query: str
    tree_items: list[ConversationTreeItemViewModel]
    selected_count: int
    loading: bool
    error: UiErrorViewModel | None
```

### Signals

- `closed`
- `doneRequested`
- `searchChanged(query)`
- `filterChanged(mode)`
- `selectionChanged(target_ids)`
- `clearSelectionRequested`

### Must not

- clear selection when search/filter changes
- permanently resize workspace
- show inline IDs by default

## 12. ConversationTree contract

### Purpose

Display DMs, servers, categories, and channels.

### Row model

```python
@dataclass
class ConversationTreeItemViewModel:
    id: str
    kind: Literal["section", "dm", "server", "category", "channel"]
    label: str
    subtitle: str | None
    icon: QIcon | None
    checked_state: Literal["unchecked", "checked", "partial"]
    disabled: bool
    disabled_reason: str | None
    children: list[ConversationTreeItemViewModel]
```

### Must support

- checkboxes
- partial parent state
- expand/collapse
- keyboard navigation
- disabled rows
- tooltips for IDs only when enabled

## 13. ActivityTray contract

### Purpose

Show active/recent export jobs without becoming a dashboard.

### Contains

- header: `Export activity` + active count chip + collapse chevron
- list of `ActivityJobRow`s
- optional footer count

### Inputs

```python
@dataclass
class ActivityTrayState:
    expanded: bool
    jobs: list[ExportJobViewModel]
    active_count: int
    queued_count: int
    completed_count: int
    failed_count: int
```

### Signals

- `collapseToggled`
- `cancelAllRequested`
- `cancelJobRequested(job_id)`
- `retryJobRequested(job_id)`
- `openFolderRequested(job_id)`
- `jobDetailsRequested(job_id)`

### Must not

- show raw logs by default
- show a giant attachment gallery by default

## 14. ActivityJobRow contract

### Purpose

One export job status row.

### Row model

```python
@dataclass
class ExportJobViewModel:
    job_id: str
    target_label: str
    target_type: str
    status: Literal["queued", "fetching", "formatting", "saving_attachments", "writing_files", "finalizing", "complete", "failed", "cancelled"]
    status_label: str
    detail: str
    progress_percent: int | None
    messages_done: int | None
    messages_total: int | None
    attachments_done: int | None
    attachments_total: int | None
    latest_attachment: AttachmentPreviewItem | None
    output_folder: str | None
    error_message: str | None
    expanded: bool
```

### Must support

- cancel for queued/running where backend supports it
- retry for failed/cancelled
- open folder for complete
- details expansion
- latest attachment preview if available

## 15. AttachmentPreviewStrip contract

### Purpose

Expanded job detail showing recent saved attachments.

### Item model

```python
@dataclass
class AttachmentPreviewItem:
    attachment_id: str
    filename: str
    file_path: str | None
    thumbnail_path: str | None
    mime_type: str | None
    size_bytes: int | None
    previewable: bool
    status: Literal["saving", "saved", "failed", "skipped"]
```

### Rules

- max visible items: 8
- low-res thumbnails only
- no blocking UI thread
- full-res only after explicit user action

## 16. CompletionPanel contract

### Purpose

Show final export result.

### Inputs

```python
@dataclass
class ExportRunResultViewModel:
    result_state: Literal["success", "partial_failure", "failed", "cancelled"]
    title: str
    subtitle: str
    stats: ExportRunStatsViewModel
    rows: list[ExportResultRowViewModel]
    output_root: str | None
```

### Row model

```python
@dataclass
class ExportResultRowViewModel:
    target_label: str
    target_type: str
    status: Literal["complete", "failed", "cancelled"]
    message_count: int | None
    attachment_count: int | None
    size_bytes: int | None
    output_folder: str | None
    error_message: str | None
```

### Signals

- `openFolderRequested`
- `reviewFilesRequested`
- `exportAgainRequested`
- `retryFailedRequested`
- `detailsRequested`

## 17. SettingsView contract

### Purpose

Account, appearance, defaults, activity/previews, diagnostics.

### Sections

- Account
- Appearance
- Export defaults
- Activity & previews
- Diagnostics
- About

### Signals

- `closeRequested`
- `reconnectRequested`
- `disconnectRequested`
- `tokenUpdateRequested`
- `themeChanged`
- `exportDefaultsChanged`
- `diagnosticsRequested`

### Must not

- clear workflow state when opened/closed
- expose token in diagnostics

## 18. DiagnosticsView contract

### Purpose

Houses existing logs UI and technical details.

Can reuse current `LogTab` behavior, but it must live under Settings > Diagnostics or export Details, not primary tabs.

### Contains

- level filter
- search
- auto-scroll
- copy selected
- clear logs
- log table

## 19. Event ownership

Workers and backend events should be translated into view models before hitting components.

Example:

```text
BatchExportWorker progress signal
  -> controller updates ExportJobViewModel
  -> ActivityTray re-renders affected row
```

Do not wire worker signals directly into random labels in many widgets.

## 20. Acceptance checklist

A correct component implementation must satisfy:

- each major surface has a named component
- `MainWindow` coordinates state but does not own every widget detail
- styling tokens are centralized
- worker state is transformed into view models
- components emit actions upward instead of running backend work themselves
- components can be tested independently where practical