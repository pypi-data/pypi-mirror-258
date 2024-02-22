﻿# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from typing import List, Optional  # pylint: disable=unused-import
from ..protobufs import main_pb2
from ..units import UnitsAndLiterals, Units, units_from_literals


class GetSetting:
    """
    Specifies a setting to get with one of the multi-get commands.
    """

    def __init__(
            self: 'GetSetting',
            setting: str,
            axes: Optional[List[int]] = None,
            unit: Optional[UnitsAndLiterals] = None
    ) -> None:
        self._setting = setting
        self._axes = axes
        self._unit = unit

    @property
    def setting(self) -> str:
        """
        The setting to read.
        """

        return self._setting

    @setting.setter
    def setting(self, value: str) -> None:
        self._setting = value

    @property
    def axes(self) -> Optional[List[int]]:
        """
        The list of axes to read.
        """

        return self._axes

    @axes.setter
    def axes(self, value: Optional[List[int]]) -> None:
        self._axes = value

    @property
    def unit(self) -> Optional[UnitsAndLiterals]:
        """
        The unit to convert the read settings to.
        """

        return self._unit

    @unit.setter
    def unit(self, value: Optional[UnitsAndLiterals]) -> None:
        self._unit = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def to_protobuf(source: 'Optional[GetSetting]') -> main_pb2.GetSetting:
        pb_data = main_pb2.GetSetting()

        if source is None:
            return pb_data

        if not isinstance(source, GetSetting):
            raise TypeError("Provided value is not GetSetting.")

        pb_data.setting = source.setting
        if source.axes is not None:
            pb_data.axes.extend(source.axes)
        pb_data.unit = units_from_literals(source.unit or Units.NATIVE).value
        return pb_data
