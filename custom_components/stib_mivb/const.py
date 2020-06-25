"""Constants for blueprint."""
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

# Base component constants
NAME = "STIB-MIVB"
DOMAIN = 'stib_mivb'
DOMAIN_DATA = f"{DOMAIN}_data"
ATTRIBUTION = "Data provided by opendata.stib-mivb.be"
VERSION = "1.0.0"

ISSUE_URL = "https://github.com/helldog136/ha-stib-mivb/issues"

# Icons
ICON_BUS = "mdi:bus"
ICON_METRO = 'mdi:subway'
ICON_TRAM = 'mdi:tram'

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Configuration and options
CONF_CLIENT_ID_KEY = 'client_id'
CONF_CLIENT_SECRET_KEY = 'client_secret'

CONF_ENABLED = "enabled"

CONF_SENSOR_UNAME = 'sensor_name'
CONF_STOP_NAME = 'stop_name'
CONF_LANG = 'lang'
CONF_MONITORED_LINES = 'monitored_lines'
CONF_DESTINATION = 'destination'
CONF_MAIN_DIRECTION = 'main_direction'

CONF_MAX_PASSAGES = 'max_passages'
CONF_MAX_DELTA_ACTU = 'actualization_delta'

# platform schema
LINE_FILTERS_ENTRY = {
    vol.Optional(CONF_MONITORED_LINES, default=None, description={"description": "comma separated numbers of lines. Ex: 3, 81"}): str,
    vol.Optional(CONF_MAX_PASSAGES, default=None, description={"description": "max passages for sensor"}): int
}

STIB_API_ENTRY = {
    vol.Required(CONF_CLIENT_ID_KEY, description={"description": "<your STIB/MIVB opendata client_id>"}): str,
    vol.Required(CONF_CLIENT_SECRET_KEY, description={"description": "<your STIB/MIVB opendata client_secret>"}): str,
    vol.Optional(CONF_LANG, default='fr', description={"description": "fr/nl"}): str,

    vol.Required(CONF_STOP_NAME, description={"description": "stop to monitor"}): str,
    vol.Required(CONF_MAIN_DIRECTION, description={"description": "direction of passages (1 or 2)"}): vol.In(1, 2)
}

# Defaults
DEFAULT_NAME = DOMAIN

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
