﻿# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
from enum import Enum


class IoPortType(Enum):
    """
    Kind of I/O pin to use.
    """

    NONE = 0
    ANALOG_INPUT = 1
    ANALOG_OUTPUT = 2
    DIGITAL_INPUT = 3
    DIGITAL_OUTPUT = 4
