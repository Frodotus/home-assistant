"""
Support for Tellstick switches using Tellstick Net.

This platform uses the Telldus Live online service.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/switch.tellduslive/

"""
import logging

from homeassistant.components import switch, tellduslive
from homeassistant.components.tellduslive.entry import TelldusLiveEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import ToggleEntity

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Old way of setting up TelldusLive.

    Can only be called when a user accidentally mentions the platform in their
    config. But even in that case it would have been ignored.
    """
    pass


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up tellduslive sensors dynamically."""
    async def async_discover_switch(device_id):
        """Discover and add a discovered sensor."""
        client = hass.data[tellduslive.DOMAIN]
        async_add_entities([TelldusLiveSwitch(client, device_id)])

    async_dispatcher_connect(
        hass,
        tellduslive.TELLDUS_DISCOVERY_NEW.format(switch.DOMAIN,
                                                 tellduslive.DOMAIN),
        async_discover_switch,
    )


class TelldusLiveSwitch(TelldusLiveEntity, ToggleEntity):
    """Representation of a Tellstick switch."""

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self.device.is_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self.device.turn_on()

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self.device.turn_off()