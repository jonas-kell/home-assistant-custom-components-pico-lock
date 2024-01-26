"""Platform for lock integration."""
from __future__ import annotations

import logging
import voluptuous as vol
from typing import Final, Any
import homeassistant.helpers.config_validation as cv
from homeassistant.components.lock import (
    PLATFORM_SCHEMA,
    LockEntity,
)
from homeassistant.const import CONF_IP_ADDRESS, CONF_NAME, CONF_DEVICES
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback, PlatformNotReady
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

import requests

_LOGGER = logging.getLogger(__name__)

DOMAIN: Final = "pico_lock"

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_DEVICES, default={}): vol.Schema(
            {
                cv.string: {
                    vol.Required(CONF_NAME): cv.string,
                    vol.Required(CONF_IP_ADDRESS): cv.string,
                }
            }
        ),
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    # Assign configuration variables.
    # The configuration check takes care they are present.

    devices = []
    for unique_id, device_config in config[CONF_DEVICES].items():
        name = device_config[CONF_NAME]
        ip_address = device_config[CONF_IP_ADDRESS]

        pico = RaspberryPiPico(
            unique_id, name, ip_address
        )

        # Verify that passed in configuration works
        if not pico.assert_can_connect():
            raise PlatformNotReady(f"Could not connect to RaspberryPi Pico with custom firmware (ip: {ip_address})")
        
        _LOGGER.info(f"appended device")

        # append to devices array
        devices.append(pico)

    _LOGGER.info(f"#devices {len(devices)}")

    # Add devices
    add_entities(PicoLock(pico) for pico in devices)


class RaspberryPiPico:
    """Controls Connection to a RaspberriPi Pico with custom firmware"""

    def __init__(
        self, unique_id, name, ip_address
    ) -> None:
        self._unique_id = unique_id
        self._name = name
        self._ip_address = ip_address

    def assert_can_connect(self) -> bool:
        ok, response = self.request("check_connect", {}, "get", False)

        if ok:
            _LOGGER.info(f"Asserted that Pico can connect")
            return True

        return False

    def unlock(self):
        ok, response = self.request(
            "open",
            {},
            "post",
        )

        if ok:
            _LOGGER.info(f"Lock opened")
            return True

        return False

    def request(self, route, params={}, method="get", log_connection_error=True):
        try:
            if method == "get":
                r = requests.get(
                    url=f"http://{self._ip_address}/{route}",
                    params=params,
                )
            elif method == "post":
                r = requests.post(
                    url=f"http://{self._ip_address}/{route}",
                    params=params,
                )
            else:
                raise ValueError
        except Exception as ex:
            if log_connection_error:
                _LOGGER.error(
                    f"Could not connect to RaspberryPi Pico with custom firmware on ip {self._ip_address} due to exception {type(ex).__name__}, {str(ex.args)}"
                )
            return False, {}

        if r.status_code != 200:
            _LOGGER.error(
                f"Could connect Pico to with custom firmware but returned status code {r.status_code}"
            )
            return False, {}

        try:
            response = r.json()
            status = response["status"]
        except:
            _LOGGER.error(
                f"Pico response no valid json or has the 'status' field not set: {r.text}"
            )
            return False, {}

        if status != "success":
            _LOGGER.error(f"Pico returned internal status: {str(response)}")
            return False, {}

        _LOGGER.info(f"Response from PI {self._ip_address}: {str(response)}")
        return True, response


class PicoLock(LockEntity):
    """Control Representation of a Lock"""

    _attr_code_format = None
    _attr_changed_by = "Default trigger"

    def __init__(self, pico: RaspberryPiPico) -> None:
        self._pico = pico
        self._attr_unique_id = pico._unique_id
        self._name = pico._name

    @property
    def name(self) -> str:
        """Return the display name of this lock."""
        return self._name

    @property
    def is_locked(self):
        """Return the state of the lock"""
        return True

    def unlock(self, **kwargs: Any) -> None:
        """Unlock specified lock."""
        self._pico.unlock()