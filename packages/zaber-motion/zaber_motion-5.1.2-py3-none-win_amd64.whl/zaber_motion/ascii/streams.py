﻿# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
from typing import TYPE_CHECKING, List

from ..call import call, call_async
from ..protobufs import main_pb2

from .stream import Stream
from .stream_buffer import StreamBuffer

if TYPE_CHECKING:
    from .device import Device


class Streams:
    """
    Class providing access to device streams.
    Requires at least Firmware 7.05.
    """

    @property
    def device(self) -> 'Device':
        """
        Device that these streams belong to.
        """
        return self._device

    def __init__(self, device: 'Device'):
        self._device = device

    def get_stream(
            self,
            stream_id: int
    ) -> 'Stream':
        """
        Gets a Stream class instance which allows you to control a particular stream on the device.

        Args:
            stream_id: The ID of the stream to control. Stream IDs start at one.

        Returns:
            Stream instance.
        """
        if stream_id <= 0:
            raise ValueError('Invalid value; streams are numbered from 1.')

        return Stream(self.device, stream_id)

    def get_buffer(
            self,
            stream_buffer_id: int
    ) -> 'StreamBuffer':
        """
        Gets a StreamBuffer class instance which is a handle for a stream buffer on the device.

        Args:
            stream_buffer_id: The ID of the stream buffer to control. Stream buffer IDs start at one.

        Returns:
            StreamBuffer instance.
        """
        if stream_buffer_id <= 0:
            raise ValueError('Invalid value; stream buffers are numbered from 1.')

        return StreamBuffer(self.device, stream_buffer_id)

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
        request.pvt = False
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
        request.pvt = False
        response = main_pb2.IntArrayResponse()
        await call_async("device/stream_buffer_list", request, response)
        return list(response.values)
