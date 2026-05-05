# 07 — Implementation Guardrails

This file defines strict boundaries for implementing the ArchiveCord UI/UX redesign.

A literal implementer must follow these rules. If a requirement is not explicitly described in the UI/UX docs, do not invent a large new pattern. Use the closest existing pattern from these docs.

## 1. Non-negotiable product rules

1. ArchiveCord is a desktop utility, not a website.
2. The main task is: connect, select conversations, export, monitor result.
3. The main workspace is the center of the product.
4. Conversation selection belongs in a drawer/temporary selector surface, not a permanent default panel during export.
5. Advanced options are hidden by default.
6. Activity is integrated as a tray/state, not a default dashboard page.
7. Logs are diagnostics, not a primary tab.
8. Token management belongs in first-connect state and Settings, not permanently in the top bar.
9. The top-right account cluster owns connection status.
10. Every state has one clear primary action.

## 2. Forbidden UI patterns

Do not implement:

- a permanent large left DMs/Servers tree beside every state
- a SaaS-style dashboard with many cards for the core workflow
- a forced multi-step wizard with Next/Back for normal exporting
- a separate top-level DMs page
- a separate top-level Servers page
- a separate top-level Logs tab as default user experience
- decorative hero sections
- large empty welcome pages
- confetti or celebratory animation
- fake pause/resume controls
- always-expanded advanced options
- raw JSON/TXT/metadata file lists as the main export result
- inline Discord IDs in normal row labels
- stack traces in normal UI
- multiple equally prominent primary buttons

## 3. Required state model

Implement the UI as states of one workflow.

Required states:

1. Not connected
2. Connected with no selection
3. Ready to export
4. Selector drawer open
5. Export in progress
6. Export complete
7. Export finished with issues
8. Settings open

Do not treat these as unrelated pages with different design systems.

## 4. Current-code migration guidance

Current UI characteristics:

- top token field
- remember token checkbox in top bar
- permanent conversation tree on left
- right-side Export tab
- Logs tab
- progress bars inside execute group
- output preview text area

Target migration:

- move token field to not-connected state and Settings > Account
- replace permanent tree with selector drawer
- replace Export tab form with main workspace summary
- replace Logs tab with Settings > Diagnostics / failure details
- replace batch progress group with activity tray
- preserve backend export behavior unless explicitly changing backend

## 5. PySide layout guidance

### Recommended widget structure

A possible PySide structure:

```text
MainWindow
  RootWidget
    TopBarWidget
    WorkspaceStack or WorkspaceContainer
    ConversationSelectorDrawer overlay/widget
```

The exact class names are not mandatory, but the separation of responsibilities is mandatory.

### Recommended components

Create or refactor toward reusable components:

- `TopBar`
- `AccountStatusCluster`
- `MainWorkspace`
- `ExportSummaryPanel`
- `SummaryRow`
- `ConversationSelectorDrawer`
- `ConversationTreeView`
- `ActivityTray`
- `ActivityJobRow`
- `SettingsView`
- `DiagnosticsView`

Do not keep all UI construction inside one giant `_build_ui()` function long-term.

## 6. Styling implementation guidance

Centralize styling tokens.

Allowed approaches:

- QSS stylesheet constants
- Python constants for colors, spacing, and dimensions
- theme object/helper module

Avoid:

- hardcoding random hex values inside many widgets
- slightly different blues for similar states
- one-off margins on every layout
- mixing dark/light colors manually everywhere

## 7. Naming rules

Use user-facing language consistently.

Use:

- `Export`
- `Ready to export`
- `Export in progress`
- `Export complete`
- `Export finished with issues`
- `Selected conversations`
- `Change selection`
- `Date range`
- `Destination`
- `Advanced options`
- `Activity`
- `Diagnostics`

Avoid:

- `Process`
- `Batch worker`
- `Pipeline`
- `Payload`
- `Internal export structure`
- `UserRole data`
- `Raw target`
- implementation terms in visible UI

Exception: developer diagnostics/logs may include implementation terms after user clicks Details.

## 8. Button rules

### Primary action per state

Not connected:

- `Connect`

Connected/no selection:

- `Select conversations`

Ready:

- `Export`

Exporting:

- no primary export button; use `Cancel all` as destructive secondary

Complete:

- `Open folder`

Finished with issues:

- `Retry failed`

Settings:

- `Save changes` only if settings use explicit save

Do not show two blue primary buttons in one state unless one is inside an isolated modal/drawer footer.

## 9. Drawer rules

The selector drawer:

- opens from left
- overlays workspace
- width 360–440px
- has title, search, filters, tree, footer
- closes without losing selection
- must not push the main workspace around as default behavior

If implementing overlay is hard in PySide, a temporary side panel may be acceptable only if:

- workspace movement is minimal
- animation is subtle
- the app preserves layout stability
- the final target remains overlay/drawer behavior

## 10. Activity rules

Activity tray:

- appears during export
- shows per-job progress
- has clear statuses
- supports cancel/retry/open folder where backend supports it
- shows attachment previews only as optional expanded detail

Do not implement a full activity dashboard as the first/default export progress state.

## 11. Attachment preview rules

If implementing previews:

- use low-res thumbnails
- cap memory usage
- lazy-load previews
- only show recent thumbnails
- clear temporary cache after export by default
- never block export progress for thumbnail generation
- never load full-resolution image automatically during export

If thumbnail generation is not safe/performance-ready, implement the UI placeholder but keep previews disabled behind Settings.

## 12. Logs/diagnostics rules

Normal users see plain statuses.

Diagnostics view may show:

- logs table
- level filter
- search
- copy selected
- clear logs

But logs must not be a default primary tab.

Failures should show:

- short reason
- suggested fix
- Details expander for technical log

## 13. Accessibility requirements

Do not ship UI without:

- visible focus states
- keyboard selection in tree
- keyboard access to drawer controls
- Esc close behavior
- labels/tooltips for icon-only buttons
- status text alongside status color
- disabled controls explaining why where relevant

## 14. Visual acceptance checklist

Before considering UI work done, verify:

- no permanent DMs/Servers tree visible in ready/exporting/complete states unless selector drawer is open
- top bar connection state is grouped with account
- Settings is reachable but not visually dominant
- ready state has only the essential summary rows
- Export button is the single dominant action in ready state
- advanced options are collapsed
- activity tray appears during export and is not a standalone dashboard by default
- completion state emphasizes outcome and Open folder
- dark mode uses same layout as light mode
- colors match `00-design-system.md`
- typography and spacing use the defined scale

## 15. Functional acceptance checklist

Verify:

- user can connect
- user can open selector
- user can search/filter All/DMs/Servers
- user can select multiple conversations
- selected count updates
- user can close selector and see selection summary
- user can edit format/date/destination
- user can export
- progress appears with per-job statuses
- user can cancel supported jobs
- completion shows success/failure clearly
- user can open output folder
- settings preserve workflow state

## 16. Documentation rule

If implementation intentionally deviates from these docs, the developer must update the relevant doc in the same PR/commit and explain why.

Do not silently diverge from the spec.