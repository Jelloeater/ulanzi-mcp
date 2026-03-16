# Ulanzi MCP Server - Specification

## Project Overview

**Project Name:** Ulanzi MCP Server  
**Type:** Model Context Protocol (MCP) Server + CLI Tool  
**Core Functionality:** Allows AI assistants (Claude Desktop, Cursor, Windsurf, etc.) to control the Ulanzi TC001 Smart Pixel Clock via the AWTRIX 3 firmware HTTP API. Includes a CLI for direct command-line usage.  
**Target Users:** Developers and AI enthusiasts who want to integrate their Ulanzi pixel clock with AI assistants or run automations via CLI.

---

## Problem Statement

The Ulanzi TC001 Smart Pixel Clock runs AWTRIX 3 firmware with a powerful HTTP API, but there's no standardized way for AI assistants to interact with it. This MCP server bridges that gap, enabling natural language control of the clock.

---

## Technical Architecture

### Tech Stack
- **Language:** Python 3.11+
- **MCP Framework:** `mcp` Python SDK with `FastMCP`
- **HTTP Client:** `httpx` (async HTTP)
- **Configuration:** `pydantic-settings` for env config
- **CLI:** `typer` for CLI interface
- **Testing:** `pytest` + `pytest-asyncio`

### MCP Server Design
```
┌─────────────────┐      stdio       ┌──────────────────┐
│   AI Assistant  │ ◄──────────────► │   Ulanzi MCP    │
│  (Claude/Cursor)│                  │     Server      │
└─────────────────┘                  └────────┬─────────┘
                                               │
                                               ▼
                                      ┌──────────────────┐
                                      │  AWTRIX 3 Clock  │
                                      │  (HTTP API)      │
                                      └──────────────────┘
```

### Transport
- **Primary:** stdio (standard for MCP)
- **Dev Mode:** `mcp dev src/ulanzi_mcp/server.py` for testing

### CLI Mode
- Standalone CLI tool for non-MCP usage
- Commands mirror MCP tools
- Useful for scripting and automation

---

## Configuration

### Environment Variables

```env
# Required - One or more clocks (comma-separated for multiple)
ULANZI_HOSTS=http://192.168.1.100
# Example multiple: ULANZI_HOSTS=http://192.168.1.100,http://192.168.1.101,http://192.168.1.102

# Optional - Auth (applied to all clocks)
ULANZI_USERNAME=admin
ULANZI_PASSWORD=secret

# Optional
ULANZI_API_TIMEOUT=10              # HTTP request timeout (seconds)
ULANZI_MQTT_PREFIX=awtrix          # MQTT topic prefix
```

### Multi-Clock Support

When multiple clocks are configured (`ULANZI_HOSTS` with comma-separated values), tools accept an optional `clock_index` parameter (0-based) to target specific clocks. Default: index 0.

---

## MCP Tools

### Status & Info Tools

| Tool Name | Description |
|-----------|-------------|
| `get_clock_stats` | Get device statistics (battery, RAM, uptime) |
| `get_clock_settings` | Retrieve current clock settings |
| `get_apps_in_loop` | List all apps in the display rotation |
| `get_available_effects` | List all available visual effects |

### Power Control Tools

| Tool Name | Description |
|-----------|-------------|
| `set_power` | Turn matrix on/off |
| `set_brightness` | Set matrix brightness (0-255) |
| `set_sleep` | Send clock to deep sleep |
| `reboot_clock` | Reboot the clock |
| `switch_to_app` | Switch to specific app |
| `next_app` | Go to next app in loop |
| `previous_app` | Go to previous app in loop |

### Custom App & Notification Tools

| Tool Name | Description |
|-----------|-------------|
| `show_notification` | Display a notification |
| `show_custom_app` | Create/update a custom app |
| `delete_custom_app` | Remove a custom app |
| `dismiss_notification` | Dismiss held notification |

### Visual Effects Tools

| Tool Name | Description |
|-----------|-------------|
| `set_moodlight` | Set mood lighting |
| `set_indicator` | Set colored indicator (1-3) |
| `clear_indicators` | Clear all indicators |

### Sound Tools

| Tool Name | Description |
|-----------|-------------|
| `play_sound` | Play a RTTTL melody |
| `play_rtttl` | Play RTTTL string |

---

## CLI Commands

All MCP tools have corresponding CLI commands:

```bash
# Status
ulanzi stats                    # Get device statistics
ulanzi settings-cmd             # Get current settings
ulanzi list-apps                  # List apps in loop
ulanzi effects                  # List available effects

# Power & Display
ulanzi power on                 # Turn on
ulanzi power off                # Turn off
ulanzi brightness 200           # Set brightness
ulanzi sleep 3600               # Sleep for 1 hour
ulanzi reboot                   # Reboot clock

# Navigation
ulanzi switch Time              # Switch to app
ulanzi next                     # Next app
ulanzi prev                     # Previous app

# Notifications
ulanzi notify "Hello!"           # Show notification
ulanzi custom myapp -t "Text"   # Create custom app
ulanzi delete myapp             # Delete custom app
ulanzi dismiss                  # Dismiss notification

# Effects
ulanzi moodlight -b 170         # Set moodlight
ulanzi indicator 1 "#FF0000"    # Set indicator
ulanzi clear-indicators         # Clear all

# Sound
ulanzi play alarm               # Play sound
ulanzi rtttl ":d=4,o=5,b=180:"  # Play RTTTL string

# Info
ulanzi info                     # Show configuration
```

---

## Project Structure

```
ulanzi-mcp/
├── pyproject.toml              # Project configuration
├── .env.example                # Example environment file
├── README.md                   # Project readme
├── src/
│   └── ulanzi_mcp/
│       ├── __init__.py         # Package init
│       ├── config.py           # Pydantic settings
│       ├── client.py           # AWTRIX3 HTTP client
│       ├── server.py           # FastMCP server
│       └── cli.py              # CLI interface
└── tests/                      # Test directory
```

---

## Running the Server

### MCP Server (for AI assistants)

```bash
# Development mode (with inspector)
uv run mcp dev src/ulanzi_mcp/server.py

# Or run directly
uv run python -m ulanzi_mcp.server
```

### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

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

### CLI Usage

```bash
# Show configuration
ulanzi info

# Turn on the display
ulanzi power on

# Show a notification
ulanzi notify "Meeting in 5 minutes!"

# Set brightness
ulanzi brightness 200
```

---

## Implementation Status

- [x] Project setup with pyproject.toml
- [x] Configuration management (env vars, multi-clock)
- [x] AWTRIX3 HTTP client
- [x] MCP server with all tools
- [x] CLI with all commands

---

## References

- AWTRIX3 API: https://blueforcer.github.io/awtrix3/#/api
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk
- Ulanzi TC001: https://www.ulanzi.com/products/ulanzi-pixel-smart-clock-2882
