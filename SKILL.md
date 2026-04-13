# Ulanzi MCP – Skill Guide

This file describes how to use `ulanzi-mcp` as a Python library, CLI tool, or MCP server skill.

---

## Installation

The package is split into modules with separate optional extras:

| Extra | Installs | Use when |
|-------|----------|----------|
| *(none)* | Core library only | Using `AwtrixClient` in Python code |
| `[mcp]` | + `mcp` | Running the MCP server |
| `[cli]` | + `typer`, `rich` | Using the `ulanzi` CLI |
| `[all]` | + all of the above | MCP server + CLI |
| `[dev]` | + all + test tools | Development / contributing |

```bash
# Core library only
pip install ulanzi-mcp

# MCP server
pip install "ulanzi-mcp[mcp]"

# CLI
pip install "ulanzi-mcp[cli]"

# Everything
pip install "ulanzi-mcp[all]"
```

---

## As an Importable Library

```python
from ulanzi_mcp import AwtrixClient, get_client, settings

# Direct client usage
client = AwtrixClient("http://192.168.1.100")
await client.show_notification("Hello!", color="#00FF00")
await client.close()

# Or use the helper that reads from environment / .env
client = get_client(index=0)   # index selects which clock (0-based)
stats = await client.get_stats()
await client.close()
```

### Public API

| Symbol | Description |
|--------|-------------|
| `AwtrixClient(host, timeout)` | Low-level async HTTP client for AWTRIX3 |
| `get_client(index=0)` | Factory that creates a client from configured hosts |
| `settings` | Pydantic-settings object (reads `ULANZI_*` env vars / `.env`) |
| `Settings` | Settings class for type hints / custom instantiation |

### AwtrixClient Methods

#### Status & Info
```python
await client.get_stats()           # battery, RAM, uptime
await client.get_settings()        # brightness, time format, etc.
await client.get_apps_in_loop()    # apps in display rotation
await client.get_effects()         # available visual effects
await client.get_transitions()     # available transition effects
```

#### Power & Display
```python
await client.set_power(True)       # turn matrix on/off
await client.set_sleep(seconds=60) # deep sleep
await client.reboot()              # reboot clock
await client.update_settings({"BRI": 200})  # set brightness 0-255
```

#### Navigation
```python
await client.switch_app("Time")    # switch to named app
await client.next_app()            # next app in loop
await client.previous_app()        # previous app in loop
```

#### Notifications & Custom Apps
```python
await client.show_notification(
    text="Meeting in 5 min!",
    duration=10,
    color="#FF8800",
    icon="clock",
    sound="alert",
    hold=True,
    wakeup=True,
)

await client.show_custom_app(
    app_name="my_app",
    text="Hello!",
    color="#00FF00",
    rainbow=False,
    effect="Fade",
    save=True,
)

await client.delete_custom_app("my_app")
await client.dismiss_notification()
```

#### Visual Effects
```python
await client.set_moodlight(brightness=100, color="#0055FF")  # RGB color
await client.set_moodlight(brightness=80, kelvin=3000)       # warm white by color temperature
await client.set_indicator(1, "#FF0000", blink=500)  # id 1-3
await client.clear_indicators()
```

#### Sound
```python
await client.play_sound("alert")       # play named melody from clock
await client.play_rtttl("FF7VICT:d=4,o=5,b=180:...")  # raw RTTTL
```

---

## CLI Usage

```bash
# Show configuration
ulanzi info

# Power / display
ulanzi power on
ulanzi brightness 200
ulanzi sleep 60
ulanzi reboot

# Navigation
ulanzi switch Time
ulanzi next
ulanzi prev

# Notifications
ulanzi notify "Hello!" --duration 10 --color "#00FF00"
ulanzi notify "Urgent!" --hold --wakeup --sound alert

# Custom apps
ulanzi custom my_app --text "Custom" --rainbow
ulanzi delete my_app
ulanzi dismiss

# Visual effects
ulanzi moodlight --brightness 100 --color "#0055FF"
ulanzi moodlight --brightness 80 --kelvin 3000
ulanzi indicator 1 --color "#FF0000" --blink 500
ulanzi clear-indicators

# Sound
ulanzi play alert
ulanzi rtttl "BirthdaySong:..."

# Info
ulanzi stats
ulanzi settings-cmd
ulanzi list-apps
ulanzi effects
```

All commands accept `--clock <index>` to target a specific clock (default: 0).

---

## MCP Server

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

## Configuration

Set these environment variables or put them in a `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `ULANZI_HOSTS` | Clock address(es), comma-separated | `192.168.1.100` |
| `ULANZI_USERNAME` | HTTP auth username | (none) |
| `ULANZI_PASSWORD` | HTTP auth password | (none) |
| `ULANZI_API_TIMEOUT` | Request timeout (seconds) | `10` |
| `ULANZI_MQTT_PREFIX` | MQTT topic prefix | `awtrix` |

### Multi-Clock Example

```env
ULANZI_HOSTS=192.168.1.100,192.168.1.101
```

```python
# Target the second clock
client = get_client(index=1)
await client.show_notification("Clock 2!")
await client.close()
```

---

## Quick Patterns

### Urgent Alert
```python
from ulanzi_mcp import get_client

async def urgent_alert(message: str):
    client = get_client()
    try:
        await client.show_notification(
            text=message,
            hold=True,
            wakeup=True,
            color="#FF0000",
            duration=10,
        )
        await client.play_sound("alert")
    finally:
        await client.close()
```

### Victory Celebration
```python
async def victory():
    client = get_client()
    try:
        ff7 = "FF7VICT:d=4,o=5,b=180:32p,c6,4a#,c6,4a#,c6,4d#6,2f6,2d#6,4c6,4a#,c6,4a#,c6,4a#,2a#,2g#,4g,4f,4a#,4c6,4d6,4d#6,4f6,4g6,4a6,4a#6,2c7"
        await client.play_rtttl(ff7)
        await client.show_custom_app("victory", text="You Win!", rainbow=True)
    finally:
        await client.close()
```

### Night Mode
```python
async def night_mode():
    client = get_client()
    try:
        await client.set_moodlight(brightness=50, color="#FF2200", kelvin=2000)
    finally:
        await client.close()
```
