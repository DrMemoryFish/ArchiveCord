# 05 — Export Complete and Finished-with-Issues States

This file defines the completion state shown after one or more exports finish.

The completion state must make the result obvious and give the user useful next actions without dumping technical file internals on them.

## 1. State purpose

The completion state answers:

- Did the export finish?
- Did all selected conversations succeed?
- Where are the files?
- What was exported?
- What can I do next?
- If something failed, how do I recover?

It must not overwhelm the user with raw logs or internal filenames by default.

## 2. Completion variants

There are three completion variants:

1. All successful
2. Completed with issues
3. Cancelled/stopped with partial results

Use different titles and status treatments for each.

## 3. All-successful state

### Header

Title:

- `Export complete`

Subtitle:

- `3 exports finished successfully`

Icon:

- success checkmark
- green circle or soft green icon well

Style:

- icon size: `40–48px`
- green: `#18A957`
- icon background: `#E8F8EF`

### Primary actions

Use these actions in priority order:

1. `Open folder`
2. `Review files`
3. `Export again`
4. `View activity`

Only one should be primary.

Recommended primary:

- `Open folder`

Secondary buttons:

- `Review files`
- `Export again`
- `View activity`

Do not make all actions equally visually loud.

## 4. Summary stats

Show compact stats if available:

- exports count
- messages count
- attachments count
- total size

Example:

```text
3 exports     12,431 messages     342 attachments     1.8 GB
```

Style:

- single horizontal summary row or compact stat group
- no large dashboard cards unless the app window has enough space and they remain restrained
- labels use caption text
- numbers use 18–20px semibold

Do not show meaningless estimates. If total size is unknown, omit it.

## 5. Completed exports list

Show a compact list/table of completed export targets.

Columns/fields:

- conversation name
- target type
- messages
- attachments
- size
- status
- action

Example row:

```text
Emma                         DM              2,341 messages   68 attachments   285 MB   Complete   Open
Design Team > #announcements Server channel  6,342 messages   221 attachments  1.1 GB   Complete   Open
Study Group > #general       Server channel  3,748 messages   53 attachments   420 MB   Complete   Open
```

Do not show `messages.txt`, `metadata.json`, or `attachments/` as the main row labels.

Those file artifacts may appear only when a row is expanded.

## 6. Row expansion after completion

A completed row may expand to show:

- export folder path
- artifact list
- attachment count
- recent attachments preview if enabled
- open folder
- reveal transcript

Artifact list wording:

- `Messages transcript`
- `Raw JSON data` if enabled
- `Metadata`
- `Attachments folder`

Only show actual filenames in secondary text:

- `messages.txt`
- `messages.json`
- `metadata.json`
- `attachments/`

## 7. Folder/path display

Show the main output location near the bottom or under the completed list.

Text:

- `Files exported to:`
- path below

Example:

```text
Files exported to:
C:\Users\Emma\Documents\ArchiveCord\exports
```

Action:

- `Open folder`

Long paths:

- middle-truncate visually if necessary
- full path available in tooltip

## 8. Completed with issues

Use this state when at least one export failed but at least one succeeded.

### Header

Title:

- `Export finished with issues`

Subtitle examples:

- `2 exports completed · 1 failed`
- `Some conversations could not be exported.`

Icon:

- warning icon
- amber treatment, not red unless the whole operation failed

### Actions

Primary:

- `Retry failed`

Secondary:

- `Open completed folder`
- `View details`
- `Export again`

### Failed rows

Failed rows should be visually clear but calm.

Row fields:

- conversation name
- status: `Failed`
- short reason
- actions: `Retry`, `Details`

Examples:

- `Could not access channel.`
- `Output folder is not writable.`
- `Attachment download failed.`

Do not display stack traces inline.

## 9. All-failed state

If every export failed:

Title:

- `Export failed`

Subtitle:

- `No files were exported.`

Actions:

- `Try again`
- `Change destination`
- `View details`

If partial files exist, do not say no files were exported. Say:

- `Some partial files may exist in the output folder.`

## 10. Cancelled / stopped state

If the user cancelled:

Title:

- `Export stopped`

Subtitle examples:

- `1 export completed · 2 were cancelled`
- `Completed files were kept in the output folder.`

Actions:

- `Open folder`
- `Export remaining`
- `Export again`

Do not treat user cancellation as an error.

## 11. Review files action

`Review files` should open a secondary view or file browser style panel showing exported packages.

It should not dump raw JSON into the main workspace.

Review view can show:

- conversations
- message transcript artifact
- attachments folder
- metadata file
- open/reveal actions

Default action remains `Open folder`, because that maps to user expectation after an export.

## 12. Export again action

`Export again` should return to the ready workspace with the previous selection and settings preserved.

It should not clear selection by default.

If the user wants a new selection, provide:

- `Change selection`

## 13. View activity action

`View activity` reopens or expands the activity tray for the completed run.

If a full history view exists later, this action may open it, but it must still show the just-completed export first.

## 14. Error details panel

When user clicks `Details` on a failed row, show:

- friendly reason
- suggested fix
- technical details collapsed
- copy details button

Example:

```text
Design Team > #announcements failed
ArchiveCord could not access this channel. Your token may not have permission anymore.

Suggested fix:
Reconnect, then try again.

[Retry] [Copy details]

Technical details ▸
```

Do not show technical details expanded by default.

## 15. Visual hierarchy

Completion state should prioritize:

1. outcome title
2. primary next action
3. summary stats
4. completed/failed rows
5. details and technical information

Do not place details above the outcome.

## 16. Forbidden patterns

Do not:

- show a giant celebratory graphic
- use confetti
- make every action a primary button
- list raw files as the main result instead of conversations
- hide failed rows
- mark cancellation as a failure
- erase partial success information
- automatically clear the selection after completion

## 17. Acceptance checklist

A correct completion state must satisfy:

- user can tell success/failure within 2 seconds
- user can open the output folder immediately
- user can see which conversations completed
- partial failures are visible and recoverable
- technical details are available but not forced
- previous selection/settings are preserved for Export again
- raw export artifacts are secondary details, not the headline UI