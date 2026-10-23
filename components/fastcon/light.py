"""Light platform for Fastcon BLE lights."""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import light
from esphome.const import CONF_LIGHT_ID, CONF_OUTPUT_ID

from .fastcon_controller import FastconController

DEPENDENCIES = ["esp32_ble"]
AUTO_LOAD = ["light"]

CONF_CONTROLLER_ID = "controller_id"
CONF_WHITE_MODE = "white_mode"
WHITE_MODES = {"cct": 0, "fixed": 1, "rgb_emulated": 2}

fastcon_ns = cg.esphome_ns.namespace("fastcon")
FastconLight = fastcon_ns.class_("FastconLight", light.LightOutput, cg.Component)

CONFIG_SCHEMA = cv.All(
    light.BRIGHTNESS_ONLY_LIGHT_SCHEMA.extend(
        {
            cv.GenerateID(CONF_OUTPUT_ID): cv.declare_id(FastconLight),
            cv.Required(CONF_LIGHT_ID): cv.int_range(min=1, max=255),
            cv.Optional(CONF_WHITE_MODE, default="cct"): cv.enum(WHITE_MODES, lower=True),
            cv.Optional(CONF_CONTROLLER_ID, default="fastcon_controller"): cv.use_id(
                FastconController
            ),
        }
    ).extend(cv.COMPONENT_SCHEMA)
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_OUTPUT_ID], config[CONF_LIGHT_ID])
    await cg.register_component(var, config)
    await light.register_light(var, config)

    controller = await cg.get_variable(config[CONF_CONTROLLER_ID])
    cg.add(var.set_controller(controller))
    cg.add(var.set_white_mode(WHITE_MODES[config[CONF_WHITE_MODE]]))
