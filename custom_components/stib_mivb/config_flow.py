import logging

from homeassistant import config_entries, exceptions
from homeassistant.core import callback

from . import InvalidAuth
from .const import *

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class StibMivbConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """STIB-MIVB config flow."""

    VERSION = 1

    def __init__(self):
        """Initialize the STIB config flow."""
        self.api_config = {}

    async def async_step_user(self, user_input=None):
        """
        Handle a Stib config flow start.
        """
        errors = {}

        if user_input is not None:
            _LOGGER.error("STIBu: " + str(user_input) +"--" + str(self.api_config) + " - " + str(STIB_API_ENTRY) + " -- " + str(errors))
            try:
                uid = f"{user_input[CONF_STOP_NAME]}[{user_input[CONF_MAIN_DIRECTION]}]"
                await self.async_set_unique_id(uid)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=uid, data=user_input)

            except InvalidAuth:
                errors["base"] = "faulty_credentials"

            except CannotConnect:
                errors["base"] = "device_unavailable"
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(STIB_API_ENTRY),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a option flow for tado."""

    def __init__(self, config_entry: config_entries.ConfigEntry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Handle options flow."""
        _LOGGER.error("STBI"+str(user_input))
        return await self.async_step_line_filter()

    async def async_step_line_filter(self, user_input=None):
        """Choose line filter."""
        _LOGGER.error("STBLF"+str(user_input))
        errors = {}

        if user_input is not None:
            lines_filter = [int(n) for n in user_input.get(CONF_MONITORED_LINES).split(",")]
            lines_filter.sort()
            self.config_entry.options[CONF_MONITORED_LINES] = lines_filter
            self.config_entry.options[CONF_MAX_PASSAGES] = user_input.get(CONF_MAX_PASSAGES)

        return self.async_show_form(
            step_id="line_filter",
            data_schema=vol.Schema(LINE_FILTERS_ENTRY),
            errors=errors,
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


