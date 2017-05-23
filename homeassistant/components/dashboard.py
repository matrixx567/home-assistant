"""
Event parser and human readable log generator.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/logbook/
"""
import asyncio
import logging
from datetime import timedelta
from itertools import groupby
import os

import voluptuous as vol

from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.components.frontend import register_built_in_panel
from homeassistant.const import (EVENT_HOMEASSISTANT_START, CONF_NAME, CONF_ICON,
                                 EVENT_HOMEASSISTANT_STOP, EVENT_STATE_CHANGED,
                                 STATE_NOT_HOME, STATE_OFF, STATE_ON,
                                 ATTR_HIDDEN, HTTP_BAD_REQUEST)

DOMAIN = "dashboard"
DEPENDENCIES = ['frontend']

_LOGGER = logging.getLogger(__name__)

CONF_IMAGE = 'image'

BOARD_SCHEMA = vol.Schema({
    vol.Required(CONF_IMAGE):  cv.string,
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_ICON): cv.icon,
 }, extra=vol.ALLOW_EXTRA)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: cv.ordered_dict(BOARD_SCHEMA)
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Listen for download events to download files."""

    local = hass.config.path('www')
    panel_config = config.get(DOMAIN,{})

    list_config = []
    for board, board_cfg in panel_config.items():
        board_cfg["id"] = board
        svg_file = os.path.join(local, board_cfg[CONF_IMAGE])
        if not os.path.isfile(svg_file):
            _LOGGER.error("SVG File ({}) not found".format(svg_file))
            return False
        list_config.append(board_cfg)

    register_built_in_panel(hass, 'dashboard', 'Dashboard',
                            'mdi:bulletin-board', config=list_config)

    return True
