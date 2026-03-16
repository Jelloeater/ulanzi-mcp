# Ulanzi MCP Server

MCP server and CLI for the Ulanzi TC001 Smart Pixel Clock (AWTRIX3 firmware).

## Features

- **MCP Server**: Control your Ulanzi clock from AI assistants (Claude Desktop, Cursor, Windsurf)
- **CLI Tool**: Command-line interface for scripting and automation
- **Multi-clock Support**: Control multiple clocks from a single instance
- **Full API Coverage**: Access all AWTRIX3 HTTP API endpoints

## Quick Start

### 1. Install

```bash
cd ulanzi-mcp
uv sync
```

### 2. Configure

Copy `.env.example` to `.env` and set your clock IP:

```env
ULANZI_HOSTS=http://192.168.1.100
```

For multiple clocks:
```env
ULANZI_HOSTS=http://192.168.1.100,http://192.168.1.101
```

### 3. Use CLI

```bash
# Check configuration
ulanzi info

# Turn on display
ulanzi power on

# Show notification
ulanzi notify "Meeting in 5 minutes!"

# Set brightness
ulanzi brightness 200
```

### 4. Use with MCP (Claude Desktop)

Add to your Claude Desktop config:

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

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ULANZI_HOSTS` | Clock address(es), comma-separated | `http://192.168.1.100` |
| `ULANZI_USERNAME` | HTTP auth username | (none) |
| `ULANZI_PASSWORD` | HTTP auth password | (none) |
| `ULANZI_API_TIMEOUT` | Request timeout (seconds) | `10` |
| `ULANZI_MQTT_PREFIX` | MQTT topic prefix | `awtrix` |

## Available Tools/Commands

See [docs/clock_spec.md](docs/clock_spec.md) for complete documentation.

## Development

```bash
# Run MCP server in development mode
uv run mcp dev src/ulanzi_mcp/server.py

# Run CLI
ulanzi --help

# Run tests
uv run pytest
```

## License

MIT
