"""Ulanzi MCP - MCP Server and CLI for Ulanzi TC001 Smart Pixel Clock."""

from .client import AwtrixClient, get_client
from .config import Settings, settings

__version__ = "0.1.0"
__all__ = [
    "AwtrixClient",
    "get_client",
    "Settings",
    "settings",
    "__version__",
]
