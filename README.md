# ArchiveCord

[![Release](https://img.shields.io/github/v/release/DrMemoryFish/ArchiveCord)](https://github.com/DrMemoryFish/ArchiveCord/releases)

ArchiveCord is a desktop app for exporting Discord conversations (DMs and server channels) with filtering, formatted preview, attachment export, and real-time logs.

## Highlights
- Hierarchical conversation tree with DMs, servers, categories, and channels.
- Multi-selection across DMs/channels, including cross-server selections.
- Batch export with sequential execution and per-item plus overall progress.
- Export JSON, formatted TXT, and attachments.
- Before/after date and time filtering.
- Preview pane updates during export.
- Real-time Logs tab with level filter, search, auto-scroll, copy, and clear.
- Token handling with optional OS keyring storage.

## Requirements
- Windows 10/11, macOS, or Linux.
- Internet access to Discord API.

## Download and Install
1. Open [Releases](https://github.com/DrMemoryFish/ArchiveCord/releases).
2. Download the artifact for your platform:
- Windows portable: `ArchiveCord-v<version>-win64-portable.exe`
- Windows installer: `ArchiveCord-v<version>-win64-setup.exe`
- macOS primary: `ArchiveCord-v<version>-macos-universal.dmg`
- macOS fallback: `ArchiveCord-v<version>-macos-universal.zip` (contains `ArchiveCord.app`)
- Linux primary: `ArchiveCord-v<version>-linux-x86_64.AppImage`
- Linux fallback: `ArchiveCord-v<version>-linux-x86_64.tar.gz`

Run basics:
- Windows portable: run the EXE directly.
- Windows installer: run setup EXE and follow the wizard.
- macOS: open DMG or ZIP, move `ArchiveCord.app` to `Applications`, then run it.
- Linux AppImage: `chmod +x ArchiveCord-v<version>-linux-x86_64.AppImage` then run it.
- Linux tar.gz: extract and run `ArchiveCord`.

No Python is required for prebuilt release artifacts.

Unsigned build note:
- Current release artifacts are unsigned. First-run SmartScreen/Gatekeeper/desktop warnings are expected.

## Build From Source
### Requirements
- Python 3.11+ recommended.

### Install dependencies
Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

macOS/Linux (bash):
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Run
```bash
python -m app.main
```

## Packaging
The project includes packaging scripts for Windows, macOS, and Linux builds.

### Windows portable EXE
```powershell
pip install -r requirements-dev.txt
.\packaging\build_portable.ps1
```
Output:
- `dist/ArchiveCord-v<version>-win64-portable.exe`

### Windows installer EXE (Inno Setup)
Install Inno Setup 6 and ensure `ISCC.exe` is available.
If not in the default location:
```powershell
$env:INNO_SETUP_COMPILER = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
```
Build:
```powershell
.\packaging\build_installer.ps1
```
Output:
- `dist_installer/ArchiveCord-v<version>-win64-setup.exe`

### macOS app bundle plus DMG/ZIP
```bash
./packaging/build_macos.sh <version>
```
Output:
- `dist/ArchiveCord-v<version>-macos-universal.dmg`
- `dist/ArchiveCord-v<version>-macos-universal.zip`

### Linux AppImage plus tar.gz
```bash
./packaging/build_linux.sh <version>
```
Output:
- `dist/ArchiveCord-v<version>-linux-x86_64.AppImage`
- `dist/ArchiveCord-v<version>-linux-x86_64.tar.gz`

### Icon replacement
Replace:
```text
exe/app_logo.ico
```
This updates the app icon for packaged builds.

## Basic Usage
1. Paste your Discord user token.
2. Click `Connect`.
3. Check one or more DMs/channels in the tree.
4. Configure filters and export options.
5. Click `Export & Process`.
6. Monitor preview/progress and logs in real time.

## Conversation Tree and Selection
- Leaf nodes are DMs/channels and are strictly checked or unchecked.
- Parent nodes are servers/categories with derived tri-state display.
- Parent toggle behavior:
- Unchecked parent: selects all selectable descendants.
- Checked parent: deselects all selectable descendants.
- Partially checked parent: deselects all selectable descendants.
- Disabled/unavailable items are not selectable and are never exported.
- Keyboard:
- `Space`: toggles the focused item.
- `Enter`: expands/collapses a parent node.

Refresh behavior:
- When conversations reload (for example reconnect), selection is explicitly cleared.

## Export Behavior
- Export targets are derived from checked leaf nodes only (DM/channel), never parent nodes.
- Duplicate targets are removed by stable ID.
- If one item is selected, export uses single-export flow.
- If multiple items are selected, export runs through `BatchExportWorker` sequentially.
- Batch failure handling:
- Failed items are logged.
- Export continues with remaining items.
- Batch cancellation:
- Cancel stops queueing new items.
- Current in-flight item is allowed to finish cleanly.

## Progress and Preview
- Primary progress indicator shows current item export progress.
- Batch mode also shows overall progress (`Exporting X of Y`) and a batch progress bar.
- Preview always reflects the currently exporting item.
- After batch completion, preview remains on the last successful item.

## Export Options
- `Export JSON`: raw Discord message payloads.
- `Export formatted TXT`: readable transcript.
- `Export attachments/assets`: downloads attachments.
- `Include edited timestamps`: adds edited time to header.
- `Include pinned markers`: adds `[PINNED]` prefix.
- `Include reply references`: adds reply context line.

Default UI option states:
- `Export formatted TXT`: on
- `Include edited timestamps`: on
- `Include pinned markers`: on
- `Include reply references`: on

## Output Location
ArchiveCord defaults to user-writable paths resolved via `platformdirs`.

Default export root:
- User Documents folder: `ArchiveCord/exports`

Fallback export root (if Documents cannot be resolved):
- User app-data folder: `ArchiveCord/exports`

Default logs path:
- User app-data folder: `ArchiveCord/logs`

Logs fallback (if app-data cannot be resolved):
- A `logs` folder adjacent to the export root.

Platform examples:
- Windows export default: `C:\Users\<User>\Documents\ArchiveCord\exports`
- Windows logs default: `C:\Users\<User>\AppData\Local\ArchiveCord\logs`
- macOS export default: `~/Documents/ArchiveCord/exports`
- macOS logs default: `~/Library/Application Support/ArchiveCord/logs`
- Linux export default: `~/Documents/ArchiveCord/exports`
- Linux logs default: `~/.local/share/ArchiveCord/logs`

If you set a custom output directory in the UI, that value is persisted and reused on next launch.

Internal export structure is unchanged:
- DMs: `DMs/<DM Name>/`
- Server channels: `Servers/<Server Name>/<Channel Name>/`

Before starting an export, the app verifies export/log directories are writable. Export is blocked if checks fail.

## Filter Behavior
Filters are optional and use your local timezone.
- `Before`: excludes messages after the selected timestamp.
- `After`: excludes messages before the selected timestamp.

## Filename and TXT Format
Example filename:
- `ServerName #general [2026-01-01-2026-02-11] [0000-2359] [Exported 20260211_153500].txt`

TXT excerpt:
```text
[PINNED] Username#1234 (Nickname) 06-01-2026 09:42 PM (edited at 06-01-2026 09:50 PM)
(Replying to OtherUser#5678: original message content here)
Message content here
```

Formatting notes:
- Messages are separated by one blank line.
- Nickname is omitted if unavailable.
- Missing reply target is rendered as:
- `(Replying to Unknown User: Original message not found)`

## Logs
The Logs tab supports:
- Level filter (`INFO`, `WARNING`, `ERROR`, `DEBUG`)
- Search filter
- Auto-scroll toggle
- Copy selected line
- Clear logs

File logging:
- Rotating log file: `archivecord.log`
- Default size policy: 5 MB per file, 3 backups.

## Security Notes
Your token is treated like a password.

- If `Remember token` is off, token is not stored after the session.
- If `Remember token` is on, token is stored via OS keyring (`keyring` library).
- If keyring is unavailable, `Remember token` is disabled automatically.
- Using a Discord user token may violate Discord Terms of Service. Use at your own risk.

Windows keyring details:
- Location: Credential Manager -> Windows Credentials
- Service name: `ArchiveCord`
- Account name: `user_token`

## How to Get Your Discord Token
This app uses a Discord user token. Only use your own account and treat it like a password.

1. Open Discord in browser or desktop app.
2. Open Developer Tools (`F12` or `Ctrl+Shift+I`).
3. Go to `Network`.
4. Trigger requests by opening a DM or channel.
5. Open a request such as `science` or `messages`.
6. Copy the `Authorization` header value.

Important:
- Paste only the raw token.
- Do not share your token.

## Troubleshooting
- `Token must be a single line with no spaces.`
- Paste only the raw token with no extra whitespace.
- `Token invalid` or HTTP 401.
- Token is incorrect or expired.
- `Remember token` is disabled.
- No usable keyring backend is available on this system.
- Export is blocked due to output/log path.
- Select a writable output directory and retry.
- Missing channels.
- Token does not have permission for that guild/channel.
- First-run warning dialogs on Windows/macOS/Linux.
- Expected for unsigned binaries.

## Project Layout
- UI: `app/ui/`
- Core services: `app/core/`
- Workers: `app/workers/`
- Packaging scripts: `packaging/`

## License
MIT License. See `LICENSE`.

---

Use responsibly and in accordance with Discord terms.
