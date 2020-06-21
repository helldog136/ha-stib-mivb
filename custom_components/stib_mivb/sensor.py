"""
Support for STIB/MVIB information.
For more info on the API see :
https://opendata.stib-mivb.be/
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.XXX --> to do
"""
import logging
import datetime
import time

from homeassistant.helpers.entity import Entity
from homeassistant.const import ATTR_ATTRIBUTION

from .const import ATTRIBUTION

REQUIREMENTS = ['pystibmivb==1.6.0']
SCAN_INTERVAL = datetime.timedelta(seconds=20)
_LOGGER = logging.getLogger(__name__)


class STIBMVIBPublicTransportSensor(Entity):
    def __init__(self, service, parameters):
        """Initialize the sensor."""
        self._is_init = False
        self._available = False
        self._assumed_state = False
        self.stib_service = service
        stop_name, lines_filter, max_passages, lang = parameters
        self._sensor_name = stop_name
        self.stop_name = stop_name
        self.lines_filter = lines_filter
        self.max_passages = max_passages
        self.lang = lang
        self.passages = {}
        self._name = stop_name
        self._attributes = {"stop_name": self._name,
                            ATTR_ATTRIBUTION: ATTRIBUTION}
        self._last_update = 0
        self._last_intermediate_update = 0
        self._state = None

    async def async_update(self):
        """Get the latest data from the STIB/MVIB API."""
        now = time.time()
        max_delta = 20
        if 'arriving_in_min' in self._attributes.keys() and 'arriving_in_sec' in self._attributes.keys():
            max_delta = min(max_delta,
                            (int(self._attributes['arriving_in_min']) * 60 + int(
                                self._attributes['arriving_in_sec'])) // 2)
        max_delta = max(max_delta, 10)
        delta = now - self._last_update
        if self._state is None \
                or delta > max_delta \
                or (self._state == 0 and delta > 10):  # Here we are making a reconciliation by calling STIB API
            try:
                self.passages = await self.stib_service.get_passages(stop_name=self.stop_name,
                                                                     line_filters=self.lines_filter,
                                                                     max_passages=self.max_passages,
                                                                     lang_stop_name=self.lang,
                                                                     lang_message=self.lang,
                                                                     now=datetime.datetime.now())
            except Exception as e:
                _LOGGER.error("Error while retrieving data from STIB. " + str(e))
                self._available = False
                return
            if self.passages is None:
                _LOGGER.error("No data recieved from STIB.")
                self._available = False
                return
            _LOGGER.info("Data recieved from STIB: " + str(self.passages))
            try:
                first = self.passages[0]
                self._state = int(first['arriving_in']['min'])
                self._attributes['destination'] = first['destination']
                self._attributes['expected_arrival_time'] = first['expected_arrival_time']
                self._attributes['stop_id'] = first['stop_id']
                self._attributes['message'] = first['message']
                self._attributes['arriving_in_min'] = int(first['arriving_in']['min'])
                self._attributes['arriving_in_sec'] = int(first['arriving_in']['sec'])
                self._attributes['line_id'] = first['line_id']
                self._attributes['line_type'] = first['line_type']
                self._attributes['line_color'] = first['line_color']
                self._attributes['next_passages'] = self.passages[1:]
                self._attributes['all_passages'] = self.passages
                self._last_update = now
                self._last_intermediate_update = now
                self._assumed_state = False
                self._is_init = True
                self._available = True
            except (KeyError, IndexError) as error:
                _LOGGER.error("Error getting data from STIB/MVIB, %s", error)
                self._available = False
        else:  # here we update logically the state and arrival in min. (this prevents too many calls to API)
            intermediate_delta = now - self._last_intermediate_update
            if intermediate_delta > 60:
                self._last_intermediate_update = now
                self._state = int(max(self._state - intermediate_delta // 60, 0))
                self._attributes['arriving_in_min'] = int(max(
                    self._attributes['arriving_in_min'] - intermediate_delta // 60, 0))
                self._assumed_state = True

    @property
    def is_init(self):
        return self._is_init

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        if 'line_type' in self._attributes.keys():
            if self._attributes['line_type'] == 'B':
                return 'mdi:bus'
            if self._attributes['line_type'] == 'M':
                return 'mdi:subway'
            if self._attributes['line_type'] == 'T':
                return 'mdi:tram'
        return 'mdi:bus'

    @property
    def available(self):
        """Return True if entity is available."""
        return self._available

    @property
    def unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        if self._state == 1:
            return "min"
        return "mins"

    @property
    def assumed_state(self):
        """Return True if the state is based on our assumption instead of reading it from the device."""
        return self._assumed_state

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._sensor_name

    @property
    def device_state_attributes(self):
        """Return attributes for the sensor."""
        return self._attributes

    @property
    def unique_id(self):
        return self.stop_name + "_" + str(hash(str(self.lines_filter)))
