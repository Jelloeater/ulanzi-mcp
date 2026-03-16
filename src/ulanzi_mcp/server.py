"""MCP server for Ulanzi TC001 Smart Pixel Clock."""

import asyncio
from typing import Any, Optional

from mcp.server.fastmcp import FastMCP

# Import via absolute path for mcp dev compatibility
from ulanzi_mcp.client import AwtrixClient, get_client
from ulanzi_mcp.config import settings

# Create FastMCP server instance
mcp = FastMCP("ulanzi-mcp")

# Context for clock index (can be overridden per request)
_clock_index: int = 0


def set_clock_index(index: int) -> None:
    """Set the default clock index for tools."""
    global _clock_index
    _clock_index = index


async def get_client_for_request(clock_index: Optional[int] = None) -> AwtrixClient:
    """Get client for the specified clock index or default."""
    index = clock_index if clock_index is not None else _clock_index
    return get_client(index)


# =============================================================================
# Status & Info Tools
# =============================================================================


@mcp.tool()
async def get_clock_stats(clock_index: Optional[int] = None) -> dict[str, Any]:
    """
    Get device statistics from the clock.

    Returns battery level, RAM usage, uptime, and other device info.

    Args:
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.get_stats()
    finally:
        await client.close()


@mcp.tool()
async def get_clock_settings(clock_index: Optional[int] = None) -> dict[str, Any]:
    """
    Get current clock settings.

    Returns current display settings like brightness, colors, time format, etc.

    Args:
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.get_settings()
    finally:
        await client.close()


@mcp.tool()
async def get_apps_in_loop(clock_index: Optional[int] = None) -> dict[str, Any]:
    """
    Get list of all apps in the display rotation loop.

    Returns the names of all apps that cycle through on the display.

    Args:
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.get_apps_in_loop()
    finally:
        await client.close()


@mcp.tool()
async def get_available_effects(clock_index: Optional[int] = None) -> dict[str, Any]:
    """
    Get list of all available visual effects.

    Returns available background effects that can be used with custom apps.

    Args:
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.get_effects()
    finally:
        await client.close()


# =============================================================================
# Power Control Tools
# =============================================================================


@mcp.tool()
async def set_power(power: bool, clock_index: Optional[int] = None) -> dict[str, Any]:
    """
    Turn the matrix display on or off.

    Args:
        power: True to turn on, False to turn off
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.

    Returns:
        Status of the power operation
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.set_power(power)
    finally:
        await client.close()


@mcp.tool()
async def set_brightness(brightness: int, clock_index: Optional[int] = None) -> dict[str, Any]:
    """
    Set the matrix brightness.

    Args:
        brightness: Brightness level from 0 (off) to 255 (max)
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.

    Returns:
        Updated settings
    """
    if not 0 <= brightness <= 255:
        raise ValueError("Brightness must be between 0 and 255")

    client = await get_client_for_request(clock_index)
    try:
        return await client.update_settings({"BRI": brightness})
    finally:
        await client.close()


@mcp.tool()
async def set_sleep(seconds: int, clock_index: Optional[int] = None) -> dict[str, Any]:
    """
    Send the clock to deep sleep mode.

    The clock will wake up after the specified seconds or when the middle button is pressed.

    Args:
        seconds: Number of seconds to sleep
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.set_sleep(seconds)
    finally:
        await client.close()


@mcp.tool()
async def reboot_clock(clock_index: Optional[int] = None) -> dict[str, Any]:
    """
    Reboot the clock.

    Args:
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.reboot()
    finally:
        await client.close()


# =============================================================================
# App Navigation Tools
# =============================================================================


@mcp.tool()
async def switch_to_app(app_name: str, clock_index: Optional[int] = None) -> dict[str, Any]:
    """
    Switch to a specific app.

    Args:
        app_name: Name of the app to switch to (e.g., 'Time', 'Date', 'Temperature', 'Humidity', 'Battery', or custom app name)
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.switch_app(app_name)
    finally:
        await client.close()


@mcp.tool()
async def next_app(clock_index: Optional[int] = None) -> dict[str, Any]:
    """
    Switch to the next app in the display loop.

    Args:
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.next_app()
    finally:
        await client.close()


@mcp.tool()
async def previous_app(clock_index: Optional[int] = None) -> dict[str, Any]:
    """
    Switch to the previous app in the display loop.

    Args:
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.previous_app()
    finally:
        await client.close()


# =============================================================================
# Custom App & Notification Tools
# =============================================================================


@mcp.tool()
async def show_notification(
    text: str,
    duration: int = 5,
    color: Optional[str] = None,
    icon: Optional[str] = None,
    sound: Optional[str] = None,
    hold: bool = False,
    wakeup: bool = False,
    stack: bool = True,
    clock_index: Optional[int] = None,
) -> dict[str, Any]:
    """
    Display a notification on the clock.

    Args:
        text: Text to display
        duration: How long to show the notification in seconds (default: 5)
        color: Text color as hex string (e.g., "#FF0000") or RGB array
        icon: Icon name to display
        sound: Sound filename to play
        hold: Keep notification on screen until dismissed (default: False)
        wakeup: Wake up the matrix if it's off (default: False)
        stack: Stack with other notifications (default: True)
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.show_notification(
            text=text,
            duration=duration,
            color=color,
            icon=icon,
            sound=sound,
            hold=hold,
            wakeup=wakeup,
            stack=stack,
        )
    finally:
        await client.close()


@mcp.tool()
async def show_custom_app(
    app_name: str,
    text: Optional[str] = None,
    duration: int = 5,
    repeat: int = -1,
    color: Optional[str] = None,
    background: Optional[str] = None,
    icon: Optional[str] = None,
    rainbow: bool = False,
    effect: Optional[str] = None,
    save: bool = False,
    clock_index: Optional[int] = None,
) -> dict[str, Any]:
    """
    Create or update a custom app on the clock.

    Args:
        app_name: Unique name for this custom app
        text: Text to display
        duration: How long to show in seconds (default: 5)
        repeat: How many times to repeat scrolling (-1 = infinite, default)
        color: Text color as hex string or RGB array
        background: Background color
        icon: Icon name to display
        rainbow: Show text in rainbow colors (default: False)
        effect: Background effect name
        save: Save to flash memory (default: False)
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.show_custom_app(
            app_name=app_name,
            text=text,
            duration=duration,
            repeat=repeat,
            color=color,
            background=background,
            icon=icon,
            rainbow=rainbow,
            effect=effect,
            save=save,
        )
    finally:
        await client.close()


@mcp.tool()
async def delete_custom_app(app_name: str, clock_index: Optional[int] = None) -> dict[str, Any]:
    """
    Delete a custom app from the clock.

    Args:
        app_name: Name of the custom app to delete
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.delete_custom_app(app_name)
    finally:
        await client.close()


@mcp.tool()
async def dismiss_notification(clock_index: Optional[int] = None) -> dict[str, Any]:
    """
    Dismiss a held notification.

    Args:
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.dismiss_notification()
    finally:
        await client.close()


# =============================================================================
# Visual Effects Tools
# =============================================================================


@mcp.tool()
async def set_moodlight(
    brightness: int = 170,
    color: Optional[str] = None,
    kelvin: Optional[int] = None,
    clock_index: Optional[int] = None,
) -> dict[str, Any]:
    """
    Set mood lighting on the clock.

    Args:
        brightness: Brightness level 0-255 (default: 170)
        color: Color as hex string or RGB array
        kelvin: Color temperature in Kelvin
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    if not 0 <= brightness <= 255:
        raise ValueError("Brightness must be between 0 and 255")

    client = await get_client_for_request(clock_index)
    try:
        return await client.set_moodlight(brightness=brightness, color=color, kelvin=kelvin)
    finally:
        await client.close()


@mcp.tool()
async def set_indicator(
    indicator_id: int,
    color: str,
    blink: Optional[int] = None,
    fade: Optional[int] = None,
    clock_index: Optional[int] = None,
) -> dict[str, Any]:
    """
    Set a colored indicator on the clock.

    Indicators are small notification signs displayed on specific areas:
    - Indicator 1: Upper right corner
    - Indicator 2: Right side
    - Indicator 3: Lower right corner

    Args:
        indicator_id: Which indicator (1, 2, or 3)
        color: Color as hex string (e.g., "#FF0000") or RGB array
        blink: Blink interval in milliseconds
        fade: Fade interval in milliseconds
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    if indicator_id not in (1, 2, 3):
        raise ValueError("indicator_id must be 1, 2, or 3")

    client = await get_client_for_request(clock_index)
    try:
        return await client.set_indicator(
            indicator_id=indicator_id,
            color=color,
            blink=blink,
            fade=fade,
        )
    finally:
        await client.close()


@mcp.tool()
async def clear_indicators(clock_index: Optional[int] = None) -> dict[str, Any]:
    """
    Clear all indicators from the clock.

    Args:
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.clear_indicators()
    finally:
        await client.close()


# =============================================================================
# Sound Tools
# =============================================================================


@mcp.tool()
async def play_sound(sound: str, clock_index: Optional[int] = None) -> dict[str, Any]:
    """
    Play a RTTTL melody from the MELODIES folder.

    Args:
        sound: Name of the sound file (without extension)
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.play_sound(sound)
    finally:
        await client.close()


@mcp.tool()
async def play_rtttl(rtttl: str, clock_index: Optional[int] = None) -> dict[str, Any]:
    """
    Play a RTTTL melody string directly.

    Args:
        rtttl: RTTTL melody string (e.g., ":d=4,o=5,b=180:...")
        clock_index: Optional index of clock to target (0-based). Defaults to first clock.
    """
    client = await get_client_for_request(clock_index)
    try:
        return await client.play_rtttl(rtttl)
    finally:
        await client.close()


# =============================================================================
# Server Entry Point
# =============================================================================


def main():
    """Run the MCP server."""
    # Print configuration info
    hosts = settings.get_hosts_list()
    print(f"Starting Ulanzi MCP Server...")
    print(f"  Hosts: {hosts}")
    print(f"  MQTT Prefix: {settings.mqtt_prefix}")
    print(f"  Timeout: {settings.api_timeout}s")
    print(f"  Auth: {'Yes' if settings.username else 'No'}")
    print()

    # Run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
