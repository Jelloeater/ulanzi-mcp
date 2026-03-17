"""Configuration management for Ulanzi MCP."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="ULANZI_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Required
    hosts: str = Field(
        default="192.168.1.100",
        description="One or more clock addresses (comma-separated, no http:// needed)",
    )

    # Optional: Auth
    username: str | None = Field(default=None, description="HTTP auth username")
    password: str | None = Field(default=None, description="HTTP auth password")

    # Optional: API settings
    api_timeout: int = Field(default=10, description="HTTP request timeout (seconds)")
    mqtt_prefix: str = Field(default="awtrix", description="MQTT topic prefix")

    def get_hosts_list(self) -> list[str]:
        """Parse hosts string into a list of addresses (with http:// prefix)."""
        result = []
        for h in self.hosts.split(","):
            h = h.strip()
            if h:
                if not h.startswith("http://") and not h.startswith("https://"):
                    h = f"http://{h}"
                result.append(h)
        return result

    def get_host(self, index: int = 0) -> str:
        """Get host by index."""
        hosts = self.get_hosts_list()
        if index < 0 or index >= len(hosts):
            raise IndexError(f"Clock index {index} out of range (have {len(hosts)} clocks)")
        return hosts[index]


# Global settings instance
settings = Settings()
