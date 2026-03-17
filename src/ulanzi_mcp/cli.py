"""CLI interface for Ulanzi MCP."""

import asyncio

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from .client import get_client
from .config import settings

app = typer.Typer(
    help="""Ulanzi TC001 Smart Pixel Clock CLI

Environment Variables:
  ULANZI_HOSTS        Clock address(es), comma-separated (required)
                      Example: http://192.168.1.100 or http://192.168.1.100,http://192.168.1.101
  ULANZI_USERNAME     HTTP auth username (optional)
  ULANZI_PASSWORD     HTTP auth password (optional)
  ULANZI_API_TIMEOUT  HTTP request timeout in seconds (default: 10)
  ULANZI_MQTT_PREFIX  MQTT topic prefix (default: awtrix)

Example:
  export ULANZI_HOSTS=http://192.168.1.100
  export ULANZI_USERNAME=user
  export ULANZI_PASSWORD=secret
  ulanzi-mcp stats
"""
)
console = Console()


def get_clock_count() -> int:
    """Get number of configured clocks."""
    return len(settings.get_hosts_list())


@app.command()
def stats(clock: int = 0):
    """Get device statistics."""
    client = get_client(clock)
    try:
        result = asyncio.run(client.get_stats())
        console.print("[bold]Clock Statistics:[/bold]")
        for key, value in result.items():
            console.print(f"  {key}: {value}")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def settings_cmd(clock: int = 0):
    """Get current clock settings."""
    client = get_client(clock)
    try:
        result = asyncio.run(client.get_settings())
        console.print("[bold]Clock Settings:[/bold]")
        for key, value in result.items():
            console.print(f"  {key}: {value}")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def list_apps(clock: int = 0):
    """List apps in the display loop."""
    client = get_client(clock)
    try:
        result = asyncio.run(client.get_apps_in_loop())
        console.print("[bold]Apps in Loop:[/bold]")
        for app_name in result:
            console.print(f"  - {app_name}")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def effects(clock: int = 0):
    """List available visual effects."""
    client = get_client(clock)
    try:
        result = asyncio.run(client.get_effects())
        console.print("[bold]Available Effects:[/bold]")
        for effect in result:
            console.print(f"  - {effect}")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def power(on: bool = True, clock: int = 0):
    """Turn matrix on or off."""
    client = get_client(clock)
    try:
        result = asyncio.run(client.set_power(on))
        console.print(f"[green]Power {'on' if on else 'off'}![/green]")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def brightness(level: int = typer.Argument(..., min=0, max=255), clock: int = 0):
    """Set matrix brightness (0-255)."""
    client = get_client(clock)
    try:
        result = asyncio.run(client.update_settings({"BRI": level}))
        console.print(f"[green]Brightness set to {level}![/green]")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def sleep(seconds: int = typer.Argument(..., min=1), clock: int = 0):
    """Send clock to sleep for specified seconds."""
    client = get_client(clock)
    try:
        result = asyncio.run(client.set_sleep(seconds))
        console.print(f"[green]Sleeping for {seconds} seconds![/green]")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def reboot(clock: int = 0):
    """Reboot the clock."""
    client = get_client(clock)
    try:
        result = asyncio.run(client.reboot())
        console.print("[green]Rebooting![/green]")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def switch(app_name: str, clock: int = 0):
    """Switch to a specific app."""
    client = get_client(clock)
    try:
        result = asyncio.run(client.switch_app(app_name))
        console.print(f"[green]Switched to {app_name}![/green]")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def next(clock: int = 0):
    """Switch to next app."""
    client = get_client(clock)
    try:
        result = asyncio.run(client.next_app())
        console.print("[green]Next app![/green]")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def prev(clock: int = 0):
    """Switch to previous app."""
    client = get_client(clock)
    try:
        result = asyncio.run(client.previous_app())
        console.print("[green]Previous app![/green]")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def notify(
    text: str,
    duration: int = 5,
    color: str | None = None,
    icon: str | None = None,
    sound: str | None = None,
    hold: bool = False,
    wakeup: bool = False,
    clock: int = 0,
):
    """Display a notification."""
    client = get_client(clock)
    try:
        result = asyncio.run(
            client.show_notification(
                text=text,
                duration=duration,
                color=color,
                icon=icon,
                sound=sound,
                hold=hold,
                wakeup=wakeup,
            )
        )
        console.print(f"[green]Notification: {text}[/green]")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def custom(
    app_name: str,
    text: str | None = None,
    duration: int = 5,
    color: str | None = None,
    background: str | None = None,
    icon: str | None = None,
    rainbow: bool = False,
    effect: str | None = None,
    save: bool = False,
    clock: int = 0,
):
    """Create or update a custom app."""
    client = get_client(clock)
    try:
        result = asyncio.run(
            client.show_custom_app(
                app_name=app_name,
                text=text,
                duration=duration,
                color=color,
                background=background,
                icon=icon,
                rainbow=rainbow,
                effect=effect,
                save=save,
            )
        )
        console.print(f"[green]Custom app '{app_name}' updated![/green]")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def delete(app_name: str, clock: int = 0):
    """Delete a custom app."""
    client = get_client(clock)
    try:
        result = asyncio.run(client.delete_custom_app(app_name))
        console.print(f"[green]Deleted app '{app_name}'![/green]")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def dismiss(clock: int = 0):
    """Dismiss a held notification."""
    client = get_client(clock)
    try:
        result = asyncio.run(client.dismiss_notification())
        console.print("[green]Notification dismissed![/green]")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def moodlight(
    brightness: int = 170,
    color: str | None = None,
    kelvin: int | None = None,
    clock: int = 0,
):
    """Set mood lighting."""
    client = get_client(clock)
    try:
        result = asyncio.run(
            client.set_moodlight(
                brightness=brightness,
                color=color,
                kelvin=kelvin,
            )
        )
        console.print("[green]Moodlight set![/green]")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def indicator(
    id: int = typer.Argument(..., min=1, max=3),
    color: str = "#FF0000",
    blink: int | None = None,
    fade: int | None = None,
    clock: int = 0,
):
    """Set a colored indicator (1-3)."""
    client = get_client(clock)
    try:
        result = asyncio.run(
            client.set_indicator(
                indicator_id=id,
                color=color,
                blink=blink,
                fade=fade,
            )
        )
        console.print(f"[green]Indicator {id} set to {color}![/green]")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def clear_indicators(clock: int = 0):
    """Clear all indicators."""
    client = get_client(clock)
    try:
        result = asyncio.run(client.clear_indicators())
        console.print("[green]Indicators cleared![/green]")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def play(sound: str, clock: int = 0):
    """Play a RTTTL melody."""
    client = get_client(clock)
    try:
        result = asyncio.run(client.play_sound(sound))
        console.print(f"[green]Playing {sound}![/green]")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def rtttl(rtttl_string: str, clock: int = 0):
    """Play a RTTTL melody string."""
    client = get_client(clock)
    try:
        result = asyncio.run(client.play_rtttl(rtttl_string))
        console.print("[green]Playing RTTTL![/green]")
    except Exception as e:
        rprint(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        asyncio.run(client.close())


@app.command()
def info():
    """Show configuration info."""
    hosts = settings.get_hosts_list()
    table = Table(title="Ulanzi MCP Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Hosts", ", ".join(hosts))
    table.add_row("Count", str(len(hosts)))
    table.add_row("MQTT Prefix", settings.mqtt_prefix)
    table.add_row("Timeout", f"{settings.api_timeout}s")
    table.add_row("Auth", "Yes" if settings.username else "No")

    console.print(table)

    # Also show env var reference
    env_table = Table(title="Environment Variables")
    env_table.add_column("Variable", style="cyan")
    env_table.add_column("Description", style="white")
    env_table.add_column("Current", style="yellow")

    env_table.add_row("ULANZI_HOSTS", "Clock address(es)", settings.hosts)
    env_table.add_row("ULANZI_USERNAME", "HTTP auth user", settings.username or "(not set)")
    env_table.add_row(
        "ULANZI_PASSWORD", "HTTP auth pass", "***" if settings.password else "(not set)"
    )
    env_table.add_row("ULANZI_API_TIMEOUT", "Request timeout", str(settings.api_timeout))
    env_table.add_row("ULANZI_MQTT_PREFIX", "MQTT prefix", settings.mqtt_prefix)

    console.print(env_table)


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
