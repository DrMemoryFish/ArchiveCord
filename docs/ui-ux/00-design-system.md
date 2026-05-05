# 00 — Design System

This file defines the visual and interaction system for ArchiveCord. All UI states must use these rules unless another file explicitly overrides them.

## 1. Product feel

ArchiveCord must feel:

- calm
- compact
- deliberate
- trustworthy
- easy to scan
- precise
- desktop-native
- powerful underneath a simple surface

ArchiveCord must not feel:

- flashy
- web-dashboard-like
- developer-console-like
- marketing-heavy
- playful or toy-like
- empty and oversized
- crowded and technical
- template-like

The product should look refined through restraint, not decoration.

## 2. Visual identity

ArchiveCord's identity comes from repeated structural details:

- a compact desktop top bar
- a stable main workspace
- left-side temporary selector drawer
- blue checkboxes and blue selected-row treatment
- summary rows with one icon column, one text column, and one action column
- small green connection dot beside account status
- clear status chips in activity rows
- low-contrast dividers instead of heavy cards
- one dominant blue primary button per state

Do not introduce unrelated decorative motifs. Do not use gradients as the main identity. Do not add large illustrations except in the not-connected empty state, and even there they must be small and restrained.

## 3. Color palette

Use this palette exactly unless platform rendering requires tiny adjustments.

### Light mode

| Role | Hex | Usage |
|---|---:|---|
| App background | `#F7F9FC` | Window background behind main panels. |
| Main surface | `#FFFFFF` | Workspace panels, drawer, settings surface. |
| Secondary surface | `#F3F6FB` | Subtle inactive tabs, soft row hover, small neutral surfaces. |
| Tertiary surface | `#EEF2F7` | Disabled backgrounds and quiet segmented controls. |
| Border | `#D8DEE8` | Main panel borders and input borders. |
| Divider | `#E6EAF1` | Row separators and section dividers. |
| Text primary | `#111827` | Headings and primary labels. |
| Text secondary | `#4B5563` | Descriptions and secondary values. |
| Text muted | `#6B7280` | Hints, timestamps, footer text. |
| Text disabled | `#9AA3B2` | Disabled labels and inactive controls. |
| Primary blue | `#1F6BFF` | Primary action, selected filter, selected checkbox. |
| Primary blue hover | `#155BE6` | Hover state for primary action. |
| Primary blue pressed | `#0F49BD` | Pressed state for primary action. |
| Primary blue soft | `#EAF1FF` | Selected rows, icon wells, soft active backgrounds. |
| Primary blue border | `#AFC7FF` | Focus/active border. |
| Success green | `#18A957` | Connected, complete, success. |
| Success soft | `#E8F8EF` | Success chip background. |
| Warning amber | `#B7791F` | Queued/warning text. |
| Warning soft | `#FFF6DB` | Warning chip background. |
| Danger red | `#D93D3D` | Failed/destructive/cancel. |
| Danger soft | `#FDECEC` | Error chip background. |
| Neutral chip | `#EEF2F7` | Neutral status chip background. |

### Dark mode

| Role | Hex | Usage |
|---|---:|---|
| App background | `#07111F` | Window background. |
| Main surface | `#0D1624` | Workspace panels and drawer. |
| Secondary surface | `#111C2D` | Row hover, inactive tabs, settings groups. |
| Tertiary surface | `#172236` | Inputs, disabled surfaces. |
| Border | `#223047` | Main borders. |
| Divider | `#1B2638` | Row separators. |
| Text primary | `#F4F7FB` | Headings and primary labels. |
| Text secondary | `#B6C2D2` | Secondary content. |
| Text muted | `#7D8BA0` | Hints and metadata. |
| Text disabled | `#59687D` | Disabled controls. |
| Primary blue | `#4C7DFF` | Primary action and selected states. |
| Primary blue hover | `#6B93FF` | Hover state. |
| Primary blue pressed | `#3A66D9` | Pressed state. |
| Primary blue soft | `rgba(76, 125, 255, 0.14)` | Selected row and icon wells. |
| Success green | `#31C46D` | Connected and complete. |
| Warning amber | `#D99A2B` | Queued/warning. |
| Danger red | `#F05D5D` | Failed/cancel. |

## 4. Typography

Use a system font stack.

Recommended stack:

- Windows: `Segoe UI`
- macOS: `SF Pro` / `.AppleSystemUIFont`
- Linux fallback: `Inter`, `Noto Sans`, system sans-serif

Do not use decorative fonts. Do not use monospace except for file paths, filenames, IDs, and transcript previews.

### Type scale

| Token | Size | Weight | Usage |
|---|---:|---:|---|
| App title | 16px | 650 | `ArchiveCord` in top bar. |
| Page title | 24px | 700 | Main workspace title, e.g. `Ready to export`. |
| Section title | 16px | 650 | Summary row title, drawer section title. |
| Body | 14px | 400 | Standard labels and body copy. |
| Body strong | 14px | 600 | Important values and row names. |
| Secondary | 13px | 400 | Description text and metadata. |
| Caption | 12px | 400 | Footer text, timestamps, helper text. |
| Button | 14px | 600 | Button labels. |
| Monospace preview | 13px | 400 | Transcript preview and file path snippets. |

### Text rules

- Keep labels short.
- Use sentence case, not title case, except product name and proper nouns.
- Prefer `Ready to export`, not `Export Configuration Dashboard`.
- Prefer `Change`, not `Modify selected export destination configuration`.
- Do not expose internal class names, API names, worker names, or stack traces in normal UI.

## 5. Spacing system

Use a strict 4px-based spacing rhythm.

| Token | Pixels | Usage |
|---|---:|---|
| `space-1` | 4px | Tight icon/text gaps. |
| `space-2` | 8px | Small internal gaps. |
| `space-3` | 12px | Standard control gaps. |
| `space-4` | 16px | Section padding. |
| `space-5` | 20px | Large internal panel spacing. |
| `space-6` | 24px | Major section spacing. |
| `space-8` | 32px | Page-level spacing. |

Do not use arbitrary spacing values unless necessary for platform alignment. In PySide, use layout margins and spacing to match these tokens.

## 6. Radius and shape

| Element | Radius |
|---|---:|
| App window | 14–18px if custom chrome supports it. |
| Main workspace panel | 12px |
| Drawer | 12px |
| Summary rows container | 10–12px |
| Buttons | 8px |
| Inputs | 8px |
| Chips/pills | 999px |
| Small thumbnails | 6px |

Avoid extreme rounding. ArchiveCord should not feel cartoonish.

## 7. Borders and elevation

Use borders for stable surfaces and shadows only for temporary overlays.

### Stable surfaces

Main workspace, summary containers, settings groups, and activity rows use:

- border: `1px solid #D8DEE8` in light mode
- border: `1px solid #223047` in dark mode
- no heavy shadow

### Drawer

The conversation selector drawer is temporary and may use elevation:

- border: `1px solid #D8DEE8`
- shadow: soft, low opacity, visually behind the drawer only
- no dramatic floating card effect

Suggested CSS-like shadow description:

- `0 18px 45px rgba(17, 24, 39, 0.12)` light mode
- `0 18px 45px rgba(0, 0, 0, 0.35)` dark mode

Do not apply this shadow to every card.

## 8. Icons

Use simple line icons where possible. Icons support recognition; they do not decorate.

Icon size:

- top bar icons: 18px
- summary row icons: 20px
- drawer row icons/avatars: 28–32px avatar; 16px channel icon
- activity status icons: 16–20px

Icon colors:

- normal: `#4B5563` light, `#B6C2D2` dark
- active: primary blue
- success: success green
- warning: warning amber
- danger: danger red

Do not use multicolored icons except for server/user avatars or the ArchiveCord product icon.

## 9. Buttons

### Primary button

Use for exactly one primary action per state.

Examples:

- Connect
- Done
- Export
- Open folder
- Retry failed

Style:

- background: `#1F6BFF`
- hover: `#155BE6`
- pressed: `#0F49BD`
- text: white
- radius: 8px
- height: 38–44px depending on context
- horizontal padding: 16–24px
- font: 14px, semibold

### Secondary button

Use for supporting actions.

Examples:

- Change
- Edit
- Review files
- Export again
- Reveal
- Update token

Style:

- background: `#FFFFFF`
- border: `#D8DEE8`
- text: `#111827`
- hover background: `#F3F6FB`

### Destructive button

Use for disconnect, cancel, clear saved token, cancel all.

Style:

- background: transparent or `#FFFFFF`
- border: danger red at low opacity
- text: danger red
- use solid red only for confirmed destructive states, not ordinary cancel controls

## 10. Inputs

Input height:

- standard: 36–40px
- compact: 32px where necessary

Input styling:

- background: main surface
- border: border color
- radius: 8px
- text: primary
- placeholder: muted
- focus border: primary blue border
- focus ring: subtle, not thick

Search inputs must include a search icon on the left.

Password/token inputs must include reveal/hide control on the right.

## 11. Segmented controls

Used for the selector filters only:

- All
- DMs
- Servers

Style:

- container background: secondary/tertiary surface
- active segment background: primary blue
- active text: white
- inactive text: primary or secondary
- height: 36px
- radius: 8px

Do not use segmented controls for unrelated settings unless there are exactly 2–3 mutually exclusive choices.

## 12. Status language

Use exact status labels:

Connection:

- Connected
- Connecting
- Disconnected
- Connection failed

Export job:

- Queued
- Fetching messages
- Formatting messages
- Saving attachments
- Writing files
- Finalizing
- Complete
- Failed
- Cancelled

Batch/activity:

- Export in progress
- Export complete
- Export finished with issues
- Waiting to start

Do not use vague labels like `Processing` if a more specific label is known.

## 13. Motion

Motion must be subtle and practical.

Allowed:

- selector drawer slide-in: 140–180ms ease-out
- drawer slide-out: 120–160ms ease-in
- activity tray expand/collapse: 120–180ms
- advanced options expand/collapse: 120–160ms
- progress bars update smoothly

Forbidden:

- bounce animations
- excessive easing
- animated backgrounds
- confetti
- attention-seeking motion
- layout movement that shifts the user's main workspace unpredictably

The selector drawer must overlay the workspace instead of constantly pushing it around.

## 14. Accessibility

Minimum requirements:

- visible keyboard focus for every interactive control
- logical tab order
- Space toggles checkboxes
- Enter activates focused primary action where safe
- Esc closes drawer, dialogs, and expanded preview panels
- arrow keys navigate tree rows
- color is never the only status indicator
- status always includes text plus color/icon
- all icon-only buttons require accessible names/tooltips
- contrast must be readable in both light and dark mode

Focus ring:

- 2px primary blue border or outline
- do not rely on shadow-only focus

## 15. Layout density

ArchiveCord should be compact, but not cramped.

Rules:

- Do not use giant hero sections.
- Do not show more than 5 main summary rows in the ready state.
- Do not show logs in the main workspace unless a failure detail is expanded.
- Do not show raw file lists by default during export.
- Do not show attachment thumbnails unless a job is saving attachments or the user expands job details.

## 16. Dark mode

Dark mode must use the same structure and hierarchy as light mode.

Do not create a separate dark-mode layout.

Requirements:

- same spacing
- same row structure
- same icons
- same control placement
- adjusted colors only
- no neon or high-saturation backgrounds

## 17. Empty states

Empty states must be compact and action-oriented.

Allowed:

- short title
- one sentence
- one primary action
- optional small note

Forbidden:

- huge decorative hero images
- marketing slogans
- large blank areas

Example:

Title: `Choose conversations to export`  
Body: `Select DMs or server channels to create an export.`  
Primary action: `Select conversations`

## 18. Implementation reminder

Do not implement the design system by hardcoding colors randomly in different files. Centralize style constants or QSS tokens where practical.

If PySide styling limits exact values, approximate the behavior while preserving:

- hierarchy
- spacing
- labels
- control placement
- visible states
- progressive disclosure
- accessibility