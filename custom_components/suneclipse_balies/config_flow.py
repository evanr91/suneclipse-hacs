"""Config flow for SunEclipse Balies."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DEFAULT_NAME, DEFAULT_URL, DOMAIN


class SunEclipseBaliesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SunEclipse Balies."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()

            url = user_input["url"]
            session = async_get_clientsession(self.hass)
            try:
                async with session.get(url, timeout=10) as response:
                    response.raise_for_status()
                    payload = await response.json()
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                if not {"balies", "max-balies", "load"}.issubset(payload):
                    errors["base"] = "invalid_payload"
                else:
                    return self.async_create_entry(
                        title=user_input["name"],
                        data={"name": user_input["name"], "url": url},
                    )

        schema = vol.Schema(
            {
                vol.Required("name", default=DEFAULT_NAME): str,
                vol.Required("url", default=DEFAULT_URL): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
