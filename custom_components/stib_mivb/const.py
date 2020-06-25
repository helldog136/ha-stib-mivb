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
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]


# Configuration and options
CONF_CLIENT_ID_KEY = 'client_id'
CONF_CLIENT_SECRET_KEY = 'client_secret'

CONF_ENABLED = "enabled"

CONF_SENSOR_UNAME = 'sensor_name'
CONF_STOPS = 'stops'
CONF_STOP_NAME = 'stop_name'
CONF_LANG = 'lang'
CONF_LINE_FILTER = 'line_filter'
CONF_LINE_NR = 'line_nr'
CONF_DESTINATION = 'destination'

CONF_MAX_PASSAGES = 'max_passages'
CONF_MAX_DELTA_ACTU = 'actualization_delta'

# platform schema
STIB_ENTRY_SCHEMA = vol.Schema({
    vol.Required(CONF_CLIENT_ID_KEY): str,
    vol.Required(CONF_CLIENT_SECRET_KEY): str,
    vol.Optional(CONF_LANG, default='fr', description={"suggested_value": "fr"}): str,

    vol.Required(CONF_STOP_NAME): str,
    vol.Optional(CONF_LINE_FILTER, default=[]): [
        {
            vol.Required(CONF_LINE_NR): int,
            vol.Required(CONF_DESTINATION): vol.In([str, 1, 2])
        }
    ],
    vol.Optional(CONF_MAX_PASSAGES, default=None): int
})


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


