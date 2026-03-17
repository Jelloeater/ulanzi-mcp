"""AWTRIX3 HTTP client for Ulanzi clock."""

from typing import Any

import httpx

from .config import settings


class AwtrixClient:
    """HTTP client for AWTRIX3 API."""

    def __init__(self, host: str, timeout: int = 10):
        """Initialize client with host address."""
        self.host = host.rstrip("/")
        self.timeout = timeout

        # Setup auth if provided
        auth: tuple[str, str] | None = None
        if settings.username and settings.password:
            auth = (settings.username, settings.password)

        self.client = httpx.AsyncClient(
            base_url=self.host,
            timeout=timeout,
            auth=auth,
        )

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def get(self, endpoint: str) -> dict[str, Any]:
        """Make GET request to API."""
        try:
            response = await self.client.get(f"/api/{endpoint}")
            response.raise_for_status()
            text = response.text.strip() if response.text else ""
            if not text:
                return {}
            try:
                return response.json()
            except Exception:
                return {"response": text}
        except Exception as e:
            raise Exception(f"API error on {endpoint}: {e}") from e

    async def post(self, endpoint: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make POST request to API."""
        try:
            response = await self.client.post(f"/api/{endpoint}", json=data)
            response.raise_for_status()
            text = response.text.strip() if response.text else ""
            if not text:
                return {"success": True}
            try:
                return response.json()
            except Exception:
                # Return text as dict if not JSON
                return {"response": text}
        except Exception as e:
            raise Exception(f"API error on {endpoint}: {e}") from e

    # === Status & Info ===

    async def get_stats(self) -> dict[str, Any]:
        """Get device statistics (battery, RAM, uptime, etc.)."""
        return await self.get("stats")

    async def get_settings(self) -> dict[str, Any]:
        """Get current clock settings."""
        return await self.get("settings")

    async def get_apps_in_loop(self) -> dict[str, Any]:
        """Get list of apps in the display loop."""
        return await self.get("loop")

    async def get_effects(self) -> dict[str, Any]:
        """Get list of available visual effects."""
        return await self.get("effects")

    async def get_transitions(self) -> dict[str, Any]:
        """Get list of available transition effects."""
        return await self.get("transitions")

    # === Power Control ===

    async def set_power(self, power: bool) -> dict[str, Any]:
        """Turn matrix on or off."""
        return await self.post("power", {"power": power})

    async def set_sleep(self, seconds: int) -> dict[str, Any]:
        """Send clock to deep sleep mode."""
        return await self.post("sleep", {"sleep": seconds})

    async def reboot(self) -> dict[str, Any]:
        """Reboot the clock."""
        return await self.post("reboot", None)

    # === App Navigation ===

    async def switch_app(self, app_name: str) -> dict[str, Any]:
        """Switch to a specific app."""
        return await self.post("switch", {"name": app_name})

    async def next_app(self) -> dict[str, Any]:
        """Go to next app in the loop."""
        return await self.post("nextapp", None)

    async def previous_app(self) -> dict[str, Any]:
        """Go to previous app in the loop."""
        return await self.post("previousapp", None)

    # === Custom Apps & Notifications ===

    async def show_notification(
        self,
        text: str,
        duration: int = 5,
        color: str | None = None,
        icon: str | None = None,
        sound: str | None = None,
        hold: bool = False,
        wakeup: bool = False,
        stack: bool = True,
    ) -> dict[str, Any]:
        """Display a notification."""
        data: dict[str, Any] = {"text": text, "duration": duration}

        if color:
            data["color"] = color
        if icon:
            data["icon"] = icon
        if sound:
            data["sound"] = sound
        if hold:
            data["hold"] = True
        if wakeup:
            data["wakeup"] = True
        if not stack:
            data["stack"] = False

        return await self.post("notify", data)

    async def show_custom_app(
        self,
        app_name: str,
        text: str | None = None,
        duration: int = 5,
        repeat: int = -1,
        color: str | None = None,
        background: str | None = None,
        icon: str | None = None,
        rainbow: bool = False,
        effect: str | None = None,
        save: bool = False,
    ) -> dict[str, Any]:
        """Create or update a custom app."""
        data: dict[str, Any] = {
            "name": app_name,
            "duration": duration,
            "repeat": repeat,
        }

        if text:
            data["text"] = text
        if color:
            data["color"] = color
        if background:
            data["background"] = background
        if icon:
            data["icon"] = icon
        if rainbow:
            data["rainbow"] = True
        if effect:
            data["effect"] = effect
        if save:
            data["save"] = True

        return await self.post("custom", data)

    async def delete_custom_app(self, app_name: str) -> dict[str, Any]:
        """Delete a custom app."""
        return await self.post(f"custom/{app_name}", None)

    async def dismiss_notification(self) -> dict[str, Any]:
        """Dismiss a held notification."""
        return await self.post("notify/dismiss", None)

    # === Visual Effects ===

    async def set_moodlight(
        self,
        brightness: int = 170,
        color: str | None = None,
        kelvin: int | None = None,
    ) -> dict[str, Any]:
        """Set mood lighting."""
        data: dict[str, Any] = {"brightness": brightness}

        if color:
            data["color"] = color
        if kelvin:
            data["kelvin"] = kelvin

        return await self.post("moodlight", data)

    async def set_indicator(
        self,
        indicator_id: int,
        color: str,
        blink: int | None = None,
        fade: int | None = None,
    ) -> dict[str, Any]:
        """Set a colored indicator (1-3)."""
        if indicator_id not in (1, 2, 3):
            raise ValueError("indicator_id must be 1, 2, or 3")

        data: dict[str, Any] = {"color": color}

        if blink:
            data["blink"] = blink
        if fade:
            data["fade"] = fade

        return await self.post(f"indicator{indicator_id}", data)

    async def clear_indicators(self) -> dict[str, Any]:
        """Clear all indicators."""
        for i in range(1, 4):
            await self.post(f"indicator{i}", {"color": "0"})
        return {"status": "cleared"}

    # === Sound ===

    async def play_sound(self, sound: str) -> dict[str, Any]:
        """Play a RTTTL melody from the MELODIES folder."""
        return await self.post("sound", {"sound": sound})

    async def play_rtttl(self, rtttl: str) -> dict[str, Any]:
        """Play a RTTTL string."""
        return await self.post("rtttl", {"rtttl": rtttl})

    # === Settings ===

    async def update_settings(self, settings_dict: dict[str, Any]) -> dict[str, Any]:
        """Update clock settings."""
        return await self.post("settings", settings_dict)


def get_client(index: int = 0) -> AwtrixClient:
    """Get an AWTRIX client for the specified clock index."""
    host = settings.get_host(index)
    return AwtrixClient(host, settings.api_timeout)
