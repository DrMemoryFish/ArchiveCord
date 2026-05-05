# 13 — Theme Tokens

This file turns the design-system values into implementation-oriented theme tokens.

Do not scatter raw hex colors, spacing values, or radius values across UI files. Use centralized constants or QSS variables/helpers where practical.

## 1. Token naming convention

Use semantic token names, not descriptive guesses.

Good:

- `COLOR_PRIMARY`
- `COLOR_SURFACE_MAIN`
- `SPACE_4`
- `RADIUS_BUTTON`

Bad:

- `blue1`
- `nice_gray`
- `card_color`
- `random_padding`

## 2. Light theme color tokens

```python
LIGHT_THEME = {
    "color.app.background": "#F7F9FC",
    "color.surface.main": "#FFFFFF",
    "color.surface.secondary": "#F3F6FB",
    "color.surface.tertiary": "#EEF2F7",

    "color.border.default": "#D8DEE8",
    "color.border.subtle": "#E6EAF1",
    "color.border.focus": "#AFC7FF",

    "color.text.primary": "#111827",
    "color.text.secondary": "#4B5563",
    "color.text.muted": "#6B7280",
    "color.text.disabled": "#9AA3B2",
    "color.text.inverse": "#FFFFFF",

    "color.primary.default": "#1F6BFF",
    "color.primary.hover": "#155BE6",
    "color.primary.pressed": "#0F49BD",
    "color.primary.soft": "#EAF1FF",

    "color.success.default": "#18A957",
    "color.success.soft": "#E8F8EF",
    "color.success.border": "#B7E8C9",

    "color.warning.default": "#B7791F",
    "color.warning.soft": "#FFF6DB",
    "color.warning.border": "#F3D58A",

    "color.danger.default": "#D93D3D",
    "color.danger.soft": "#FDECEC",
    "color.danger.border": "#F3B5B5",

    "color.neutral.chip": "#EEF2F7",
}
```

## 3. Dark theme color tokens

```python
DARK_THEME = {
    "color.app.background": "#07111F",
    "color.surface.main": "#0D1624",
    "color.surface.secondary": "#111C2D",
    "color.surface.tertiary": "#172236",

    "color.border.default": "#223047",
    "color.border.subtle": "#1B2638",
    "color.border.focus": "#4C7DFF",

    "color.text.primary": "#F4F7FB",
    "color.text.secondary": "#B6C2D2",
    "color.text.muted": "#7D8BA0",
    "color.text.disabled": "#59687D",
    "color.text.inverse": "#FFFFFF",

    "color.primary.default": "#4C7DFF",
    "color.primary.hover": "#6B93FF",
    "color.primary.pressed": "#3A66D9",
    "color.primary.soft": "rgba(76, 125, 255, 0.14)",

    "color.success.default": "#31C46D",
    "color.success.soft": "rgba(49, 196, 109, 0.14)",
    "color.success.border": "rgba(49, 196, 109, 0.35)",

    "color.warning.default": "#D99A2B",
    "color.warning.soft": "rgba(217, 154, 43, 0.15)",
    "color.warning.border": "rgba(217, 154, 43, 0.35)",

    "color.danger.default": "#F05D5D",
    "color.danger.soft": "rgba(240, 93, 93, 0.14)",
    "color.danger.border": "rgba(240, 93, 93, 0.35)",

    "color.neutral.chip": "#172236",
}
```

## 4. Spacing tokens

```python
SPACING = {
    "space.1": 4,
    "space.2": 8,
    "space.3": 12,
    "space.4": 16,
    "space.5": 20,
    "space.6": 24,
    "space.8": 32,
}
```

Usage rules:

- top bar horizontal padding: `space.4`
- main workspace outer margin: `space.6`
- panel padding: `space.6`
- summary row horizontal padding: `space.4`
- row internal gap: `space.3`
- tight icon/text gap: `space.2`

## 5. Radius tokens

```python
RADIUS = {
    "radius.window": 16,
    "radius.panel": 12,
    "radius.drawer": 12,
    "radius.row_container": 12,
    "radius.button": 8,
    "radius.input": 8,
    "radius.thumbnail": 6,
    "radius.pill": 999,
}
```

## 6. Typography tokens

```python
TYPOGRAPHY = {
    "font.family": "Segoe UI, SF Pro, Inter, Noto Sans, sans-serif",

    "font.size.app_title": 16,
    "font.size.page_title": 24,
    "font.size.section_title": 16,
    "font.size.body": 14,
    "font.size.secondary": 13,
    "font.size.caption": 12,
    "font.size.preview": 13,

    "font.weight.regular": 400,
    "font.weight.medium": 500,
    "font.weight.semibold": 600,
    "font.weight.bold": 700,
}
```

PySide note: if exact font weight rendering differs by platform, choose the closest visible weight.

## 7. Size tokens

```python
SIZES = {
    "top_bar.height": 56,
    "button.height.standard": 40,
    "button.height.primary": 44,
    "input.height.standard": 40,
    "input.height.compact": 32,
    "summary_row.min_height": 72,
    "activity_row.height": 64,
    "drawer.width.compact": 360,
    "drawer.width.standard": 400,
    "drawer.width.max": 440,
    "icon.top_bar": 18,
    "icon.summary": 20,
    "avatar.small": 28,
    "avatar.standard": 32,
    "thumbnail.inline": 40,
    "thumbnail.preview": 64,
}
```

## 8. QSS mapping guidance

If using Qt stylesheets, map tokens to selectors consistently.

Examples:

```css
QWidget#AppRoot {
    background: {color.app.background};
    color: {color.text.primary};
}

QFrame#MainPanel {
    background: {color.surface.main};
    border: 1px solid {color.border.default};
    border-radius: {radius.panel}px;
}

QPushButton#PrimaryButton {
    background: {color.primary.default};
    color: {color.text.inverse};
    border: none;
    border-radius: {radius.button}px;
    min-height: {button.height.primary}px;
    padding-left: 20px;
    padding-right: 20px;
    font-weight: 600;
}

QPushButton#PrimaryButton:hover {
    background: {color.primary.hover};
}

QPushButton#PrimaryButton:pressed {
    background: {color.primary.pressed};
}

QLineEdit {
    background: {color.surface.main};
    border: 1px solid {color.border.default};
    border-radius: {radius.input}px;
    min-height: {input.height.standard}px;
    padding-left: 12px;
    padding-right: 12px;
}

QLineEdit:focus {
    border: 1px solid {color.border.focus};
}
```

Do not copy these examples blindly if the app uses a different styling mechanism. Preserve the token mapping.

## 9. Component token assignments

### Top bar

- height: `top_bar.height`
- background: `color.surface.main`
- bottom border: `color.border.subtle`
- app title: `font.size.app_title`, semibold

### Main workspace panel

- background: `color.surface.main`
- border: `color.border.default`
- radius: `radius.panel`
- padding: `space.6`

### Summary row

- min height: `summary_row.min_height`
- divider: `color.border.subtle`
- icon color: `color.text.secondary` or primary blue when active
- title: text primary, semibold
- value: text secondary

### Selector drawer

- width: standard `drawer.width.standard`
- background: `color.surface.main`
- border: `color.border.default`
- shadow: overlay shadow if supported

### Activity tray

- background: `color.surface.main`
- border: `color.border.default`
- radius: `radius.row_container`

### Status chips

- complete: success soft + success text
- queued: warning soft + warning text
- failed: danger soft + danger text
- running: primary soft + primary text
- neutral: neutral chip + secondary text

## 10. Forbidden token usage

Do not:

- use raw hex values in component files when a token exists
- invent a second primary blue
- use random margin values like 17px or 23px
- use box shadows on every panel
- use different row heights for equivalent rows without reason
- make dark mode a separate layout

## 11. Acceptance checklist

A correct theme implementation must satisfy:

- light and dark themes share the same semantic token names
- primary action blue is consistent across the app
- selected states use primary soft/primary default consistently
- status colors are consistent across top bar, activity, and completion
- focus states are visible
- disabled states are readable
- no random raw colors are scattered across new UI files