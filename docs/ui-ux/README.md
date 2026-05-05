# ArchiveCord UI/UX Specification

This folder is the product design contract for ArchiveCord's GUI redesign. It is written for a literal implementer. Do not treat it as inspiration, mood, or loose direction. Treat it as a strict specification.

ArchiveCord is a desktop utility for connecting to Discord, selecting conversations, exporting them, and monitoring the export result. It performs a complex task, but the UI must feel calm, compact, and obvious.

The interface must not look or behave like a SaaS dashboard, web app, developer console, debug tool, or marketing landing page. It must feel like a focused desktop workspace.

## Core product sentence

> Export these conversations with these settings.

Every visible element must support that sentence. If an element does not help the user connect, select conversations, review export settings, export, monitor progress, recover from failure, or adjust defaults, it should be hidden one layer deeper.

## Required UI states and docs

Read these files in order before implementing anything:

1. `00-design-system.md`  
   Shared colors, typography, spacing, shape language, status language, controls, motion, and accessibility requirements.

2. `01-app-shell-navigation.md`  
   The top bar, account/connection placement, workspace behavior, drawer behavior, and navigation rules.

3. `02-main-workspace-ready-to-export.md`  
   Main workspace in the ready state. Covers the summary rows, primary action, footer, and stable layout rules.

4. `03-conversation-selector-drawer.md`  
   Conversation selector drawer. Covers search, All/DMs/Servers filtering, DMs/server tree, selection states, footer, and closing behavior.

5. `04-export-progress-activity.md`  
   Export in progress. Covers the activity tray, per-job status rows, running/queued/complete/failed states, cancellation, and attachment preview expansion.

6. `05-export-complete.md`  
   Successful and partially failed completion states. Covers completion summaries, actions, export result rows, and failure recovery.

7. `06-settings.md`  
   Settings surface. Covers account/token management, appearance, export defaults, activity/previews, diagnostics, and about.

8. `07-implementation-guardrails.md`  
   Non-negotiable implementation rules, forbidden UI patterns, PySide implementation notes, and acceptance checklist.

## Global UX rules

1. **Use one main workspace.** Do not create many app-level pages for the core task.
2. **The conversation tree is a tool, not the app.** Show it in the selector drawer. Do not keep it permanently visible during export unless the user explicitly opens it.
3. **The main workspace must remain stable.** Opening the selector drawer must not shove the export summary around.
4. **Use progressive disclosure.** Advanced options, logs, diagnostics, and attachment previews are deeper layers.
5. **Show system status plainly.** The user must always know whether ArchiveCord is connected, ready, exporting, complete, failed, or waiting.
6. **Do not expose raw technical artifacts as the main UX.** `messages.txt`, `metadata.json`, and `attachments/` are file details, not headline UI.
7. **One primary action per state.** Connect, Select conversations, Export, Open folder, or Retry failed. Do not show multiple equally dominant actions.
8. **No fake controls.** Do not add pause/resume unless the backend truly supports it. Cancel, retry, details, and open folder are allowed.
9. **Use plain language before technical language.** Technical details live under Details or Diagnostics.
10. **No visual noise.** Avoid decorative cards, heavy shadows, oversized hero areas, unnecessary icons, and dashboard-style modules.

## Main app states

The app has six user-facing states:

- Not connected / connect state
- Connected with no selection
- Ready to export
- Conversation selector open
- Export in progress
- Export complete or complete with issues
- Settings opened as a secondary surface

These are states of one product, not unrelated pages.

## Source visual direction

The current preferred concept is the six-panel UI concept board generated from the ArchiveCord specification, especially panel 1: **Main Workspace — Ready to Export**.

Use that concept's structure as the layout basis:

- compact top bar
- calm white/light-gray workspace
- clear blue primary action
- summary rows with icons on the left and actions on the right
- drawer-based selector
- activity tray for export progress
- restrained settings surface

Do not copy visual noise from earlier concept images that kept the full DMs/servers tree permanently visible beside every state. That approach is too broad and visually heavy.

## Relationship to current code

The current PySide UI has a top token bar, permanent conversation tree, right-side export tab, and logs tab. The redesign should move toward:

- token management in Settings / first-connect state
- account connection state in the top-right account cluster
- selector drawer instead of permanent tree as the main default
- main workspace summary instead of many visible settings groups
- activity tray instead of full dashboard by default
- logs inside Settings > Diagnostics or export details

Current backend behavior and export architecture should not be broken by UI changes.