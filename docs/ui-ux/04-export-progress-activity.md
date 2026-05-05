# 04 — Export Progress and Activity

This file defines the export-in-progress state, the activity tray, per-job rows, cancellation behavior, and attachment preview expansion.

The activity UI must make the export feel trustworthy and alive without turning ArchiveCord into a dashboard.

## 1. State purpose

The export progress state answers:

- Is the export running?
- How far along is it?
- Which conversation is currently being exported?
- What step is happening now?
- Can I cancel?
- What has completed?
- Did anything fail?

It must not primarily show raw file artifacts, JSON/TXT internals, or developer logs.

## 2. Main workspace layout

When exporting, the main workspace stays in the same general position as the ready state.

Recommended structure:

```text
+--------------------------------------------------------------+
| Export in progress                                [Cancel all]|
| 2 of 3 exports active                                      |
|                                                              |
| [overall progress summary]                                  |
|                                                              |
| [selected conversations summary - compact]                   |
| [format/date/destination rows - compact or collapsed]         |
|                                                              |
| [Export activity tray expanded]                              |
+--------------------------------------------------------------+
```

Do not navigate away to a full page by default. Keep the activity connected to the export the user just started.

## 3. Header

Title:

- `Export in progress`

Subtitle examples:

- `2 of 3 exports running`
- `1 running · 1 queued · 1 complete`

Right side controls:

- `Cancel all` destructive secondary button
- optional chevron to collapse activity if activity tray is visible

Do not show `Pause all` unless true pause/resume exists in backend.

## 4. Overall progress summary

Show a compact summary above the activity tray.

Allowed elements:

- circular progress indicator or horizontal progress bar
- total progress percentage
- active count
- queued count
- completed count
- estimated total size if known
- elapsed time

Recommended concise layout:

```text
[progress ring 37%]  2 of 3 exports active     Messages 4,231 / 11,542     Attachments 128 / 342
```

If exact totals are unknown, do not fake precision. Use:

- `Fetching messages...`
- `Counting attachments...`
- `Size unknown until export completes`

## 5. Activity tray

The activity tray appears inside the main workspace.

### Collapsed state

Collapsed label:

- `Export activity`
- chip: `2 of 3 active`

Collapsed content:

- one-line overall status
- optional small progress bar
- chevron down

### Expanded state

Expanded tray contains job rows.

Style:

- background: main surface
- border: `1px solid` border color
- radius: `10–12px`
- divider between rows
- no heavy shadow

Header row:

```text
Export activity       2 of 3 active                                      [collapse chevron]
```

Footer row optional:

- `3 exports in total`
- `View completed exports` if a later history view exists

## 6. Job row structure

Each export job row uses this structure:

```text
[status icon/avatar] [conversation name + type] [current step + progress] [right metrics/actions]
```

### Row height

- compact: `64px`
- expanded/detail row: variable

### Left area

Contains:

- avatar/icon
- conversation name
- type/target subtitle

Example:

```text
Design Team > #announcements
Server channel
```

or:

```text
Emma
DM
```

### Middle area

Contains:

- status label
- current step detail
- progress bar if running

Example:

```text
Running
Saving attachments 128 of 342
[progress bar]
```

### Right area

Contains:

- percent if known
- action button
- expand chevron or overflow menu

Examples:

- `37%` + `Cancel`
- `Open folder`
- `Retry`
- overflow `...`

## 7. Job statuses

Use exact status language.

### Queued

Visual:

- gray or amber dot/chip
- no progress bar unless queue position is meaningful

Text:

- `Queued`
- `Waiting to start`

Allowed action:

- `Cancel`

### Running: fetching messages

Text:

- `Fetching messages`
- `18,942 of 42,517 messages` if count known

Progress:

- determinate if total known
- indeterminate/animated if unknown

### Running: formatting messages

Text:

- `Formatting messages`

Progress:

- optional percent if message count known

### Running: saving attachments

Text:

- `Saving attachments`
- `128 of 342`

Also show latest saved file if available:

- `Latest: IMG_2048.jpg`

### Running: writing files

Text:

- `Writing files`

This should usually be brief.

### Running: finalizing

Text:

- `Finalizing`

### Complete

Visual:

- green status icon/dot/chip

Text:

- `Complete`
- summary: `4,231 messages · 128 attachments`

Action:

- `Open folder`

### Failed

Visual:

- red status icon/dot/chip

Text:

- `Failed`
- short reason if known

Actions:

- `Retry`
- `Details`

### Cancelled

Visual:

- neutral/danger muted

Text:

- `Cancelled`

Actions:

- `Retry`
- `Remove from activity` optional

## 8. Progress bars

Progress bars must be calm and precise.

Style:

- height: `4–6px`
- track: divider/secondary surface
- fill: primary blue for running
- green for complete only if shown as complete bar
- red only for failed state indicators, not ordinary progress

Do not animate aggressively.

For unknown progress:

- use indeterminate subtle animation
- label must say what is happening

## 9. Cancel behavior

### Cancel job

Button text:

- `Cancel`

Behavior:

- cancels queued item immediately if not started
- requests cancellation for running item if backend supports it
- if current backend can only stop after current item finishes, text should be truthful

If cancellation is graceful and not instant:

- show `Cancelling...`

### Cancel all

Button text:

- `Cancel all`

Behavior:

- prevents queued jobs from starting
- requests cancellation of active job(s)

Do not show a confirmation dialog for ordinary cancel unless data loss risk is high. If confirmation is needed, use simple text:

`Stop remaining exports? Completed files will stay in the output folder.`

Buttons:

- `Keep exporting`
- `Stop exports`

## 10. Attachment previews

Attachment previews are optional richness. They must remain secondary.

### Default running row

When saving attachments, the job row may show:

- one small latest thumbnail if previewable
- filename of latest saved attachment
- count progress

Example:

```text
Saving attachments 128 of 342
Latest: IMG_2048.jpg
```

Thumbnail size:

- `40px x 40px` in row
- radius: `6px`
- object-fit crop or contain depending implementation

If the latest file is not previewable:

- show file icon instead of thumbnail

### Expanded job attachment preview

When the user expands a job row, show a section:

Title:

- `Recent attachments`

Subtitle/count:

- `Last 8 saved`

Content:

- horizontal strip or small grid of thumbnails
- max visible thumbnails: 8
- each thumbnail: `56–72px` square
- filename below or on hover/tooltip

Include link/button:

- `View all attachments (128)`

Only show this if attachments are enabled and files are being saved or have been saved.

### Thumbnail cache behavior

Implementation requirements:

- generate low-resolution thumbnails only
- do not load full-resolution images during export by default
- use lazy loading
- cap memory usage
- clear temporary thumbnails after export unless session cache setting is enabled
- previewable types only: common images first; video poster frames later if supported

Settings should include:

- `Show live attachment previews`
- `Cache thumbnails during export`
- `Clear preview cache after export`

Defaults:

- show live previews: on if performance is acceptable; off if backend cannot do it safely
- cache thumbnails: temporary/session only
- clear after export: on

## 11. Expanded job details

A job row may expand to show:

- recent attachment previews
- detailed progress counts
- current output folder
- skipped/failed attachment count
- View details button

Do not show raw logs unless user clicks `Details`.

Expanded detail area style:

- indented under row
- background: secondary surface or main surface
- top divider
- compact spacing

## 12. Failure details

If a job fails, show a short reason inline.

Examples:

- `Could not access channel.`
- `Output folder is not writable.`
- `12 attachments failed to download.`

Action:

- `Retry`
- `Details`

Details panel may show technical log excerpt, but not by default.

## 13. Activity history

The app may later support a full activity/history page. This is not required for the default progress state.

If implemented:

- open from `View activity`
- do not make it the default page after pressing Export
- keep current export progress visible in the main workspace

## 14. Relationship to current backend

Current batch behavior may be sequential rather than parallel. UI copy must match reality.

If only one export runs at a time:

- say `1 running · 2 queued`
- do not say `2 exports active`

If current in-flight item cannot be interrupted immediately:

- use `Cancel remaining` or `Stop after current item` instead of implying instant cancellation

Do not lie for visual polish.

## 15. Forbidden patterns

Do not:

- show a full raw table as the default progress UI
- show JSON/TXT file internals as primary progress content
- show all saved attachments as a giant gallery by default
- add pause buttons unless backend supports real pause/resume
- replace the whole app with an exports dashboard after the user clicks Export
- hide cancel/retry actions deep in menus only
- use bright flashing indicators
- use vague status labels when specific steps are known

## 16. Acceptance checklist

A correct export progress UI must satisfy:

- user knows export is running
- user knows which job is running and which are queued/complete
- user sees specific current step
- user can cancel the job or remaining batch truthfully
- completed jobs expose Open folder
- failed jobs expose Retry and Details
- attachment previews are available only as secondary detail
- raw logs and raw file internals are not primary content
- UI remains visually calm during progress updates