# 12 — QA and Acceptance Tests

This file defines the manual and automated checks required before accepting the ArchiveCord UI/UX redesign.

This is not optional polish. These checks prevent the redesigned UI from looking good while breaking the actual export workflow.

## 1. Required command checks

Run after every implementation phase:

```bash
python -m unittest discover -s tests -v
python -m compileall app tests
```

If UI tests are added later, run them too.

No UI redesign phase is complete if existing backend/export tests fail.

## 2. Manual QA environment

Test at minimum:

- Windows 10/11 or the primary development OS
- light mode
- dark mode if implemented
- fresh settings profile if possible
- saved-token profile if possible
- no-network or invalid-token scenario
- small server/DM test account
- at least one export with attachments

## 3. Smoke test: fresh launch without saved token

Expected:

1. App opens.
2. Top bar is visible.
3. Main workspace shows `Connect to Discord`.
4. Token field is visible only in the connect panel.
5. Permanent DMs/servers tree is not visible.
6. Export button is not visible or not actionable.
7. Settings remains accessible if safe.

Fail if:

- app opens to a blank page
- token field is floating permanently in top bar
- export controls appear before connection
- logs/debug table is visible by default

## 4. Invalid token test

Steps:

1. Enter invalid token.
2. Click `Connect`.

Expected:

- state changes to connecting/loading
- input is disabled or guarded while connecting
- failure returns to connect state
- clear inline error appears
- token is not saved if remember is off
- no crash

Expected copy style:

- `Could not connect to Discord.`
- `Check your token and try again.`

Fail if:

- raw stack trace appears
- app remains stuck connecting
- token disappears unexpectedly
- logs become the main view

## 5. Valid connection test

Steps:

1. Enter valid token.
2. Click `Connect`.

Expected:

- account cluster shows connected state top-right
- account label appears, e.g. `emma#1234`
- main workspace shows connected/no-selection state
- primary action says `Select conversations`
- token field is no longer permanently visible

Fail if:

- connected badge floats randomly in center top bar
- permanent tree appears by default beside empty state
- app jumps into a dashboard/logs page

## 6. Selector drawer open/close test

Steps:

1. From connected/no-selection, click `Select conversations`.
2. Selector drawer opens.
3. Press Esc.
4. Open selector again.
5. Press X.
6. Open selector again.
7. Press Done.

Expected:

- drawer opens from left
- workspace remains stable behind it
- no major layout push
- search field is focused when drawer opens
- Esc closes drawer
- X closes drawer
- Done closes drawer
- closing does not clear selection unless user explicitly clears it

Fail if:

- drawer permanently replaces main workspace
- Export button jumps horizontally during open/close
- selection is lost on close

## 7. Selector search/filter test

Steps:

1. Open selector.
2. Select one DM.
3. Search for another conversation.
4. Switch All -> DMs -> Servers -> All.
5. Clear search.

Expected:

- selected count persists
- selected item remains selected even when hidden by search/filter
- All shows DMs and servers
- DMs shows DMs only
- Servers shows server tree only
- no IDs shown inline by default

Fail if:

- changing filter clears selection
- search mutates selected targets
- DMs/Servers become top-level app pages instead of drawer filters

## 8. Tree selection behavior test

Steps:

1. Expand a server.
2. Select one channel.
3. Select a parent server/category if supported.
4. Deselect parent.
5. Try selecting disabled/unavailable item if test data exists.

Expected:

- selected count updates correctly
- parent partial/checked/unchecked state is correct
- disabled item cannot be selected
- Space toggles focused item
- Enter expands/collapses parent

Fail if:

- parent selection exports non-leaf parent as a target
- disabled items export
- keyboard controls regress

## 9. Ready-to-export summary test

Steps:

1. Select 3–4 conversations.
2. Close selector.

Expected:

- main workspace title: `Ready to export`
- summary rows visible:
  - Selected conversations
  - Format
  - Date range
  - Destination
  - Advanced options
- Export button is primary and bottom-right/stable
- full conversation tree is not visible by default
- advanced options are collapsed

Fail if:

- app shows the old full form groups by default
- logs are visible
- multiple blue primary buttons compete
- selected conversations list consumes the whole screen

## 10. Edit settings from ready state test

Steps:

1. Change destination.
2. Change format.
3. Set custom date range.
4. Expand/collapse advanced options.

Expected:

- summary rows update after changes
- controls are available but not all visible by default
- destination validates writability
- Export button disables with explanation if invalid
- Export button location remains stable

Fail if:

- advanced controls stay permanently expanded after unrelated actions
- invalid destination only fails after export starts with no preflight clue

## 11. Single export success test

Steps:

1. Select one DM/channel.
2. Export TXT only.

Expected:

- state changes to `Export in progress`
- activity tray appears
- one job row shows specific status
- progress updates
- completion state appears
- `Open folder` action works
- output package exists

Fail if:

- app shows only generic progress with no target label
- user cannot tell what is being exported
- completion does not show output action

## 12. Batch export success test

Steps:

1. Select at least 3 targets.
2. Export.

Expected if backend is sequential:

- UI says `1 running · N queued`
- queued jobs show `Waiting to start`
- completed jobs show `Complete`
- current job shows specific step
- final state says all exports complete

Expected if backend becomes parallel:

- active count matches real number of running jobs

Fail if:

- UI claims multiple jobs are active when backend is sequential
- batch progress does not identify individual conversations

## 13. Batch partial failure test

Use a controlled failure if possible.

Expected:

- export continues for remaining jobs if backend supports current behavior
- final state says `Export finished with issues`
- completed jobs remain visible
- failed jobs show short reason
- failed jobs expose `Retry` and `Details`
- stack traces hidden behind Details

Fail if:

- one failure wipes out successful results
- app says `Export complete` when something failed
- raw traceback appears in main UI

## 14. Cancel behavior test

Steps:

1. Start batch export.
2. Cancel a queued job if supported.
3. Cancel all/remaining.

Expected:

- labels match backend truth
- if current item cannot stop immediately, UI says so or shows `Cancelling...`
- completed files remain accessible
- cancellation is not presented as app failure

Fail if:

- UI implies instant cancellation but job continues silently
- cancellation loses completed result info

## 15. Attachment preview test

Only run if attachment previews are implemented.

Steps:

1. Export a target with image attachments.
2. Expand running job row.
3. Watch recent attachment strip.
4. Click a thumbnail.

Expected:

- UI does not freeze
- low-res thumbnails appear only for previewable attachments
- non-previewable attachments use file icons
- max visible thumbnails respects spec
- clicking opens medium preview/details
- full resolution loads only after explicit action
- cache clears after export if setting is enabled

Fail if:

- thumbnails block export
- all attachments become a giant default gallery
- full-res images load automatically during export

## 16. Completion success test

Expected:

- title: `Export complete`
- subtitle includes successful count
- summary stats shown if known
- rows are conversation-first, not raw-file-first
- primary action: `Open folder`
- secondary actions: Review files, Export again, View activity if implemented

Fail if:

- main result is a list of `messages.txt`, `metadata.json`, `attachments/`
- no easy open-folder action
- selection/settings are lost when clicking Export again

## 17. Settings test

Steps:

1. Open Settings from top-right.
2. Visit Account, Appearance, Export defaults, Activity & previews, Diagnostics.
3. Close Settings.

Expected:

- previous workflow state preserved
- account/token controls in Account
- appearance mode available if implemented
- default export folder/formats available
- diagnostics/logs available under Diagnostics
- token is never copied in diagnostics

Fail if:

- settings clears selection
- logs remain a main top-level tab by default
- token appears in plain text without deliberate Reveal

## 18. Accessibility keyboard test

Steps:

1. Navigate app with keyboard only.
2. Open selector.
3. Search/select conversations.
4. Close selector.
5. Export.
6. Open settings.

Expected:

- visible focus ring everywhere
- Tab order is logical
- Esc closes drawer/settings/details
- Space toggles tree item
- Enter activates focused button or expands parent
- status is text + icon/color, not color alone

Fail if:

- keyboard trap exists
- focus disappears
- icon-only buttons lack tooltips/names

## 19. Dark mode visual test

If dark mode implemented:

Expected:

- same layout as light mode
- no neon backgrounds
- readable contrast
- selected states clear
- disabled states clear
- status colors distinct but calm

Fail if:

- dark mode uses different layout
- text contrast is weak
- blue/red/green are too saturated and noisy

## 20. Long names and long paths test

Use long server/channel names and a long output path.

Expected:

- names truncate gracefully
- full text available in tooltip/details
- row height does not explode
- Export button remains stable
- path middle-truncates visually if needed

Fail if:

- rows become huge
- actions move offscreen
- text overlaps controls

## 21. Minimum release acceptance

A UI redesign implementation is acceptable only if:

- all command checks pass
- all current export functionality still exists
- main workflow is visibly simpler than current UI
- selector drawer works
- ready summary works
- activity tray works
- completion states work
- settings preserves workflow state
- logs are available in diagnostics
- accessibility keyboard basics work
- no forbidden UI patterns from `07-implementation-guardrails.md` are present