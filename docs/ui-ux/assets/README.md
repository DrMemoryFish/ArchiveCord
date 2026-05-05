# UI/UX Reference Assets

This folder is reserved for visual references used by the ArchiveCord UI/UX redesign.

## Required reference image

The current preferred visual reference is the six-panel ArchiveCord concept board generated during design exploration.

Preferred file name once added:

```text
archivecord-six-panel-ui-concept-board.png
```

The concept board contains these panels:

1. Main Workspace — Ready to Export
2. Conversation Selector Drawer Open
3. Export in Progress — Activity Tray Expanded
4. Activity — Attachments Preview / Job Expanded
5. Export Complete — All Successful
6. Settings

Panel 1 is the strongest reference for the main workspace direction. The implementation should preserve its overall structure:

- compact top bar
- stable central workspace
- calm summary rows
- one dominant Export button
- no permanent DMs/server tree beside the ready state

Panel 2 is the reference for the selector drawer direction:

- left-side temporary selector
- search field
- All/DMs/Servers filter
- tree list
- pinned footer with selected count and Done

Panel 3 and 4 are references for activity behavior:

- progress remains inside the workflow
- activity is a tray/section, not a full dashboard by default
- attachment previews appear only as expanded detail

Panel 5 is the reference for completion:

- outcome first
- Open folder as the primary next action
- conversation-first result rows

Panel 6 is the reference for settings:

- low-key settings navigation
- account/token management inside settings
- appearance/defaults/diagnostics grouped clearly

## Important limitation

Do not treat the image as pixel-perfect truth. The Markdown specs in `docs/ui-ux/` override the image if they conflict.

The image is a layout and hierarchy reference. The written specs define exact behavior, state rules, colors, typography, accessibility, and implementation constraints.

## Asset handling rule

If a developer adds reference images to this folder, they should:

- keep file names descriptive
- avoid huge files where possible
- update this README with the file name and purpose
- avoid using generated image artifacts inside the actual app UI unless explicitly approved

Reference images are for implementation guidance only. They are not app assets by default.