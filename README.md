# Discord Conversation Processor

[![Release](https://img.shields.io/github/v/release/DrMemoryFish/ChatForge)](https://github.com/DrMemoryFish/ChatForge/releases)

A production‑grade desktop app that unifies Discord conversation export, processing, and preview into a single workflow. It replaces multi‑tool manual steps with one cohesive, secure UI.

## Highlights
- Secure token handling with optional OS keychain storage.
- Hierarchical conversation discovery: DMs and Servers/Channels.
- Filter by before/after date and time.
- Export JSON, formatted TXT, and attachments.
- Non‑blocking async processing with progress indicator.
- In‑app formatted preview.
- Real‑time Logs tab with filtering, search, and copy controls.

## Requirements
- Windows 10/11 (tested)
- Python 3.11+ recommended
- Internet access to Discord API

## Install
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```powershell
python -m app.main
```

## Packaging (Portable + Installer)
The project includes packaging scripts for Windows builds.

### 1) Portable EXE (single file, no installer)
Install PyInstaller into your environment (use the same `.venv` you run the app with):
```powershell
pip install -r requirements-dev.txt
```

Build the portable EXE:
```powershell
.\packaging\build_portable.ps1
```

Output:
- `dist/DiscordConversationProcessor.exe`

### 2) Installer EXE (Inno Setup)
Install **Inno Setup 6** and ensure `ISCC.exe` is available.  
If it is not in the default path, set:
```powershell
$env:INNO_SETUP_COMPILER = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
```

Build the installer:
```powershell
.\packaging\build_installer.ps1
```

Output:
- `dist_installer/DiscordConversationProcessorSetup.exe`

### Icon Replacement
The application icon is sourced from:
```
exe/app_logo.ico
```
Replace that file to update the portable EXE, installer icon, and shortcuts.

## Basic Usage
1. Paste your Discord user token in the top bar.
2. Click **Connect**.
3. Select a DM or a channel from the left tree.
4. Configure filters and export options.
5. Click **Export & Process**.
6. View the formatted output in the preview pane and check the Logs tab for details.

## Export Options
- **Export JSON**: raw Discord message payloads.
- **Export formatted TXT**: human‑readable transcript (see format below).
- **Export attachments/assets**: downloads message attachments.
- **Include edited timestamps**: appends edited time to header.
- **Include pinned markers**: adds `[PINNED]` prefix to headers.
- **Include reply references**: adds reply block with resolved original message.

## Output Location
The output path is determined by the **Output folder** and **Base filename** fields in the Export panel.

Examples (default base filename `discord_export`):
- JSON: `output/discord_export.json`
- TXT: `output/discord_export.txt`
- Attachments: `output/discord_export_attachments/`

## Filter Behavior
Filters are optional and use your local timezone.
- **Before**: excludes messages after the selected timestamp.
- **After**: excludes messages before the selected timestamp.

## TXT Format (Excerpt)
```
[PINNED] Username#1234 (Nickname) 06-01-2026 09:42 PM (edited at 06-01-2026 09:50 PM)
(Replying to OtherUser#5678: original message content here)
Message content here
```

Formatting rules:
- One blank line separates each message block.
- If the nickname is missing, it is omitted.
- If the referenced message cannot be found, the reply line shows:
  `(Replying to Unknown User: Original message not found)`

## Logs
The Logs tab streams internal events in real time and supports:
- Level filter (INFO/WARNING/ERROR/DEBUG)
- Text search
- Auto‑scroll toggle
- Copy selected entry
- Clear logs

A rotating log file is also written to:
- `logs/discordsorter.log`

## Security Notes
Your token is treated like a password. This app never sends it to third‑party services.

- If **Remember token** is **off**, the token is **not stored** on disk; it exists only in memory for the current session.
- If **Remember token** is **on**, the token is stored using your OS keychain via the `keyring` library.

### Where It’s Stored (Windows)
When **Remember token** is enabled on Windows, the token is saved to **Windows Credential Manager**.

You can view or remove it here:
- **Control Panel → Credential Manager → Windows Credentials**

It is stored under:
- **Service name**: `DiscordSorter`
- **Account name**: `user_token`

Disable **Remember token** to avoid any local storage.

## How to Get Your Discord Token
This app uses a Discord **user token**. Only use your own account and handle it like a password.

1. Open Discord in a browser (recommended) or desktop app.
2. Open **Developer Tools**:
   - Browser: press `F12` or `Ctrl+Shift+I`.
   - Discord desktop app: press `Ctrl+Shift+I`.
3. Go to the **Network** tab.
4. In Discord, click into a DM or server channel to trigger network requests.
5. In the Network list, click a request named `science` or `messages`.
6. In the request headers, find `Authorization`.
7. Copy the token value (single line, no spaces).

**Important:** never share your token and avoid pasting anything except the raw token.

## Troubleshooting
- **“Token must be a single line with no spaces.”**
  Paste only the raw token (no extra whitespace or console output).
- **“Token invalid” or 401 errors**
  The token is incorrect or expired.
- **Rate limiting**
  The app automatically retries after Discord’s `retry_after` delay.
- **Missing channels**
  The token lacks permission for that guild/channel.

## Project Layout
- UI: `app/ui/`
- Core services: `app/core/`
- Workers (async threads): `app/workers/`

## License
MIT License. See `LICENSE`.

## Releases
Creating a tag like `v1.0.0` triggers the GitHub Actions release workflow.

```powershell
git tag v1.0.0
git push origin v1.0.0
```

---

This app uses a Discord user token as requested. Use responsibly and within Discord’s terms.
