# Agent Guide for ulanzi-mcp

This document helps AI agents understand how to interact with the Ulanzi MCP server.

## Quick Reference

### Connection
```json
{
  "mcpServers": {
    "ulanzi-mcp": {
      "command": "uv",
      "args": ["--directory", "/path/to/ulanzi-mcp", "run", "python", "-m", "ulanzi_mcp.server"]
    }
  }
}
```

---

## MCP Components

### Tools (Actions)
Tools perform actions on the clock.

#### Status & Info
- `get_clock_stats` - Battery, RAM, uptime
- `get_clock_settings` - Brightness, time format, etc.
- `get_apps_in_loop` - Apps in display rotation
- `get_available_effects` - Available visual effects

#### Power & Display
- `set_power(power: bool)` - Turn on/off
- `set_brightness(brightness: 0-255)` - Set brightness
- `set_sleep(seconds: int)` - Deep sleep mode
- `reboot_clock()` - Reboot

#### Navigation
- `switch_to_app(app_name: str)` - Switch to specific app
- `next_app()` / `previous_app()` - Navigate loop

#### Notifications & Custom Apps
- `show_notification(text, duration, color, icon, sound, hold, wakeup, stack)`
- `show_custom_app(app_name, text, duration, repeat, color, background, icon, rainbow, effect, save)`
- `delete_custom_app(app_name)`
- `dismiss_notification()`

#### Visual Effects
- `set_moodlight(brightness, color, kelvin)`
- `set_indicator(indicator_id: 1-3, color, blink, fade)`
- `clear_indicators()`

#### Sound
- `play_sound(sound: str)` - Play from MELODIES folder
- `play_rtttl(rtttl: str)` - Play RTTTL melody string

### Resources (Data)
Resources provide read-only data for agents to ingest.

| URI | Description |
|-----|-------------|
| `ulanzi://stats` | Device statistics |
| `ulanzi://settings` | Current settings |
| `ulanzi://apps` | Apps in loop |
| `ulanzi://effects` | Available effects |
| `ulanzi://transitions` | Transition effects |

### Prompts (Templates)
Prompts are reusable templates for common workflows.

| Prompt | Parameters | Description |
|--------|-----------|-------------|
| `notify_urgent` | `text`, `reason` | Critical alerts with hold + sound |
| `notify_meeting` | `meeting_name`, `minutes_until` | Meeting reminders |
| `notify_timer` | `label`, `duration_seconds` | Countdown timers |
| `victory_alert` | `custom_text?` | FF7 victory jingle! |
| `status_report` | `clock_index?` | Full status check |
| `moodlight_scene` | `scene_name` | Preset lighting (calm/energetic/night/focus) |
| `visual_weather` | `condition`, `temperature?` | Weather display |

---

## Multi-Clock Support

Most tools accept optional `clock_index: int` (0-based) to target specific clocks.

```python
# Target second clock (index 1)
await switch_to_app("Time", clock_index=1)
```

---

## Common Patterns

### Urgent Alert
```python
await show_notification(
    text="Emergency!",
    hold=True,
    wakeup=True,
    color="#FF0000",
    duration=10
)
await play_sound("alert")
```

### Victory Celebration (FF7!)
```python
victory_rtttl = "FF7VICT:d=4,o=5,b=180:32p,c6,4a#,c6,4a#,c6,4d#6,2f6,..."
await play_rtttl(victory_rtttl)
await show_custom_app("victory", text="You Win!", rainbow=True)
```

### Mood Lighting Scene
```python
# Night mode (dim red)
await set_moodlight(brightness=50, color="#FF2200", kelvin=2000)
```

---

## Notes

- Default clock: index 0 (first configured host)
- Brightness range: 0-255
- Colors: hex strings like "#FF0000" or RGB arrays
- RTTTL melodies can be played with `play_rtttl()`
