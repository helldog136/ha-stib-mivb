"""STIB/MIVB Sensor for home assistant"""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady, PlatformNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant import exceptions

from pystibmivb import STIBAPIClient, STIBService

from custom_components.stib_mivb.const import *
from custom_components.stib_mivb.sensor import STIBMVIBPublicTransportSensor

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI.
    entry has the following data:
    {
        CONF_CLIENT_ID_KEY: user_input[CONF_CLIENT_ID_KEY],
        CONF_CLIENT_SECRET_KEY: user_input[CONF_CLIENT_SECRET_KEY],
        CONF_LANG: user_input[CONF_LANG],
        "uid": this_uid,
        "stop_name": stop_name,
        "lines_filter": lines_filter,
        "max_passages": max_passages
    }
    """
    if hass.data.get(DOMAIN) is None or hass.data.get(DOMAIN).get("service") is None:
        client_id = entry.data.get(CONF_CLIENT_ID_KEY)
        client_secret = entry.data.get(CONF_CLIENT_SECRET_KEY)
        session = async_get_clientsession(hass)
        client = STIBAPIClient(loop=hass.loop,
                               session=session,
                               client_id=client_id,
                               client_secret=client_secret)
        if await client.async_get_access_token() is None:
            raise InvalidAuth
        service = STIBService(client)
        hass.data.setdefault(DOMAIN, {"service": service})
        _LOGGER.info(STARTUP_MESSAGE)

    service = hass.data.get(DOMAIN).get("service")

    sensor = STIBMVIBPublicTransportSensor(service=service, parameters=(
    entry.data.get("stop_name"), entry.data.get("lines_filter"), entry.data.get("max_passages"),
    entry.data.get(CONF_LANG), entry.data.get(CONF_LANG)))

    if not sensor.is_init:
        raise PlatformNotReady

    hass.data[DOMAIN][entry.data["uid"]] = sensor

    entry.add_update_listener(async_reload_entry)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Handle removal of an entry."""
    hass.data[DOMAIN].pop(entry.data["uid"])
    # TODO delete all config if no more entries?
    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
