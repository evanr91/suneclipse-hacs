"""Data coordinator for SunEclipse Balies."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import logging
from typing import Any

from aiohttp import ClientError

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import SCAN_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class SunEclipseData:
    """Normalized payload from the SunEclipse endpoint."""

    balies: int
    max_balies: int
    load: float


class SunEclipseCoordinator(DataUpdateCoordinator[SunEclipseData]):
    """Class to manage fetching SunEclipse data."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize coordinator."""
        self.config_entry = entry
        self._url: str = entry.data["url"]
        super().__init__(
            hass,
            logger=_LOGGER,
            name=entry.title,
            update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
        )

    async def _async_update_data(self) -> SunEclipseData:
        """Fetch data from endpoint."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(self._url, timeout=10) as response:
                response.raise_for_status()
                payload: dict[str, Any] = await response.json()
        except (ClientError, TimeoutError, ValueError) as err:
            raise UpdateFailed(f"Error requesting {self._url}: {err}") from err

        try:
            return SunEclipseData(
                balies=int(payload["balies"]),
                max_balies=int(payload["max-balies"]),
                load=float(payload["load"]),
            )
        except (KeyError, TypeError, ValueError) as err:
            raise UpdateFailed(f"Invalid payload from {self._url}: {err}") from err
