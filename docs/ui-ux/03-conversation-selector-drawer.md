# 03 — Conversation Selector Drawer

This file defines the conversation selector drawer used to choose DMs and server channels.

The selector is a focused temporary surface. It is not the main app. It is a tool the user opens when they need to choose or change conversations.

## 1. Purpose

The selector drawer answers:

- What conversations are available?
- How can I quickly find one?
- Which conversations are selected?
- How do I confirm the selection?

It must not feel like a separate app page. It must not permanently take over the layout.

## 2. Drawer behavior

The selector opens from the left side of the window.

Required behavior:

- overlays the main workspace
- does not permanently resize or shove the main workspace
- preserves current selection
- supports keyboard and mouse selection
- closes with `Done`, `X`, `Esc`, or selector toggle button
- retains the user's current filter/search during one open session

Optional overlay:

- dim background behind drawer lightly
- do not blur heavily
- do not use a dark modal treatment that makes the app feel blocked unless necessary

## 3. Drawer size

Recommended width:

- `360px` compact
- `400px` standard
- `440px` maximum for large windows

Do not exceed 40% of the app window width.

Minimum usable width:

- `320px`

Height:

- fills available height below top bar or overlays from below top bar depending implementation
- if overlaying the full window height, preserve top bar visual continuity

## 4. Drawer visual style

Style:

- background: main surface
- border-right: `1px solid` border color
- radius: optional `12px` if drawer floats inside window with margins
- shadow: allowed, soft and low opacity

Padding:

- outer padding: `16px`
- internal section spacing: `16px`

Do not make each tree row a card.

## 5. Header

Header layout:

```text
Select conversations                                      [X]
```

Title:

- text: `Select conversations`
- size: 18px
- weight: 700
- primary text

Close button:

- icon: X
- size: `32px x 32px`
- accessible label: `Close conversation selector`

Close behavior:

- closes drawer without clearing selection

Do not use `Cancel` unless closing would discard temporary uncommitted changes. Recommended behavior is live selection, so `X` simply closes.

## 6. Search field

Position:

- directly below header

Placeholder:

- `Search conversations`

Style:

- full width
- height: 38–40px
- search icon on left
- clear icon appears when text is entered

Behavior:

- filters visible conversation rows live
- search matches DM names, server names, channel names, and optionally IDs if IDs are enabled
- preserves selected items even when hidden by search

Empty search result:

Title:

- `No conversations found`

Body:

- `Try a different search.`

Do not clear the user's selection when search changes.

## 7. Filter segmented control

Position:

- directly below search field

Segments:

- `All`
- `DMs`
- `Servers`

Default:

- `All`

Behavior:

- All: shows DMs and servers
- DMs: shows direct messages/group DMs only
- Servers: shows server tree only

Style:

- segmented control using design-system rules
- active segment: primary blue background, white text
- inactive segments: secondary surface background, primary/secondary text

These are filters, not app-level pages.

## 8. Content sections

### All filter

Shows:

1. `Direct messages`
2. `Servers`

### DMs filter

Shows only:

- `Direct messages`

### Servers filter

Shows only:

- `Servers`

Section headings:

- size: 13–14px
- weight: 650
- primary text
- top margin: `16px`
- bottom margin: `8px`

Use section disclosure if the section can collapse.

## 9. Direct message rows

Each DM row contains:

```text
[checkbox] [avatar] [name] [optional metadata/status]
```

Row height:

- `40–44px`

Padding:

- horizontal: `4–8px`
- vertical: `4px`

Avatar:

- size: `28–32px`
- circular
- show real avatar when available
- fallback: colored initials or neutral user icon

Name:

- 14px
- primary text
- semibold only if selected or active, otherwise regular/medium

System DM label:

- small chip: `SYSTEM`
- background: primary blue or neutral chip depending emphasis
- text size: 10–11px

Selected state:

- checkbox checked blue
- row background: primary blue soft
- text may use primary blue for selected leaf name

Hover:

- secondary surface background

## 10. Server tree rows

Server root row:

```text
[disclosure chevron] [checkbox if parent selectable] [server avatar/icon] [server name]
```

Channel row:

```text
[indent] [checkbox] [# icon] [channel name]
```

Category row, if shown:

```text
[indent] [disclosure chevron] [checkbox if parent selectable] [category name]
```

Indentation:

- server root: 0
- category: 16–20px
- channel: 32–40px

Do not use deep indentation beyond this. If Discord data has deeper hierarchy, flatten or use category/channel only.

## 11. Parent selection behavior

Parent nodes may support selecting all selectable descendants.

Rules:

- unchecked parent click: select all selectable descendants
- checked parent click: deselect all selectable descendants
- partial parent click: deselect all selectable descendants unless current code chooses select-all; keep behavior consistent and documented in tooltip

Parent visual state:

- unchecked
- checked
- indeterminate/partial

Disabled children must not be selected by parent toggles.

## 12. Disabled/unavailable rows

Unavailable channel row style:

- text disabled color
- checkbox disabled
- optional label: `Unavailable`
- tooltip with reason if known

Do not hide unavailable rows if their presence helps explain missing channels. If too noisy, hide behind a setting later.

## 13. Selected count footer

Footer is pinned to bottom of drawer.

Layout:

```text
4 conversations selected                         [Done]
```

Also include `Clear selection` as a text button only if at least one item is selected.

Recommended footer layout:

```text
4 conversations selected        Clear selection   [Done]
```

If space is tight, use:

```text
4 selected                                      [Done]
Clear selection
```

Footer style:

- top border: divider color
- padding: `12–16px`
- background: main surface

Done button:

- primary
- text: `Done`
- disabled only if no selection and drawer was opened from an empty state requiring selection

Clear selection:

- secondary text button
- danger only if user explicitly asks for destructive style; default neutral/blue link is fine

## 14. Selection persistence

Selection must persist when:

- switching All/DMs/Servers filters
- searching
- collapsing server/category nodes
- closing and reopening drawer
- moving to export-ready state

Selection is cleared only when:

- user presses `Clear selection`
- conversation reload invalidates the selection
- user disconnects/reconnects and current backend requires clearing selection

If reload clears selection, show a calm status message.

## 15. Keyboard behavior

Required:

- `Esc`: close drawer
- `Tab`: move through header, search, filter, tree, footer
- `Shift+Tab`: reverse
- `Space`: toggle focused checkbox/tree item
- `Enter`: expand/collapse parent or activate focused button
- Arrow up/down: move through tree rows
- Arrow right: expand parent
- Arrow left: collapse parent

Focus must be visible.

## 16. Search focus shortcut

When the selector opens:

- focus the search field by default if no item is currently focused

Global shortcut:

- `Ctrl+F`: open selector and focus search, unless focus is inside a text field where native behavior is expected

## 17. Empty/loading states

### Loading conversations

Show:

- small spinner
- text: `Loading conversations...`

Do not show empty tree skeletons unless already available.

### No DMs

Text:

- `No direct messages found.`

### No servers

Text:

- `No servers found.`

### Connection required

If selector opened while disconnected:

- title: `Connect to Discord first`
- body: `ArchiveCord needs a connection before it can load conversations.`
- primary action: `Connect`

## 18. Tooltips and IDs

IDs should be hidden by default.

If `Show IDs in tooltips` is enabled:

- DM row tooltip may show channel ID and participant IDs
- server row tooltip may show guild ID
- channel row tooltip may show channel ID

Do not display IDs inline in normal row text.

## 19. Relationship to current code

Current code has a permanent `QTreeWidget` in the left panel. The target design moves this tree into a drawer.

Implementation may reuse:

- current tree population logic
- icon cache
- selection model
- keyboard behavior
- tooltip preference

But the tree should become temporary/secondary, not always visible next to the ready/export states.

## 20. Forbidden patterns

Do not:

- make DMs and Servers separate full app pages
- permanently show the conversation tree during export by default
- use huge row cards inside the tree
- reset selection when filtering/searching
- hide selected count
- use animation that causes major layout jumping
- show raw Discord IDs inline by default
- require multiple steps after selecting before the user can export

## 21. Acceptance checklist

A correct selector drawer must satisfy:

- user can search conversations immediately
- user can filter All/DMs/Servers
- user can select DMs and server channels
- selected count is always visible
- Done closes the drawer and keeps selection
- opening/closing drawer does not disrupt the main workspace layout
- keyboard selection works
- disabled/unavailable channels cannot be selected
- IDs remain hidden unless tooltip setting is enabled