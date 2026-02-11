from __future__ import annotations

import logging
import time
from typing import Any, Optional

import requests

BASE_URL = "https://discord.com/api/v9"


class DiscordAPIError(RuntimeError):
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class DiscordClient:
    def __init__(self, token: str, timeout: int = 30):
        if not token:
            raise DiscordAPIError("Token is empty")
        self._token = token
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": token,
                "User-Agent": "DiscordSorter/1.0 (+https://discord.com)",
                "Accept": "application/json",
            }
        )

    def close(self) -> None:
        self._session.close()

    def _request(self, method: str, path: str, params: Optional[dict] = None) -> Any:
        url = f"{BASE_URL}{path}"
        logger = logging.getLogger("discordsorter.api")
        logger.debug("API request %s %s", method, path)
        while True:
            try:
                response = self._session.request(
                    method,
                    url,
                    params=params,
                    timeout=self._timeout,
                )
            except requests.RequestException as exc:
                raise DiscordAPIError(f"Network error: {exc}") from exc
            if response.status_code == 429:
                try:
                    payload = response.json()
                    retry_after = float(payload.get("retry_after", 1.0))
                except Exception:
                    retry_after = 1.0
                logger.warning("Rate limited. Retrying in %ss.", retry_after)
                time.sleep(retry_after)
                continue
            if response.status_code == 204:
                return None
            if 200 <= response.status_code < 300:
                if response.text:
                    return response.json()
                return None
            try:
                detail = response.json()
            except Exception:
                detail = response.text
            raise DiscordAPIError(
                f"Discord API error {response.status_code}: {detail}", response.status_code
            )

    def validate_token(self) -> dict:
        return self._request("GET", "/users/@me")

    def get_dms(self) -> list[dict]:
        return self._request("GET", "/users/@me/channels")

    def get_guilds(self) -> list[dict]:
        return self._request("GET", "/users/@me/guilds")

    def get_guild_channels(self, guild_id: str) -> list[dict]:
        return self._request("GET", f"/guilds/{guild_id}/channels")

    def get_channel_messages(self, channel_id: str, before_id: Optional[str] = None, limit: int = 100) -> list[dict]:
        params: dict[str, Any] = {"limit": limit}
        if before_id:
            params["before"] = before_id
        return self._request("GET", f"/channels/{channel_id}/messages", params=params)
