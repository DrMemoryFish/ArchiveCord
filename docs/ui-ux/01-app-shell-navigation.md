# 01 — App Shell and Navigation

This file defines the global app shell used by every ArchiveCord UI state.

## 1. Purpose

The shell must make ArchiveCord feel like one focused desktop workspace, not a collection of unrelated pages.

The shell must provide:

- app identity
- connection/account status
- access to settings
- access to conversation selection
- stable space for the main workspace
- predictable window controls

The shell must not overload the user with permanent navigation or multiple dashboards.

## 2. Window structure

Use a desktop application frame with this structure:

```text
+--------------------------------------------------------------+
| Top bar                                                      |
+--------------------------------------------------------------+
|                                                              |
| Main workspace                                               |
|                                                              |
+--------------------------------------------------------------+
```

When the conversation selector is open:

```text
+--------------------------------------------------------------+
| Top bar                                                      |
+--------------------------------------------------------------+
| Selector drawer overlays left side | Main workspace behind   |
+--------------------------------------------------------------+
```

The selector drawer overlays the workspace. It must not permanently shove the workspace into a new layout.

## 3. Top bar

### Height

Recommended height: `56px`.

Acceptable range: `52–60px`.

### Padding

- left/right padding: `16px`
- internal control gap: `12px`
- group gap: `20–24px`

### Top bar layout

```text
[menu/selector button] [ArchiveCord icon] [ArchiveCord]       [connection dot] [account] [settings] [window controls]
```

The top bar should feel compact and quiet.

## 4. Left top-bar group

### Selector button

Position: far left, before the app icon.

Use a small icon button.

Icon:

- hamburger/menu icon, sidebar icon, or compact conversation-list icon

Accessible label:

- `Open conversation selector`

Behavior:

- Opens the selector drawer.
- If the selector drawer is already open, it closes the drawer.

Style:

- size: `32px x 32px`
- icon size: `18px`
- no filled background by default
- hover background: secondary surface
- focus ring: primary blue

### App icon

Use a small ArchiveCord icon.

Recommended visual:

- archive box / folder / export container
- blue accent
- simple shape

Size:

- `24px x 24px`

### App name

Text:

- `ArchiveCord`

Style:

- 16px
- semibold
- primary text color

Do not add a subtitle in the top bar.

## 5. Right top-bar group

The connected state belongs in the account cluster, not floating in the center.

### Connection dot

Position:

- immediately before or inside the account cluster

States:

- Connected: green dot + `Connected`
- Connecting: small spinner + `Connecting`
- Disconnected: gray dot + `Disconnected`
- Failed: red dot + `Connection failed`

Default connected display:

```text
● Connected    emma#1234    Settings
```

If horizontal space is limited:

```text
● emma#1234    Settings
```

Connection status still needs tooltip text:

- `Connected to Discord as emma#1234`

### Account display

Show:

- small avatar or generic account circle
- username/discriminator where available
- optional chevron for account menu

Example:

- `emma#1234 ▾`

Account menu may contain:

- Reconnect
- Disconnect
- Manage token
- Open settings

### Settings button

Position:

- right side, near account cluster
- before window controls

Label:

- `Settings`

Icon:

- gear

Behavior:

- Opens Settings surface.
- Settings may be a modal-like full workspace view or a right-side/center panel. See `06-settings.md`.

Do not place settings as a large permanent sidebar item in the main workflow.

## 6. Window controls

Use platform window controls where available.

If custom chrome is used:

- minimize
- maximize/restore
- close

Keep these visually separate from app actions.

## 7. Main workspace

The main workspace is the default visible area below the top bar.

Recommended margins:

- outer margin: `24px`
- max content width: not required on desktop, but keep content readable
- do not stretch summary rows to absurd width if the window is very large

Workspace states:

- Not connected
- Connected with no selection
- Ready to export
- Export in progress
- Export complete
- Export finished with issues

The main workspace must not be replaced by separate top-level pages for DMs, Servers, Logs, or Activity by default.

## 8. Navigation model

Do not use a permanent multi-item sidebar as the primary navigation for the core task.

Allowed global navigation:

- selector drawer button
- account/settings access
- activity tray within workspace

Not allowed as default top-level nav:

- Conversations
- Search
- Exports
- Servers
- Settings
- Diagnostics
- Logs

Those make the app feel broader and heavier than the task.

If future versions add a full activity/history page, it must be secondary and opened from `View activity`, not permanently shown as a top-level destination.

## 9. Selector drawer behavior

The selector drawer is described fully in `03-conversation-selector-drawer.md`.

Global behavior requirements:

- opens from the left
- overlays the workspace
- does not resize the main workspace permanently
- closes with Done, X, Esc, or selector button
- preserves current selection
- must have focus trapping while open if modal overlay behavior is used

When open, the workspace behind may be dimmed slightly:

- light mode overlay: `rgba(17, 24, 39, 0.18)` maximum
- dark mode overlay: `rgba(0, 0, 0, 0.35)` maximum

Do not blur the main workspace heavily.

## 10. Settings behavior

Settings should open as a secondary surface.

Acceptable implementations:

1. Full main-workspace settings view with left settings section list.
2. Centered settings panel overlay.
3. Right-side settings panel.

Recommended for first implementation:

- full main-workspace settings view, because it is easiest in PySide and avoids complex overlay behavior
- retain the top bar
- provide a clear back/close affordance if settings replaces the main workflow view

Settings must not permanently add a second navigation sidebar to the main export flow.

## 11. Activity behavior

Activity is not a primary page by default.

Activity appears as:

- compact tray inside export progress state
- optional expanded tray
- optional `View activity` action for a later full history view

Do not implement a dashboard-style exports page as the default experience.

## 12. Stable-layout rule

The app must avoid constant layout shifts.

Opening the selector drawer should not cause:

- export rows to reflow significantly
- Export button to jump
- progress tray to move horizontally
- summary text to wrap differently if avoidable

Use overlay/drawer behavior to preserve the workspace layout.

## 13. Keyboard behavior

Global shortcuts:

- `Esc`: close drawer, preview panel, settings overlay, or details panel where safe
- `Ctrl+F`: focus conversation search if selector is open; otherwise open selector and focus search
- `Ctrl+,`: open settings if platform convention is acceptable
- `Ctrl+E`: trigger Export only if ready and focus is not inside a text field

Do not require shortcuts for normal use.

## 14. Implementation notes for current PySide app

Current code uses:

- permanent left conversation tree
- right tab widget for Export and Logs
- token input in top bar

The target shell should evolve toward:

- top bar with account cluster instead of permanent token input
- main workspace instead of tabbed Export/Logs primary view
- selector drawer instead of always-visible tree
- logs moved into diagnostics/details

This can be implemented incrementally, but the final UX must follow this spec.