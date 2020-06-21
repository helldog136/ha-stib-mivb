from homeassistant import config_entries, exceptions
from .const import *


@config_entries.HANDLERS.register(DOMAIN)
class StibMivbConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """STIB-MIVB config flow."""

    VERSION = 1

    def __init__(self):
        """Initialize the STIB config flow."""
        self.device_config = {}

    async def async_step_user(self, user_input=None):
        """
        Handle a Stib config flow start.
        """
        errors = {}

        if user_input is not None:
            try:
                this_uid = ""
                stop_name = user_input.get(CONF_STOP_NAME)
                this_uid += stop_name
                lines_filter_dict = user_input.get(CONF_LINE_FILTER)
                lines_filter = []
                for entry in lines_filter_dict:
                    filtr = (entry.get(CONF_LINE_NR), entry.get(CONF_DESTINATION))
                    lines_filter.append(filtr)
                lines_filter.sort(key=lambda e: str(e[0]) + str(e[1]))
                for filtr in lines_filter:
                    this_uid += "_" + str(filtr[0]) + "_" + str(filtr[1])

                max_passages = user_input.get(CONF_MAX_PASSAGES)

                await self.async_set_unique_id(this_uid)

                self._abort_if_unique_id_configured()

                self.device_config = {
                    CONF_CLIENT_ID_KEY: user_input[CONF_CLIENT_ID_KEY],
                    CONF_CLIENT_SECRET_KEY: user_input[CONF_CLIENT_SECRET_KEY],
                    CONF_LANG: user_input[CONF_LANG]
                }

                return self.async_create_entry(title=this_uid, data={
                                                        CONF_CLIENT_ID_KEY: user_input[CONF_CLIENT_ID_KEY],
                                                        CONF_CLIENT_SECRET_KEY: user_input[CONF_CLIENT_SECRET_KEY],
                                                        CONF_LANG: user_input[CONF_LANG],
                                                        "uid": this_uid,
                                                        "stop_name": stop_name,
                                                        "lines_filter": lines_filter,
                                                        "max_passages": max_passages
                                                    })

            except InvalidAuth:
                errors["base"] = "faulty_credentials"

            except CannotConnect:
                errors["base"] = "device_unavailable"

        return self.async_show_form(
            step_id="user",
            description_placeholders=self.device_config,
            data_schema=STIB_ENTRY_SCHEMA,
            errors=errors,
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


