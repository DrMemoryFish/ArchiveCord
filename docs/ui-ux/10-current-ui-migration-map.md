# 10 — Current UI Migration Map

This file maps the current ArchiveCord PySide UI to the target UI/UX architecture.

The purpose is to prevent implementation from ripping out working logic or duplicating behavior under new names.

## 1. Current UI summary

Current UI is mostly built in `app/ui/main_window.py`.

Current visible structure:

```text
Top token bar
  token input
  remember token checkbox
  connect button
  status dot/label

Main splitter
  Left panel
    search conversations
    tooltip/settings gear
    permanent DMs/server tree
    selected count

  Right panel
    tabs
      Export tab
        Date Range group
        Output Format group
        Destination group
        Execute group
        Output Preview
      Logs tab
        level filter
        search
        auto-scroll
        copy
        clear
        log table
```

This works functionally, but it exposes too much machinery at once.

## 2. Target UI summary

Target visible structure:

```text
Top bar
  selector button
  ArchiveCord identity
  account/connection cluster
  settings button

Main workspace
  disconnected/connect panel OR
  empty selection panel OR
  ready export summary OR
  export progress + activity tray OR
  completion state OR
  settings surface

Temporary surfaces
  conversation selector drawer
  advanced options expander/drawer
  diagnostics/logs details
```

## 3. Migration table

| Current item | Current location | Target location | Action |
|---|---|---|---|
| `token_input` | top bar | `ConnectPanel` and `Settings > Account` | Move. Do not keep permanent after connected. |
| `remember_token` | top bar | `ConnectPanel` and `Settings > Account` | Move. Preserve keyring behavior. |
| `connect_button` | top bar | `ConnectPanel`; reconnect in account/settings | Move primary connect action into disconnected state. |
| `status_dot` | top bar | `AccountStatusCluster` | Keep concept, move into account cluster. |
| `status_label` | top bar | `AccountStatusCluster` and status bar messages | Keep but place with account. |
| `search_input` | left panel | `ConversationSelectorDrawer` | Move. Preserve filtering behavior. |
| `search_settings_button` | left panel | selector drawer options or Settings | Keep ID tooltip preference but do not make visually dominant. |
| `tree` | permanent left panel | `ConversationSelectorDrawer > ConversationTree` | Move. Preserve selection logic, icons, keyboard behavior. |
| `selection_count_label` | left panel | selector drawer footer and ready summary | Keep count, show in proper context. |
| `tabs` | right panel | remove as primary navigation | Replace with workspace state switching. |
| Export tab | right tab | `ExportSummaryPanel` / `MainWorkspace` | Replace form-first UI with summary-first UI. |
| Logs tab | right tab | `Settings > Diagnostics` / failure details | Move. Reuse `LogTab` internals if useful. |
| `date_group` | Export tab | summary row + advanced date editor | Hide by default behind Date range row. |
| `options_group` | Export tab | summary row + advanced format editor | Hide detailed controls by default. |
| `txt_format_section` | Export tab | advanced options | Keep behavior, move deeper. |
| `output_group` | Export tab | Destination summary row + Settings default | Keep folder picker. |
| `base_filename_input` | Export tab | Advanced options > File/package naming | Rename visible copy to `Export label`. |
| `open_folder_toggle` | Export tab | Advanced options + Settings default | Keep preference. |
| `execute_group` | Export tab | ExportSummaryPanel + ActivityTray | Replace with state-specific actions. |
| `progress` | Execute group | `ActivityJobRow` current job progress | Remap. |
| `batch_progress` | Execute group | `ActivityTray` batch progress | Remap. |
| `batch_progress_label` | Execute group | Activity header/subtitle | Remap. |
| `cancel_button` | Execute group | `Cancel all` or `Cancel remaining` in activity | Rename truthfully based on backend. |
| `preview` | Export tab | optional collapsed Preview / Review files | Keep secondary. Do not dominate ready state. |
| `LogTab` | `app/ui/log_tab.py` | `DiagnosticsView` | Reuse, but move out of primary tabs. |

## 4. Existing behavior to preserve

Preserve these unless a later implementation doc explicitly changes them:

- token validation behavior
- keyring token persistence behavior
- output folder persistence behavior
- open folder after export preference
- DMs/server/category/channel tree construction
- icon cache behavior
- selection deduplication by stable ID
- keyboard tree behavior: Space toggles, Enter expands/collapses
- date before/after filtering semantics
- TXT/JSON/attachments export options
- edited/pinned/reply formatting options
- batch export continuing after failed items
- batch cancellation semantics if current backend only stops queueing new items
- export path architecture from `app/core/export_paths.py`

## 5. Existing behavior to change intentionally

Change these deliberately:

| Behavior | Current | Target |
|---|---|---|
| Token visibility | always top bar | only disconnected state/settings/account menu |
| Conversation tree | permanent left panel | selector drawer/temporary surface |
| Export options | many groups visible | summary rows by default, details on demand |
| Logs | main tab | diagnostics/details only |
| Progress | generic progress bars | activity tray with per-job rows |
| Connected status | separate/floating top label | account cluster top-right |
| Preview | large default text area | optional collapsed/secondary preview |
| Main UI model | splitter + tabs | stateful main workspace |

## 6. Methods likely affected in `main_window.py`

Exact names may change, but these current areas need migration attention:

- `_build_ui()`
- `_load_saved_token()`
- `_configure_token_persistence()`
- `set_connection_status()`
- `update_filter_controls()`
- `_update_txt_format_controls()`
- `browse_output_dir()`
- `on_output_dir_edited()`
- tree item helpers and selection sync methods
- `on_connect()`
- `on_conversations_loaded()`
- `on_export()`
- `on_cancel_batch()`
- export worker signal handlers
- preview update handlers

Do not delete these blindly. Refactor behavior into components/controllers.

## 7. Suggested new files

Recommended new UI files:

```text
app/ui/theme.py
app/ui/top_bar.py
app/ui/main_workspace.py
app/ui/export_summary_panel.py
app/ui/summary_row.py
app/ui/conversation_selector_drawer.py
app/ui/conversation_tree.py
app/ui/activity_tray.py
app/ui/activity_job_row.py
app/ui/completion_panel.py
app/ui/settings_view.py
app/ui/diagnostics_view.py
app/ui/view_models.py
```

This list is not mandatory, but equivalent separation is mandatory.

## 8. Migration constraints

### Do not break backend exports

The UI refactor must not change:

- `ExportOptions` semantics
- export path builder behavior
- exporter output package layout
- worker threading safety

### Do not remove tests

Existing export-path and export-pipeline tests must continue passing.

### Do not introduce UI thread blocking

Icon loading, export progress, and future thumbnails must not block the Qt UI thread.

### Do not fake backend features

If backend does not support true per-job pause, do not show Pause.

If backend does not support live per-attachment events, do not show detailed live thumbnails as if it does.

## 9. Worker event mapping needed for activity tray

Current progress signals may not contain enough detail for the final activity UI.

Minimum required activity data:

- job id / target id
- target label
- target type
- current step label
- progress percent if known
- message count if known
- attachment count if known
- output folder when complete
- error reason when failed

If current workers do not emit this, add adapter/controller state first.

Do not let every worker signal directly mutate random labels.

## 10. Migration-risk notes

High risk areas:

- moving tree selection logic into a drawer without breaking tri-state behavior
- preserving keyboard controls after moving tree
- replacing tabs without losing logs functionality
- ensuring export cancellation copy matches backend behavior
- not accidentally clearing selection when settings/selector opens
- handling settings changes during active export

## 11. Manual before/after comparison

Before migration is accepted, verify:

| User task | Current behavior | Target behavior |
|---|---|---|
| Connect | paste token top bar | connect panel or saved account cluster |
| Select DM | check item in permanent tree | open selector drawer, check DM, Done |
| Select server channel | expand tree permanently | open selector drawer, filter Servers, check channel, Done |
| Change output folder | Destination group | Destination summary row Change button |
| Enable JSON | Output Format group | Format row edit/advanced options |
| Start export | Export & Process button | Export button |
| Watch batch | progress bars + preview/logs | activity tray with per-job rows |
| Open logs | Logs tab | Settings > Diagnostics or Details |
| Finish export | progress completes | completion panel with Open folder |

## 12. Acceptance checklist

Migration is acceptable only if:

- all old essential functionality still exists somewhere
- old technical controls are moved deeper, not deleted accidentally
- visible default workflow is simpler than current UI
- main workspace no longer uses tab-first Export/Logs navigation
- conversation tree is not permanently visible in ready/progress/complete states
- token field is not permanently visible once connected
- existing backend tests pass
- new UI state/component tests or manual QA checklist exist