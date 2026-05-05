# 02 — Main Workspace: Ready to Export

This file defines the main workspace when ArchiveCord is connected and the user has selected one or more conversations.

This state is the most important screen in the app. It must be calm, compact, and clear. It should communicate exactly what will happen if the user clicks `Export`.

## 1. State purpose

The ready workspace answers:

- which conversations are selected
- what format will be exported
- what date range is used
- where the export will be saved
- whether advanced settings are default or customized
- what the primary next action is

The ready workspace must not show:

- the full conversation tree by default
- the full logs table
- every advanced option expanded
- raw backend details
- a dashboard of past exports

## 2. Layout overview

Recommended layout:

```text
+--------------------------------------------------------------+
| Top bar                                                      |
+--------------------------------------------------------------+
|                                                              |
|  +--------------------------------------------------------+  |
|  | Ready to export                                      |  |
|  | Review your selection and export settings.            |  |
|  |                                                        |  |
|  | [Selected conversations row]                           |  |
|  | [Format row]                                           |  |
|  | [Date range row]                                       |  |
|  | [Destination row]                                      |  |
|  | [Advanced options row]                                 |  |
|  |                                                        |  |
|  |                                      [Export button]   |  |
|  +--------------------------------------------------------+  |
|                                                              |
+--------------------------------------------------------------+
```

The content should sit in the main workspace, centered vertically only if there is enough room. Do not create a giant empty hero area.

## 3. Workspace panel

### Panel position

- top offset from top bar: `24px`
- left/right margin: `24px`
- bottom margin: `24px`

### Panel width

- should fill available width with comfortable margins
- avoid a tiny centered card on large desktop windows
- avoid stretching text lines too wide; summary rows should preserve readable text blocks

### Panel style

- background: main surface
- border: `1px solid` border color
- radius: `12px`
- padding: `24px`
- no heavy shadow

If the app window itself already has a clean background and inner surfaces, the ready workspace may be borderless with rows inside a bordered summary container. The main requirement is clear hierarchy, not card count.

## 4. Header area

### Title

Text:

- `Ready to export`

Style:

- 24px
- weight 700
- primary text

### Subtitle

Text:

- `Review your selection and export settings.`

Style:

- 14px
- secondary text
- placed directly below title with 4–6px gap

### Optional icon

A small export/check icon may appear to the left of the title.

If used:

- icon well: 48px circle or rounded square
- background: primary blue soft
- icon color: primary blue
- do not make it oversized

If the UI feels cleaner without the icon, omit it.

## 5. Summary container

The summary container contains the rows that describe the export.

Style:

- background: main surface
- border: `1px solid` border color
- radius: `10–12px`
- rows separated by `1px solid` divider
- no individual card shadows

Rows:

1. Selected conversations
2. Format
3. Date range
4. Destination
5. Advanced options

Do not add more default rows unless absolutely necessary.

## 6. Summary row structure

Each row uses the same three-column structure:

```text
[icon] [label + value/description] [action/chevron]
```

### Row dimensions

- minimum height: `72px`
- horizontal padding: `16px`
- vertical padding: `12px`
- icon column width: `36–44px`
- action column width: enough for button/chevron

### Icon column

- icon size: `20px`
- icon color: neutral, or primary blue for important rows
- optional soft icon well: `36px x 36px`, radius 999px or 8px

Use the same icon treatment on every row. Do not mix random icon styles.

### Text column

Label:

- 14px
- semibold
- primary text

Value:

- 13px
- secondary text
- max two lines before truncation

### Action column

Use either:

- small secondary button: `Change`, `Edit`
- chevron for expandable row

Do not use both a button and a chevron in the same row unless the button performs a different action.

## 7. Row details

### 7.1 Selected conversations row

Label:

- `Selected conversations`

Value examples:

- `4 conversations`
- `Emma, Discord, Design Team > #announcements, Study Group > #general`

Action:

- `Change selection`

Button style:

- secondary button
- optional pencil/edit icon

Behavior:

- opens the conversation selector drawer

If selected items exceed available space:

- show first 2–4 names
- append `+ N more`
- full list available in tooltip or selector drawer

Do not show a large list of selected conversations by default.

### 7.2 Format row

Label:

- `Format`

Value examples:

- `TXT`
- `TXT + JSON`
- `HTML with attachments`
- `TXT · Attachments off`

Action:

- `Edit` button or chevron

Behavior:

- opens inline format editor, advanced drawer, or row expansion

Default for current app behavior:

- formatted TXT on
- JSON off unless user enabled
- attachments off unless user enabled

If attachments are enabled, say so plainly:

- `TXT with attachments`

### 7.3 Date range row

Label:

- `Date range`

Value examples:

- `All time`
- `Jan 1, 2026 → Feb 11, 2026`
- `After Jan 1, 2026`
- `Before Feb 11, 2026`

Action:

- `Edit` button or chevron

Behavior:

- opens compact date range editor

Do not show date picker controls by default.

### 7.4 Destination row

Label:

- `Destination`

Value:

- display resolved path, shortened only if necessary

Example:

- `C:\Users\Emma\Documents\ArchiveCord Exports`

Action:

- `Change...`

Behavior:

- opens folder picker

Path display:

- use monospace only if needed for clarity
- if path is long, middle-truncate visually but preserve full path in tooltip

### 7.5 Advanced options row

Label:

- `Advanced options`

Value:

- `File naming, message filters, attachment options, and more.`

Action:

- chevron right if collapsed
- chevron down if expanded

Default:

- collapsed

Behavior:

- expands advanced options below the row or opens an advanced drawer

See advanced option requirements in `00-design-system.md`.

## 8. Primary Export button

Position:

- bottom-right of workspace panel
- visually separated from summary rows by `24px`

Text:

- `Export`

Icon:

- export/share arrow icon allowed on left

Style:

- primary button
- height: `42–44px`
- min width: `136px`
- radius: `8px`

Enabled state:

- enabled only if connected, at least one exportable conversation selected, and destination is writable

Disabled state:

- if disabled, show why near the button or in status area

Examples:

- `Select at least one conversation.`
- `Choose a writable destination.`
- `Connect to Discord first.`

Do not silently disable without explanation.

## 9. Footer metadata

A compact footer may appear at the bottom of the workspace or window.

Allowed examples:

- `Last export: 2 days ago`
- `3 exports · 12,431 messages · 1.8 GB`

Footer text:

- 12px
- muted text

Do not show footer metadata if it creates clutter or inaccurate estimates.

## 10. Connected with no selection

If the user is connected but no conversations are selected, use the same workspace but with an empty state.

Title:

- `Choose conversations to export`

Body:

- `Select DMs or server channels to create an export.`

Primary action:

- `Select conversations`

Secondary action:

- none unless recent selection is implemented

Do not show the full summary container with empty rows.

## 11. Not connected state

If the user is not connected, do not show the ready export summary.

Title:

- `Connect to Discord`

Body:

- `Enter your Discord token to load DMs and server channels.`

Fields:

- token input
- remember token securely checkbox

Primary action:

- `Connect`

Security note:

- `Your token is stored locally and encrypted when remembered.`

Keep this compact. Do not create a marketing welcome page.

## 12. Advanced options expanded inside ready workspace

If advanced options are expanded inline, they must not overwhelm the page.

Layout:

- appears directly below the Advanced options row
- bordered continuation area
- 2-column grid on wide windows
- single column on narrow windows

Groups:

- Format
- Date range
- TXT details
- Destination

Do not show implementation details like worker names or export path internals.

## 13. Preview

Preview is optional in the ready state.

If shown:

- collapsed by default or below primary summary
- titled `Preview`
- show only short transcript sample
- use monospace
- do not exceed `140px` height by default

Preview must not compete with the Export button.

## 14. Error/preflight messages

Preflight issues appear near the relevant row and/or above the Export button.

Examples:

- Destination row: `ArchiveCord can't write to this folder.`
- Format row: `Choose at least one export format.`
- Connection: `Reconnect before exporting.`

Use calm language.

## 15. Forbidden patterns

Do not:

- keep the full DMs/server tree permanently visible next to this ready state by default
- show logs on this screen
- show all advanced settings expanded by default
- use multiple large cards for every piece of information
- add decorative hero artwork
- move the Export button around when rows expand/collapse
- make DMs/Servers top-level pages
- expose raw JSON/TXT filenames as headline content

## 16. Acceptance checklist

A correct ready workspace must satisfy:

- user can identify selected conversations within 3 seconds
- user can identify format, date range, and destination without opening settings
- user sees one obvious primary `Export` button
- user can change selection without losing the current summary
- advanced controls are available but not visible by default
- layout remains stable when selector drawer opens
- connection/account state is in the top-right account cluster
- no permanent logs/dashboard/table is visible in the default ready state