from __future__ import annotations

import keyring

SERVICE_NAME = "ArchiveCord"
LEGACY_SERVICE_NAME = "DiscordSorter"
ACCOUNT_NAME = "user_token"


class TokenStoreError(RuntimeError):
    pass


def save_token(token: str) -> None:
    if not token:
        raise TokenStoreError("Token is empty")
    try:
        keyring.set_password(SERVICE_NAME, ACCOUNT_NAME, token)
    except Exception as exc:
        raise TokenStoreError(str(exc)) from exc


def load_token() -> str | None:
    try:
        token = keyring.get_password(SERVICE_NAME, ACCOUNT_NAME)
        if token:
            return token
        return keyring.get_password(LEGACY_SERVICE_NAME, ACCOUNT_NAME)
    except Exception as exc:
        raise TokenStoreError(str(exc)) from exc


def delete_token() -> None:
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
