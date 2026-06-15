"""Sensor platform for SunEclipse Balies."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SunEclipseCoordinator


@dataclass(frozen=True, kw_only=True)
class SunEclipseSensorEntityDescription(SensorEntityDescription):
    """Describes SunEclipse sensor entity."""

    value_key: str


SENSOR_DESCRIPTIONS: tuple[SunEclipseSensorEntityDescription, ...] = (
    SunEclipseSensorEntityDescription(
        key="balies",
        name="Balies",
        icon="mdi:counter",
        value_key="balies",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SunEclipseSensorEntityDescription(
        key="max_balies",
        name="Max Balies",
        icon="mdi:counter",
        value_key="max_balies",
    ),
    SunEclipseSensorEntityDescription(
        key="load",
        name="Load",
        icon="mdi:speedometer",
        value_key="load",
        suggested_display_precision=2,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SunEclipse sensors from config entry."""
    coordinator: SunEclipseCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[SensorEntity] = [
        SunEclipseSensor(coordinator, entry, description) for description in SENSOR_DESCRIPTIONS
    ]
    entities.append(SunEclipseSummarySensor(coordinator, entry))
    async_add_entities(entities)


class SunEclipseSensor(CoordinatorEntity[SunEclipseCoordinator], SensorEntity):
    """Representation of a SunEclipse metric sensor."""

    entity_description: SunEclipseSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SunEclipseCoordinator,
        entry: ConfigEntry,
        description: SunEclipseSensorEntityDescription,
    ) -> None:
        """Initialize sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.title,
            "manufacturer": "SunEclipse",
            "model": "balies.json",
        }

    @property
    def native_value(self) -> Any:
        """Return sensor value."""
        return getattr(self.coordinator.data, self.entity_description.value_key)


class SunEclipseSummarySensor(CoordinatorEntity[SunEclipseCoordinator], SensorEntity):
    """Single-line summary sensor."""

    _attr_name = "Status"
    _attr_has_entity_name = True
    _attr_icon = "mdi:chart-line"
    _attr_should_poll = False

    def __init__(self, coordinator: SunEclipseCoordinator, entry: ConfigEntry) -> None:
        """Initialize summary sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_status"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.title,
            "manufacturer": "SunEclipse",
            "model": "balies.json",
        }

    @property
    def native_value(self) -> str:
        """Return summary value."""
        data = self.coordinator.data
        return f"{data.balies}/{data.max_balies} - {data.load:.2f}"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose summary details as attributes."""
        data = self.coordinator.data
        return {
            "balies": data.balies,
            "max_balies": data.max_balies,
            "load": round(data.load, 2),
        }
