﻿# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
from typing import TYPE_CHECKING, List

from ..call import call, call_async
from ..protobufs import main_pb2

from .pvt_sequence import PvtSequence
from .pvt_buffer import PvtBuffer

if TYPE_CHECKING:
    from .device import Device


class Pvt:
    """
    Class providing access to device PVT (Position-Velocity-Time) features.
    Requires at least Firmware 7.33.
    """

    @property
    def device(self) -> 'Device':
        """
        Device that this PVT belongs to.
        """
        return self._device

    def __init__(self, device: 'Device'):
        self._device = device

    def get_sequence(
            self,
            pvt_id: int
    ) -> 'PvtSequence':
        """
        Gets a PvtSequence class instance which allows you to control a particular PVT sequence on the device.

        Args:
            pvt_id: The ID of the PVT sequence to control. The IDs start at 1.

        Returns:
            PvtSequence instance.
        """
        if pvt_id <= 0:
            raise ValueError('Invalid value; PVT sequences are numbered from 1.')

        return PvtSequence(self.device, pvt_id)

    def get_buffer(
            self,
            pvt_buffer_id: int
    ) -> 'PvtBuffer':
        """
        Gets a PvtBuffer class instance which is a handle for a PVT buffer on the device.

        Args:
            pvt_buffer_id: The ID of the PVT buffer to control. PVT buffer IDs start at one.

        Returns:
            PvtBuffer instance.
        """
        if pvt_buffer_id <= 0:
            raise ValueError('Invalid value; PVT buffers are numbered from 1.')

        return PvtBuffer(self.device, pvt_buffer_id)

    def list_buffer_ids(
            self
    ) -> List[int]:
        """
        Get a list of buffer IDs that are currently in use.

        Returns:
            List of buffer IDs.
        """
        request = main_pb2.StreamBufferList()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.pvt = True
        response = main_pb2.IntArrayResponse()
        call("device/stream_buffer_list", request, response)
        return list(response.values)

    async def list_buffer_ids_async(
            self
    ) -> List[int]:
        """
        Get a list of buffer IDs that are currently in use.

        Returns:
            List of buffer IDs.
        """
        request = main_pb2.StreamBufferList()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.pvt = True
        response = main_pb2.IntArrayResponse()
        await call_async("device/stream_buffer_list", request, response)
        return list(response.values)
