from __future__ import annotations

import os
from dataclasses import dataclass

from platformdirs import user_data_dir, user_documents_dir


APP_NAME = "ArchiveCord"
WRITE_PROBE = ".archivecord_write_test.tmp"


@dataclass(frozen=True)
class DefaultPathResolution:
    export_root: str
    logs_dir: str
    export_fallback_used: bool
    logs_fallback_used: bool
    warnings: tuple[str, ...]


def _norm(path: str) -> str:
    return os.path.abspath(os.path.normpath(path))


def _user_documents_dir() -> str | None:
    try:
        documents = user_documents_dir()
    except Exception:
        documents = ""
    if documents:
        return _norm(documents)
    return None


def _user_app_data_root() -> str | None:
    try:
        app_data = user_data_dir(APP_NAME, appauthor=False)
    except Exception:
        app_data = ""
    if app_data:
        return _norm(app_data)
    return None


def resolve_default_paths() -> DefaultPathResolution:
    warnings: list[str] = []
    documents = _user_documents_dir()
    app_data_root = _user_app_data_root()

    export_fallback_used = False
    if documents:
        export_root = os.path.join(documents, APP_NAME, "exports")
    elif app_data_root:
        export_root = os.path.join(app_data_root, "exports")
        export_fallback_used = True
        warnings.append("Documents folder unavailable. Falling back to LocalAppData/user app data for exports.")
    else:
        export_root = os.path.join(os.path.expanduser("~"), APP_NAME, "exports")
        export_fallback_used = True
        warnings.append("Documents and user app data unavailable. Falling back to user profile path for exports.")

    logs_fallback_used = False
    if app_data_root:
        logs_dir = os.path.join(app_data_root, "logs")
    else:
        logs_dir = os.path.join(os.path.dirname(_norm(export_root)), "logs")
        logs_fallback_used = True
        warnings.append("LocalAppData/user app data unavailable. Falling back to export-adjacent logs path.")

    return DefaultPathResolution(
        export_root=_norm(export_root),
        logs_dir=_norm(logs_dir),
        export_fallback_used=export_fallback_used,
        logs_fallback_used=logs_fallback_used,
        warnings=tuple(warnings),
    )


def ensure_writable_directory(path: str) -> tuple[bool, str | None]:
    target = _norm(path)
    try:
        os.makedirs(target, exist_ok=True)
    except Exception as exc:
        return False, f"Failed to create directory '{target}': {exc}"

    probe = os.path.join(target, WRITE_PROBE)
    try:
        with open(probe, "w", encoding="utf-8") as handle:
            handle.write("ok")
        os.remove(probe)
    except Exception as exc:
        return False, f"Directory is not writable '{target}': {exc}"

    return True, None
