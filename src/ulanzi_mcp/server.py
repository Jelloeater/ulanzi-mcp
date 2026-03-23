"""MCP server for Ulanzi TC001 Smart Pixel Clock."""

from typing import Any

from mcp.server.fastmcp import FastMCP

# Import via absolute path for mcp dev compatibility
from ulanzi_mcp.client import AwtrixClient, get_client
from ulanzi_mcp.config import settings

# Create FastMCP server instance
mcp = FastMCP("ulanzi-mcp")


async def get_client_for_request(clock_index: int | None = None) -> AwtrixClient:
    """Get client for the specified clock index or default (0)."""
    index = clock_index if clock_index is not None else 0
    return get_client(index)


# =============================================================================
# Status & Info Tools
# =============================================================================


@mcp.tool()
async def get_clock_stats(clock_index: int | None = None) -> dict[str, Any]:
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
async def get_clock_settings(clock_index: int | None = None) -> dict[str, Any]:
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
async def get_apps_in_loop(clock_index: int | None = None) -> dict[str, Any]:
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
async def get_available_effects(clock_index: int | None = None) -> dict[str, Any]:
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
async def set_power(power: bool, clock_index: int | None = None) -> dict[str, Any]:
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
async def set_brightness(brightness: int, clock_index: int | None = None) -> dict[str, Any]:
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
async def set_sleep(seconds: int, clock_index: int | None = None) -> dict[str, Any]:
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
async def reboot_clock(clock_index: int | None = None) -> dict[str, Any]:
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
async def switch_to_app(app_name: str, clock_index: int | None = None) -> dict[str, Any]:
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
async def next_app(clock_index: int | None = None) -> dict[str, Any]:
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
async def previous_app(clock_index: int | None = None) -> dict[str, Any]:
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
    color: str | None = None,
    icon: str | None = None,
    sound: str | None = None,
    hold: bool = False,
    wakeup: bool = False,
    stack: bool = True,
    clock_index: int | None = None,
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
    text: str | None = None,
    duration: int = 5,
    repeat: int = -1,
    color: str | None = None,
    background: str | None = None,
    icon: str | None = None,
    rainbow: bool = False,
    effect: str | None = None,
    save: bool = False,
    clock_index: int | None = None,
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
async def delete_custom_app(app_name: str, clock_index: int | None = None) -> dict[str, Any]:
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
async def dismiss_notification(clock_index: int | None = None) -> dict[str, Any]:
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
    color: str | None = None,
    kelvin: int | None = None,
    clock_index: int | None = None,
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
    blink: int | None = None,
    fade: int | None = None,
    clock_index: int | None = None,
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
async def clear_indicators(clock_index: int | None = None) -> dict[str, Any]:
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
async def play_sound(sound: str, clock_index: int | None = None) -> dict[str, Any]:
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
async def play_rtttl(rtttl: str, clock_index: int | None = None) -> dict[str, Any]:
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
# Resources (Ingest)
# =============================================================================


@mcp.resource("ulanzi://stats")
async def stats_resource() -> str:
    """
    Provides device statistics as a readable resource.

    Returns battery level, RAM usage, uptime, and other device info.
    This resource can be read by agents to quickly check clock status.
    """
    import json

    client = await get_client_for_request(None)
    try:
        data = await client.get_stats()
        return json.dumps(data, indent=2)
    finally:
        await client.close()


@mcp.resource("ulanzi://settings")
async def settings_resource() -> str:
    """
    Provides current clock settings as a readable resource.

    Returns display settings like brightness, colors, time format, etc.
    """
    import json

    client = await get_client_for_request(None)
    try:
        data = await client.get_settings()
        return json.dumps(data, indent=2)
    finally:
        await client.close()


@mcp.resource("ulanzi://apps")
async def apps_resource() -> str:
    """
    Provides list of all apps in the display rotation loop.

    Returns the names of all apps that cycle through on the display.
    """
    import json

    client = await get_client_for_request(None)
    try:
        data = await client.get_apps_in_loop()
        return json.dumps(data, indent=2)
    finally:
        await client.close()


@mcp.resource("ulanzi://effects")
async def effects_resource() -> str:
    """
    Provides list of all available visual effects.

    Returns available background effects that can be used with custom apps.
    """
    import json

    client = await get_client_for_request(None)
    try:
        data = await client.get_effects()
        return json.dumps(data, indent=2)
    finally:
        await client.close()


@mcp.resource("ulanzi://transitions")
async def transitions_resource() -> str:
    """
    Provides list of all available transition effects.

    Returns transitions for app switching animations.
    """
    import json

    client = await get_client_for_request(None)
    try:
        data = await client.get_transitions()
        return json.dumps(data, indent=2)
    finally:
        await client.close()


# =============================================================================
# Prompts (Inject)
# =============================================================================


@mcp.prompt()
def notify_urgent(text: str, reason: str) -> str:
    """
    Creates a prompt for urgent notifications that demand immediate attention.

    Use this when the clock needs to display critical alerts with sound.

    Args:
        text: The urgent message to display
        reason: Why this is urgent (e.g., "Fire alarm", "Security breach", "Medical alert")

    Returns:
        A prompt instructing how to display the urgent notification
    """
    return f"""Display an urgent notification on the Ulanzi clock:

1. First, wake up the clock if it's off using show_notification with wakeup=True
2. Show the notification:
   - text: "{text}"
   - hold: True (keep showing until dismissed)
   - wakeup: True
   - color: "#FF0000" (red for urgency)
   - duration: 10 seconds or more
3. Play an alert sound using play_sound with a suitable alert tone

The reason for this urgent notification: {reason}"""


@mcp.prompt()
def notify_meeting(meeting_name: str, minutes_until: int) -> str:
    """
    Creates a prompt for meeting reminder notifications.

    Use this to remind users about upcoming meetings with a polite chime.

    Args:
        meeting_name: Name of the meeting
        minutes_until: Minutes until the meeting starts

    Returns:
        A prompt instructing how to display the meeting reminder
    """
    if minutes_until <= 5:
        urgency = "starting NOW"
        color = "#FF8800"
    elif minutes_until <= 15:
        urgency = f"in {minutes_until} minutes"
        color = "#FFAA00"
    else:
        urgency = f"in {minutes_until} minutes"
        color = "#00AAFF"

    return f"""Display a meeting reminder on the Ulanzi clock:

1. Show notification:
   - text: "{meeting_name}"
   - subtitle: "Starting {urgency}"
   - duration: {min(10, minutes_until)} seconds
   - color: "{color}" (blue for normal, orange for soon)
   - wakeup: True
2. Play a gentle chime sound using play_sound (avoid jarring tones)

Meeting: {meeting_name}
Time until meeting: {minutes_until} minutes"""


@mcp.prompt()
def notify_timer(label: str, duration_seconds: int) -> str:
    """
    Creates a prompt for timer countdown notifications.

    Use this to set up countdown timers with visual feedback.

    Args:
        label: Description of what the timer is for
        duration_seconds: Total duration in seconds

    Returns:
        A prompt instructing how to display the timer
    """
    minutes = duration_seconds // 60
    seconds = duration_seconds % 60
    time_str = f"{minutes}:{seconds:02d}" if minutes > 0 else f"{seconds}s"

    return f"""Set up a timer countdown on the Ulanzi clock:

1. Create a custom app for the timer:
   - app_name: "timer_{label.lower().replace(" ", "_")}"
   - text: "{label}\\n{time_str}"
   - repeat: -1 (keep updating)
   - color: "#00FF00" (green)
   - duration: 5 seconds
2. The timer should count down - update the display periodically

Timer: {label}
Duration: {duration_seconds} seconds ({time_str})"""


@mcp.prompt()
def victory_alert(custom_text: str | None = None) -> str:
    """
    Creates a victory celebration prompt with FF7-style jingle!

    Use this when celebrating achievements, completed tasks, or wins.
    Includes the classic FF7 victory theme melody.

    Args:
        custom_text: Optional text to display during celebration

    Returns:
        A prompt instructing how to play the victory celebration
    """
    # FF7 Victory Theme RTTTL melody
    ff7_victory = "FF7VICT:d=4,o=5,b=180:32p,c6,4a#,c6,4a#,c6,4d#6,2f6,32p,f6,4d#6,c6,4a#,f6,4g#6,2a#6,32p,c6,4a#,c6,4a#,c6,4d#6,2f6,32p,f6,4d#6,c6,4a#,f6,4g#6,2c7,32p,c7,4c7,2c7"

    text_display = (
        f'\\n2. Show custom app "victory":\\n   - text: "{custom_text}"\\n   - color: "#FFD700" (gold)\\n   - rainbow: True'
        if custom_text
        else ""
    )

    return f"""Celebrate a victory on the Ulanzi clock with the classic FF7 victory jingle!

1. Play the victory melody using play_rtttl with this RTTTL string:
   {ff7_victory}{text_display}

2. Optional: Set moodlight to gold/yellow for extra celebration

Let the victory ring out! 🎉"""


@mcp.prompt()
def status_report(clock_index: int | None = None) -> str:
    """
    Creates a prompt for checking full clock status.

    Use this when you need a comprehensive overview of clock state.

    Args:
        clock_index: Optional clock index to target (0-based)

    Returns:
        A prompt instructing how to gather all clock status information
    """
    index_note = f" (targeting clock index {clock_index})" if clock_index else ""

    return f"""Gather comprehensive status from the Ulanzi clock{index_note}:

1. Get device statistics using get_clock_stats:
   - Battery level and charging status
   - RAM usage
   - Device uptime
   - Current app being displayed

2. Get current settings using get_clock_settings:
   - Brightness level
   - Time format (12h/24h)
   - Auto-brightness status

3. Get apps in loop using get_apps_in_loop:
   - List all cycling apps
   - Current position in rotation

4. Report all findings in a clear summary for the user."""


@mcp.prompt()
def moodlight_scene(scene_name: str) -> str:
    """
    Creates a prompt for setting mood lighting scenes.

    Use this to set predefined mood lighting ambiance.

    Args:
        scene_name: Scene preset - "calm" (blue), "energetic" (warm), "night" (dim red), "focus" (white)

    Returns:
        A prompt instructing how to set the mood lighting scene
    """
    scenes = {
        "calm": {
            "description": "Relaxing blue ambient lighting",
            "color": "#4488FF",
            "brightness": 100,
            "kelvin": 4000,
        },
        "energetic": {
            "description": "Warm, vibrant lighting",
            "color": "#FF8844",
            "brightness": 200,
            "kelvin": 5000,
        },
        "night": {
            "description": "Dim red for nighttime (won't disrupt sleep)",
            "color": "#FF2200",
            "brightness": 50,
            "kelvin": 2000,
        },
        "focus": {
            "description": "Bright white for concentration",
            "color": "#FFFFFF",
            "brightness": 180,
            "kelvin": 5500,
        },
    }

    if scene_name.lower() not in scenes:
        available = ", ".join(scenes.keys())
        return f"Unknown scene '{scene_name}'. Available scenes: {available}"

    scene = scenes[scene_name.lower()]

    return f"""Set mood lighting scene "{scene_name}" on the Ulanzi clock:

Scene: {scene["description"]}

1. Use set_moodlight with:
   - brightness: {scene["brightness"]}
   - color: "{scene["color"]}"
   - kelvin: {scene["kelvin"]}

2. For extra ambiance, show a custom app with the scene name

Current scene: {scene_name}
Brightness: {scene["brightness"]}/255
Color temperature: {scene["kelvin"]}K"""


@mcp.prompt()
def visual_weather(condition: str, temperature: int | None = None) -> str:
    """
    Creates a prompt for displaying weather information on the clock.

    Use this to show current weather conditions.

    Args:
        condition: Weather condition (sunny, cloudy, rainy, snowy, stormy, foggy)
        temperature: Optional temperature in Celsius

    Returns:
        A prompt instructing how to display weather information
    """
    condition_colors = {
        "sunny": "#FFDD00",
        "cloudy": "#888899",
        "rainy": "#4488FF",
        "snowy": "#FFFFFF",
        "stormy": "#666688",
        "foggy": "#AABBCC",
    }
    condition_icons = {
        "sunny": "sun",
        "cloudy": "cloud",
        "rainy": "rain",
        "snowy": "snow",
        "stormy": "storm",
        "foggy": "fog",
    }
    condition_sounds = {
        "sunny": "chime",
        "cloudy": None,
        "rainy": None,
        "snowy": None,
        "stormy": "thunder",
        "foggy": None,
    }

    color = condition_colors.get(condition.lower(), "#FFFFFF")
    icon = condition_icons.get(condition.lower(), "weather")
    sound = condition_sounds.get(condition.lower())

    temp_text = f"{temperature}°C" if temperature is not None else ""
    display_text = f"{condition.upper()}" + (f" {temp_text}" if temp_text else "")

    sound_line = f'\n2. Play ambient sound using play_sound("{sound}")' if sound else ""

    return f"""Display weather information on the Ulanzi clock:

1. Show custom app "weather":
   - app_name: "weather"
   - text: "{display_text}"
   - color: "{color}"
   - icon: "{icon}"
   - rainbow: False
   - duration: 10 seconds{sound_line}

2. Optionally use an appropriate background effect:
   - sunny: "sunrise"
   - rainy: "rain"
   - stormy: "lightning"
   - snowy: "snow"

Current weather: {condition}{f", {temperature}°C" if temperature else ""}"""


# =============================================================================
# Server Entry Point
# =============================================================================


def main():
    """Run the MCP server."""
    # Print configuration info
    hosts = settings.get_hosts_list()
    print("Starting Ulanzi MCP Server...")
    print(f"  Hosts: {hosts}")
    print(f"  MQTT Prefix: {settings.mqtt_prefix}")
    print(f"  Timeout: {settings.api_timeout}s")
    print(f"  Auth: {'Yes' if settings.username else 'No'}")
    print()

    # Run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
