from __future__ import annotations

import keyring

SERVICE_NAME = "ArchiveCord"
LEGACY_SERVICE_NAME = "DiscordSorter"
ACCOUNT_NAME = "user_token"


class TokenStoreError(RuntimeError):
    pass


def keyring_available() -> tuple[bool, str | None]:
    try:
        backend = keyring.get_keyring()
    except Exception as exc:
        return False, f"Keyring backend unavailable: {exc}"

    try:
        priority = backend.priority
        if callable(priority):
            priority = priority()
    except Exception:
        priority = None

    if isinstance(priority, (int, float)) and priority <= 0:
        return False, f"Keyring backend '{backend.__class__.__name__}' is not usable."

    try:
        keyring.get_password(SERVICE_NAME, ACCOUNT_NAME)
        return True, None
    except keyring.errors.NoKeyringError as exc:
        return False, f"Keyring backend unavailable: {exc}"
    except Exception:
        # Backend exists; runtime errors here should not mark keyring as globally unavailable.
        return True, None


def save_token(token: str) -> None:
    if not token:
        raise TokenStoreError("Token is empty")
    ok, reason = keyring_available()
    if not ok:
        raise TokenStoreError(reason or "Keyring backend unavailable.")
    try:
        keyring.set_password(SERVICE_NAME, ACCOUNT_NAME, token)
    except Exception as exc:
        raise TokenStoreError(str(exc)) from exc


def load_token() -> str | None:
    ok, reason = keyring_available()
    if not ok:
        raise TokenStoreError(reason or "Keyring backend unavailable.")
    try:
        token = keyring.get_password(SERVICE_NAME, ACCOUNT_NAME)
        if token:
            return token
        return keyring.get_password(LEGACY_SERVICE_NAME, ACCOUNT_NAME)
    except Exception as exc:
        raise TokenStoreError(str(exc)) from exc


def delete_token() -> None:
    ok, reason = keyring_available()
    if not ok:
        raise TokenStoreError(reason or "Keyring backend unavailable.")
    try:
        keyring.delete_password(SERVICE_NAME, ACCOUNT_NAME)
    except keyring.errors.PasswordDeleteError:
        pass
    except Exception as exc:
        raise TokenStoreError(str(exc)) from exc
    try:
        keyring.delete_password(LEGACY_SERVICE_NAME, ACCOUNT_NAME)
    except keyring.errors.PasswordDeleteError:
        return
    except Exception as exc:
        raise TokenStoreError(str(exc)) from exc
