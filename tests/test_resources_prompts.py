"""Tests for MCP resources and prompts."""

import pytest
from unittest.mock import AsyncMock, patch

from ulanzi_mcp.server import (
    # Resources
    stats_resource,
    settings_resource,
    apps_resource,
    effects_resource,
    transitions_resource,
    # Prompts
    notify_urgent,
    notify_meeting,
    notify_timer,
    victory_alert,
    status_report,
    moodlight_scene,
    visual_weather,
)


class TestResources:
    """Test cases for MCP resources."""

    @pytest.mark.asyncio
    async def test_stats_resource_returns_json(self):
        """Verify stats resource returns valid JSON with expected fields."""
        mock_response = {"battery": 85, "ram": "45%", "uptime": 3600}

        with patch("ulanzi_mcp.server.get_client_for_request") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get_stats.return_value = mock_response
            mock_client.close.return_value = None
            mock_get_client.return_value = mock_client

            result = await stats_resource()
            parsed = __import__("json").loads(result)

        assert "battery" in parsed
        assert "ram" in parsed
        assert parsed["battery"] == 85

    @pytest.mark.asyncio
    async def test_stats_resource_uses_default_clock(self):
        """Verify stats resource uses default clock (None)."""
        with patch("ulanzi_mcp.server.get_client_for_request") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get_stats.return_value = {}
            mock_client.close.return_value = None
            mock_get_client.return_value = mock_client

            await stats_resource()

            mock_get_client.assert_called_once_with(None)

    @pytest.mark.asyncio
    async def test_settings_resource_returns_json(self):
        """Verify settings resource returns valid JSON."""
        mock_response = {"BRI": 200, "color": "FF0000"}

        with patch("ulanzi_mcp.server.get_client_for_request") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get_settings.return_value = mock_response
            mock_client.close.return_value = None
            mock_get_client.return_value = mock_client

            result = await settings_resource()
            parsed = __import__("json").loads(result)

        assert "BRI" in parsed
        assert parsed["BRI"] == 200

    @pytest.mark.asyncio
    async def test_apps_resource_returns_json(self):
        """Verify apps resource returns valid JSON."""
        mock_response = {"apps": ["Time", "Date", "Weather"]}

        with patch("ulanzi_mcp.server.get_client_for_request") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get_apps_in_loop.return_value = mock_response
            mock_client.close.return_value = None
            mock_get_client.return_value = mock_client

            result = await apps_resource()
            parsed = __import__("json").loads(result)

        assert "apps" in parsed
        assert "Time" in parsed["apps"]

    @pytest.mark.asyncio
    async def test_effects_resource_returns_json(self):
        """Verify effects resource returns valid JSON."""
        mock_response = {"effects": ["rainbow", "fire", "ocean"]}

        with patch("ulanzi_mcp.server.get_client_for_request") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get_effects.return_value = mock_response
            mock_client.close.return_value = None
            mock_get_client.return_value = mock_client

            result = await effects_resource()
            parsed = __import__("json").loads(result)

        assert "effects" in parsed

    @pytest.mark.asyncio
    async def test_transitions_resource_returns_json(self):
        """Verify transitions resource returns valid JSON."""
        mock_response = {"transitions": ["fade", "slide", "none"]}

        with patch("ulanzi_mcp.server.get_client_for_request") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get_transitions.return_value = mock_response
            mock_client.close.return_value = None
            mock_get_client.return_value = mock_client

            result = await transitions_resource()
            parsed = __import__("json").loads(result)

        assert "transitions" in parsed

    @pytest.mark.asyncio
    async def test_resource_closes_client(self):
        """Verify resources properly close the HTTP client."""
        with patch("ulanzi_mcp.server.get_client_for_request") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get_stats.return_value = {}
            mock_client.close.return_value = None
            mock_get_client.return_value = mock_client

            await stats_resource()

            mock_client.close.assert_called_once()


class TestPrompts:
    """Test cases for MCP prompts."""

    def test_notify_urgent_includes_text(self):
        """Verify urgent notification includes the urgent text."""
        prompt = notify_urgent("Emergency!", "Fire alarm")
        assert "Emergency!" in prompt
        assert "Fire alarm" in prompt

    def test_notify_urgent_suggests_hold(self):
        """Verify urgent notification suggests hold=True."""
        prompt = notify_urgent("Alert!", "Security")
        assert "hold: True" in prompt or "hold=True" in prompt

    def test_notify_urgent_suggests_alert_sound(self):
        """Verify urgent notification suggests playing a sound."""
        prompt = notify_urgent("Urgent!", "Test")
        assert "sound" in prompt.lower()

    def test_notify_meeting_includes_meeting_name(self):
        """Verify meeting notification includes meeting name."""
        prompt = notify_meeting("Team Standup", 15)
        assert "Team Standup" in prompt
        assert "15" in prompt

    def test_notify_meeting_urgency_timing(self):
        """Verify meeting notification reflects urgency based on timing."""
        # Very soon = orange color
        prompt_soon = notify_meeting("Urgent Meeting", 3)
        assert "#FF8800" in prompt_soon or "orange" in prompt_soon.lower()

        # Later = blue color
        prompt_later = notify_meeting("Later Meeting", 30)
        assert "#00AAFF" in prompt_later or "blue" in prompt_later.lower()

    def test_notify_timer_includes_label(self):
        """Verify timer notification includes label."""
        prompt = notify_timer("Pizza", 1200)
        assert "Pizza" in prompt
        assert "1200" in prompt

    def test_notify_timer_shows_formatted_time(self):
        """Verify timer notification shows formatted time."""
        prompt = notify_timer("Eggs", 180)
        assert "3:00" in prompt

    def test_victory_alert_contains_ff7_melody(self):
        """Verify victory alert contains FF7 victory RTTTL melody."""
        prompt = victory_alert()
        assert "FF7VICT" in prompt

    def test_victory_alert_with_custom_text(self):
        """Verify victory alert includes custom text when provided."""
        prompt = victory_alert(custom_text="You did it!")
        assert "You did it!" in prompt

    def test_victory_alert_mentions_rtttl(self):
        """Verify victory alert explains using RTTTL format."""
        prompt = victory_alert()
        assert "play_rtttl" in prompt.lower()

    def test_status_report_includes_checks(self):
        """Verify status report mentions all status checks."""
        prompt = status_report()
        assert "get_clock_stats" in prompt
        assert "get_clock_settings" in prompt
        assert "get_apps_in_loop" in prompt

    def test_status_report_with_clock_index(self):
        """Verify status report includes clock index when specified."""
        prompt = status_report(clock_index=2)
        assert "2" in prompt
        assert "clock index" in prompt.lower()

    def test_moodlight_scene_calm(self):
        """Verify calm moodlight scene has correct settings."""
        prompt = moodlight_scene("calm")
        assert "calm" in prompt.lower()
        assert "blue" in prompt.lower()
        assert "100" in prompt  # brightness

    def test_moodlight_scene_night(self):
        """Verify night moodlight scene has dim red settings."""
        prompt = moodlight_scene("night")
        assert "night" in prompt.lower()
        assert "50" in prompt  # low brightness

    def test_moodlight_scene_focus(self):
        """Verify focus moodlight scene has bright white settings."""
        prompt = moodlight_scene("focus")
        assert "focus" in prompt.lower()
        assert "180" in prompt  # medium-high brightness
        assert "5500" in prompt  # high kelvin

    def test_moodlight_scene_unknown_shows_available(self):
        """Verify unknown scene shows available options."""
        prompt = moodlight_scene("unknown_scene")
        assert "Available scenes" in prompt
        assert "calm" in prompt
        assert "energetic" in prompt

    def test_visual_weather_sunny(self):
        """Verify sunny weather prompt has yellow color."""
        prompt = visual_weather("sunny", 25)
        assert "sunny" in prompt.lower()
        assert "#FFDD00" in prompt or "yellow" in prompt.lower()

    def test_visual_weather_with_temperature(self):
        """Verify weather prompt includes temperature."""
        prompt = visual_weather("cloudy", temperature=18)
        assert "18" in prompt
        assert "°C" in prompt or "C" in prompt

    def test_visual_weather_without_temperature(self):
        """Verify weather prompt works without temperature."""
        prompt = visual_weather("rainy")
        assert "rainy" in prompt.lower()
        # Should not have temperature placeholder

    def test_visual_weather_icons(self):
        """Verify weather prompt includes icons."""
        prompt = visual_weather("sunny")
        assert "icon" in prompt.lower()

    def test_visual_weather_stormy_suggests_sound(self):
        """Verify stormy weather suggests thunder sound."""
        prompt = visual_weather("stormy")
        assert "thunder" in prompt.lower()
