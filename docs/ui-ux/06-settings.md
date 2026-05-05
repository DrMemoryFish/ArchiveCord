# 06 — Settings

This file defines the Settings surface for ArchiveCord.

Settings must be easy to find, but they must not dominate the main export workflow. Settings are where deeper defaults and account management live.

## 1. Purpose

Settings answers:

- Which Discord account/session is connected?
- How is the token stored or changed?
- Which appearance mode is used?
- What are the default export options?
- How should activity and previews behave?
- Where are diagnostics/logs?

Settings must not become a replacement for the main export workflow.

## 2. Opening settings

Settings opens from the top-right settings button in the app shell.

Allowed implementations:

1. Full main-workspace settings view.
2. Centered settings panel overlay.
3. Right-side panel.

Recommended first implementation:

- full main-workspace settings view below the same top bar
- left settings section list
- right settings content

This is easiest to implement in PySide while keeping layout stable.

## 3. Settings layout

Recommended layout:

```text
+--------------------------------------------------------------+
| Top bar                                                      |
+--------------------------------------------------------------+
| Settings                                                     |
| Customize ArchiveCord to fit your workflow.                  |
|                                                              |
| +-------------------+  +-----------------------------------+ |
| | Account           |  | Account / Connection              | |
| | Appearance        |  | ...                               | |
| | Export defaults   |  | ...                               | |
| | Activity/previews |  | ...                               | |
| | Diagnostics       |  | ...                               | |
| | About             |  | ...                               | |
| +-------------------+  +-----------------------------------+ |
+--------------------------------------------------------------+
```

Settings may replace the main workspace while open, but must retain a way to return to the previous workflow state.

## 4. Settings header

Title:

- `Settings`

Subtitle:

- `Customize ArchiveCord to fit your workflow.`

If settings replaces the main workspace, include a Back or Close affordance:

- `Back to export`
- or X button if overlay/panel

## 5. Settings section list

Left section list width:

- `180–220px`

Sections:

1. `Account`
2. `Appearance`
3. `Export defaults`
4. `Activity & previews`
5. `Diagnostics`
6. `About`

Each section row:

- icon: 16–18px
- label: 14px
- height: 36–40px
- active background: primary blue soft
- active text/icon: primary blue

Do not create many more sections unless necessary.

## 6. Account section

Section title:

- `Account / Connection`

### Connection status

Show:

- status dot
- text
- account name

Examples:

- `Connected as emma#1234`
- `Disconnected`
- `Connection failed`

### Token field

Label:

- `Discord token`

Field:

- masked by default
- reveal/hide button on right
- update/replace token action

Do not show token input permanently in the main app top bar once connected. It belongs here and in the not-connected state.

### Remember token

Control:

- checkbox or toggle

Label:

- `Remember token securely`

Helper text:

- `Stored using the operating system keyring when available.`

If keyring unavailable:

- disabled control
- helper text: `Secure token storage is unavailable on this system.`

### Actions

- `Reconnect`
- `Disconnect`
- `Clear saved token`

Button treatment:

- Reconnect: secondary
- Disconnect: destructive secondary
- Clear saved token: destructive secondary or text button

Do not use solid red for ordinary disconnect.

## 7. Appearance section

Section title:

- `Appearance`

Options:

- Light
- Dark
- Follow system

Recommended control:

- radio cards or segmented/radio row

Do not make the appearance selector visually dominant.

### Light/dark preview cards

If preview cards are used:

- small thumbnail only
- no giant decorative preview
- selected option border: primary blue
- selected radio/check visible

### Accent color

Optional later. If added, keep minimal.

Default accent:

- ArchiveCord blue `#1F6BFF`

Do not add many accent themes in first implementation.

## 8. Export defaults section

Section title:

- `Export defaults`

Fields:

### Default export folder

Label:

- `Default export folder`

Value:

- current path

Action:

- `Change...`

Also include:

- `Open folder after export` toggle

### Default format

Controls:

- TXT checkbox
- JSON checkbox
- Attachments checkbox

Default based on current app:

- TXT on
- JSON off unless user changes
- Attachments off unless user changes

### TXT details defaults

Controls:

- Include edited timestamps
- Include pinned markers
- Include reply references

Default based on current app:

- all on

### IDs/tooltips

Control:

- `Show IDs in tooltips`

Default:

- follow current app preference or true if already implemented that way

Do not show IDs inline in normal UI.

## 9. Activity & previews section

Section title:

- `Activity & previews`

Purpose:

- controls how export activity and live attachment previews behave

Controls:

### Show live attachment previews

Label:

- `Show live attachment previews`

Helper:

- `Shows a small preview of recent saved attachments while exporting.`

Default:

- on only if implementation is performant
- otherwise off until optimized

### Cache thumbnails during export

Label:

- `Cache thumbnails during export`

Helper:

- `Uses temporary low-resolution thumbnails to keep the interface responsive.`

Default:

- on if previews are enabled

### Clear preview cache after export

Label:

- `Clear preview cache after export`

Default:

- on

### Max recent previews

Optional control:

- default: 8
- allowed range: 4–16

Do not expose complex cache paths or memory internals unless in Diagnostics.

## 10. Diagnostics section

Section title:

- `Diagnostics`

Contents:

- View logs
- Open logs folder
- Copy diagnostic summary
- Clear logs

Logs are not a primary app tab.

### View logs

Opens a diagnostics/logs view.

Log view can contain:

- level filter
- search
- auto-scroll
- copy selected
- clear logs

This is allowed because the user explicitly opened diagnostics.

### Copy diagnostic summary

Copies:

- app version
- OS
- export root
- logs path
- connection status, without token
- recent error summary

Never copy token.

## 11. About section

Contents:

- app name
- version
- license
- repository link
- basic responsible-use note

Keep short.

## 12. Save behavior

Use immediate apply for simple preferences where safe:

- appearance
- toggles
- preview cache setting

Use explicit save for multi-field or sensitive settings if necessary:

- token update
- export folder changes if validation required

If explicit save exists:

- primary button: `Save changes`
- secondary: `Reset to defaults`

Do not mix immediate apply and unsaved changes without clear indication.

## 13. Validation

### Token

Validate token only when user clicks:

- `Reconnect`
- `Update token`

Do not validate on every keystroke.

### Export folder

When folder changes:

- verify writable
- if not writable, show inline error

Error text:

- `ArchiveCord can't write to this folder. Choose another folder.`

## 14. Settings visual style

Settings should use restrained grouping.

Group style:

- title
- optional helper text
- bordered group container or divider-only sections
- no decorative cards

Spacing:

- settings page margin: `24px`
- between groups: `24px`
- within group: `12–16px`

## 15. Security language

Use direct, calm language.

Allowed:

- `Your token is stored locally and encrypted when remembered.`
- `Never share your Discord token.`
- `Clear saved token`

Avoid:

- fear-heavy warnings
- legalistic paragraphs in the main settings screen
- exposing raw token unless user intentionally reveals it

## 16. Return behavior

When the user closes settings:

- return to previous app state
- preserve selected conversations
- preserve current export progress if any
- do not restart connection
- do not clear form state unnecessarily

If settings are opened during export:

- activity must keep running
- avoid settings actions that would invalidate active export unless blocked with explanation

Example:

- Disconnect button disabled during export, or requires confirmation:
  `Disconnecting will stop active exports.`

## 17. Forbidden patterns

Do not:

- leave token field permanently in the top bar after connection
- hide token management so deeply that users cannot find it
- make logs a main tab by default
- add dozens of settings sections
- add decorative appearance themes before core usability
- copy token in diagnostics
- reset selection after closing settings
- allow dangerous actions during export without clear warning

## 18. Acceptance checklist

A correct settings surface must satisfy:

- user can manage token/account
- user can choose light/dark/follow system
- user can change default export folder and formats
- user can control attachment preview behavior
- diagnostics/logs are available but not primary
- settings do not interrupt current workflow state
- sensitive token actions are clear and safe
- layout is compact and readable