﻿# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
from typing import TYPE_CHECKING, List
from ..protobufs import main_pb2
from ..units import Units, units_from_literals, LengthUnits, VelocityUnits, AccelerationUnits
from ..call import call, call_async, call_sync
from .lockstep_axes import LockstepAxes

if TYPE_CHECKING:
    from .device import Device


class Lockstep:
    """
    Represents a lockstep group with this ID on a device.
    A lockstep group is a movement synchronized pair of axes on a device.
    Requires at least Firmware 6.15 or 7.11.
    """

    @property
    def device(self) -> 'Device':
        """
        Device that controls this lockstep group.
        """
        return self._device

    @property
    def lockstep_group_id(self) -> int:
        """
        The number that identifies the lockstep group on the device.
        """
        return self._lockstep_group_id

    def __init__(self, device: 'Device', lockstep_group_id: int):
        self._device = device
        self._lockstep_group_id = lockstep_group_id

    def enable(
            self,
            *axes: int
    ) -> None:
        """
        Activate the lockstep group on the axes specified.

        Args:
            axes: The numbers of axes in the lockstep group.
        """
        request = main_pb2.LockstepEnableRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.axes.extend(axes)
        call("device/lockstep_enable", request)

    async def enable_async(
            self,
            *axes: int
    ) -> None:
        """
        Activate the lockstep group on the axes specified.

        Args:
            axes: The numbers of axes in the lockstep group.
        """
        request = main_pb2.LockstepEnableRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.axes.extend(axes)
        await call_async("device/lockstep_enable", request)

    def disable(
            self
    ) -> None:
        """
        Disable the lockstep group.
        """
        request = main_pb2.LockstepDisableRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        call("device/lockstep_disable", request)

    async def disable_async(
            self
    ) -> None:
        """
        Disable the lockstep group.
        """
        request = main_pb2.LockstepDisableRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        await call_async("device/lockstep_disable", request)

    def stop(
            self,
            wait_until_idle: bool = True
    ) -> None:
        """
        Stops ongoing lockstep group movement. Decelerates until zero speed.

        Args:
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
        """
        request = main_pb2.LockstepStopRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.wait_until_idle = wait_until_idle
        call("device/lockstep_stop", request)

    async def stop_async(
            self,
            wait_until_idle: bool = True
    ) -> None:
        """
        Stops ongoing lockstep group movement. Decelerates until zero speed.

        Args:
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
        """
        request = main_pb2.LockstepStopRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.wait_until_idle = wait_until_idle
        await call_async("device/lockstep_stop", request)

    def home(
            self,
            wait_until_idle: bool = True
    ) -> None:
        """
        Retracts the axes of the lockstep group until a home associated with an individual axis is detected.

        Args:
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
        """
        request = main_pb2.LockstepHomeRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.wait_until_idle = wait_until_idle
        call("device/lockstep_home", request)

    async def home_async(
            self,
            wait_until_idle: bool = True
    ) -> None:
        """
        Retracts the axes of the lockstep group until a home associated with an individual axis is detected.

        Args:
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
        """
        request = main_pb2.LockstepHomeRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.wait_until_idle = wait_until_idle
        await call_async("device/lockstep_home", request)

    def move_absolute(
            self,
            position: float,
            unit: LengthUnits = Units.NATIVE,
            wait_until_idle: bool = True,
            velocity: float = 0,
            velocity_unit: VelocityUnits = Units.NATIVE,
            acceleration: float = 0,
            acceleration_unit: AccelerationUnits = Units.NATIVE
    ) -> None:
        """
        Move the first axis of the lockstep group to an absolute position.
        The other axes in the lockstep group maintain their offsets throughout movement.

        Args:
            position: Absolute position.
            unit: Units of position.
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
            velocity: Movement velocity.
                Default value of 0 indicates that the maxspeed setting is used instead.
                Requires at least Firmware 7.25.
            velocity_unit: Units of velocity.
            acceleration: Movement acceleration.
                Default value of 0 indicates that the accel setting is used instead.
                Requires at least Firmware 7.25.
            acceleration_unit: Units of acceleration.
        """
        request = main_pb2.LockstepMoveRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.type = main_pb2.LockstepMoveRequest.ABS
        request.arg = position
        request.unit = units_from_literals(unit).value
        request.wait_until_idle = wait_until_idle
        request.velocity = velocity
        request.velocity_unit = units_from_literals(velocity_unit).value
        request.acceleration = acceleration
        request.acceleration_unit = units_from_literals(acceleration_unit).value
        call("device/lockstep_move", request)

    async def move_absolute_async(
            self,
            position: float,
            unit: LengthUnits = Units.NATIVE,
            wait_until_idle: bool = True,
            velocity: float = 0,
            velocity_unit: VelocityUnits = Units.NATIVE,
            acceleration: float = 0,
            acceleration_unit: AccelerationUnits = Units.NATIVE
    ) -> None:
        """
        Move the first axis of the lockstep group to an absolute position.
        The other axes in the lockstep group maintain their offsets throughout movement.

        Args:
            position: Absolute position.
            unit: Units of position.
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
            velocity: Movement velocity.
                Default value of 0 indicates that the maxspeed setting is used instead.
                Requires at least Firmware 7.25.
            velocity_unit: Units of velocity.
            acceleration: Movement acceleration.
                Default value of 0 indicates that the accel setting is used instead.
                Requires at least Firmware 7.25.
            acceleration_unit: Units of acceleration.
        """
        request = main_pb2.LockstepMoveRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.type = main_pb2.LockstepMoveRequest.ABS
        request.arg = position
        request.unit = units_from_literals(unit).value
        request.wait_until_idle = wait_until_idle
        request.velocity = velocity
        request.velocity_unit = units_from_literals(velocity_unit).value
        request.acceleration = acceleration
        request.acceleration_unit = units_from_literals(acceleration_unit).value
        await call_async("device/lockstep_move", request)

    def move_relative(
            self,
            position: float,
            unit: LengthUnits = Units.NATIVE,
            wait_until_idle: bool = True,
            velocity: float = 0,
            velocity_unit: VelocityUnits = Units.NATIVE,
            acceleration: float = 0,
            acceleration_unit: AccelerationUnits = Units.NATIVE
    ) -> None:
        """
        Move the first axis of the lockstep group to a position relative to its current position.
        The other axes in the lockstep group maintain their offsets throughout movement.

        Args:
            position: Relative position.
            unit: Units of position.
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
            velocity: Movement velocity.
                Default value of 0 indicates that the maxspeed setting is used instead.
                Requires at least Firmware 7.25.
            velocity_unit: Units of velocity.
            acceleration: Movement acceleration.
                Default value of 0 indicates that the accel setting is used instead.
                Requires at least Firmware 7.25.
            acceleration_unit: Units of acceleration.
        """
        request = main_pb2.LockstepMoveRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.type = main_pb2.LockstepMoveRequest.REL
        request.arg = position
        request.unit = units_from_literals(unit).value
        request.wait_until_idle = wait_until_idle
        request.velocity = velocity
        request.velocity_unit = units_from_literals(velocity_unit).value
        request.acceleration = acceleration
        request.acceleration_unit = units_from_literals(acceleration_unit).value
        call("device/lockstep_move", request)

    async def move_relative_async(
            self,
            position: float,
            unit: LengthUnits = Units.NATIVE,
            wait_until_idle: bool = True,
            velocity: float = 0,
            velocity_unit: VelocityUnits = Units.NATIVE,
            acceleration: float = 0,
            acceleration_unit: AccelerationUnits = Units.NATIVE
    ) -> None:
        """
        Move the first axis of the lockstep group to a position relative to its current position.
        The other axes in the lockstep group maintain their offsets throughout movement.

        Args:
            position: Relative position.
            unit: Units of position.
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
            velocity: Movement velocity.
                Default value of 0 indicates that the maxspeed setting is used instead.
                Requires at least Firmware 7.25.
            velocity_unit: Units of velocity.
            acceleration: Movement acceleration.
                Default value of 0 indicates that the accel setting is used instead.
                Requires at least Firmware 7.25.
            acceleration_unit: Units of acceleration.
        """
        request = main_pb2.LockstepMoveRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.type = main_pb2.LockstepMoveRequest.REL
        request.arg = position
        request.unit = units_from_literals(unit).value
        request.wait_until_idle = wait_until_idle
        request.velocity = velocity
        request.velocity_unit = units_from_literals(velocity_unit).value
        request.acceleration = acceleration
        request.acceleration_unit = units_from_literals(acceleration_unit).value
        await call_async("device/lockstep_move", request)

    def move_velocity(
            self,
            velocity: float,
            unit: VelocityUnits = Units.NATIVE,
            acceleration: float = 0,
            acceleration_unit: AccelerationUnits = Units.NATIVE
    ) -> None:
        """
        Moves the first axis of the lockstep group at the specified speed.
        The other axes in the lockstep group maintain their offsets throughout movement.

        Args:
            velocity: Movement velocity.
            unit: Units of velocity.
            acceleration: Movement acceleration.
                Default value of 0 indicates that the accel setting is used instead.
                Requires at least Firmware 7.25.
            acceleration_unit: Units of acceleration.
        """
        request = main_pb2.LockstepMoveRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.type = main_pb2.LockstepMoveRequest.VEL
        request.arg = velocity
        request.unit = units_from_literals(unit).value
        request.acceleration = acceleration
        request.acceleration_unit = units_from_literals(acceleration_unit).value
        call("device/lockstep_move", request)

    async def move_velocity_async(
            self,
            velocity: float,
            unit: VelocityUnits = Units.NATIVE,
            acceleration: float = 0,
            acceleration_unit: AccelerationUnits = Units.NATIVE
    ) -> None:
        """
        Moves the first axis of the lockstep group at the specified speed.
        The other axes in the lockstep group maintain their offsets throughout movement.

        Args:
            velocity: Movement velocity.
            unit: Units of velocity.
            acceleration: Movement acceleration.
                Default value of 0 indicates that the accel setting is used instead.
                Requires at least Firmware 7.25.
            acceleration_unit: Units of acceleration.
        """
        request = main_pb2.LockstepMoveRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.type = main_pb2.LockstepMoveRequest.VEL
        request.arg = velocity
        request.unit = units_from_literals(unit).value
        request.acceleration = acceleration
        request.acceleration_unit = units_from_literals(acceleration_unit).value
        await call_async("device/lockstep_move", request)

    def move_max(
            self,
            wait_until_idle: bool = True,
            velocity: float = 0,
            velocity_unit: VelocityUnits = Units.NATIVE,
            acceleration: float = 0,
            acceleration_unit: AccelerationUnits = Units.NATIVE
    ) -> None:
        """
        Moves the axes to the maximum valid position.
        The axes in the lockstep group maintain their offsets throughout movement.
        Respects lim.max for all axes in the group.

        Args:
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
            velocity: Movement velocity.
                Default value of 0 indicates that the maxspeed setting is used instead.
                Requires at least Firmware 7.25.
            velocity_unit: Units of velocity.
            acceleration: Movement acceleration.
                Default value of 0 indicates that the accel setting is used instead.
                Requires at least Firmware 7.25.
            acceleration_unit: Units of acceleration.
        """
        request = main_pb2.LockstepMoveRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.type = main_pb2.LockstepMoveRequest.MAX
        request.wait_until_idle = wait_until_idle
        request.velocity = velocity
        request.velocity_unit = units_from_literals(velocity_unit).value
        request.acceleration = acceleration
        request.acceleration_unit = units_from_literals(acceleration_unit).value
        call("device/lockstep_move", request)

    async def move_max_async(
            self,
            wait_until_idle: bool = True,
            velocity: float = 0,
            velocity_unit: VelocityUnits = Units.NATIVE,
            acceleration: float = 0,
            acceleration_unit: AccelerationUnits = Units.NATIVE
    ) -> None:
        """
        Moves the axes to the maximum valid position.
        The axes in the lockstep group maintain their offsets throughout movement.
        Respects lim.max for all axes in the group.

        Args:
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
            velocity: Movement velocity.
                Default value of 0 indicates that the maxspeed setting is used instead.
                Requires at least Firmware 7.25.
            velocity_unit: Units of velocity.
            acceleration: Movement acceleration.
                Default value of 0 indicates that the accel setting is used instead.
                Requires at least Firmware 7.25.
            acceleration_unit: Units of acceleration.
        """
        request = main_pb2.LockstepMoveRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.type = main_pb2.LockstepMoveRequest.MAX
        request.wait_until_idle = wait_until_idle
        request.velocity = velocity
        request.velocity_unit = units_from_literals(velocity_unit).value
        request.acceleration = acceleration
        request.acceleration_unit = units_from_literals(acceleration_unit).value
        await call_async("device/lockstep_move", request)

    def move_min(
            self,
            wait_until_idle: bool = True,
            velocity: float = 0,
            velocity_unit: VelocityUnits = Units.NATIVE,
            acceleration: float = 0,
            acceleration_unit: AccelerationUnits = Units.NATIVE
    ) -> None:
        """
        Moves the axes to the minimum valid position.
        The axes in the lockstep group maintain their offsets throughout movement.
        Respects lim.min for all axes in the group.

        Args:
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
            velocity: Movement velocity.
                Default value of 0 indicates that the maxspeed setting is used instead.
                Requires at least Firmware 7.25.
            velocity_unit: Units of velocity.
            acceleration: Movement acceleration.
                Default value of 0 indicates that the accel setting is used instead.
                Requires at least Firmware 7.25.
            acceleration_unit: Units of acceleration.
        """
        request = main_pb2.LockstepMoveRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.type = main_pb2.LockstepMoveRequest.MIN
        request.wait_until_idle = wait_until_idle
        request.velocity = velocity
        request.velocity_unit = units_from_literals(velocity_unit).value
        request.acceleration = acceleration
        request.acceleration_unit = units_from_literals(acceleration_unit).value
        call("device/lockstep_move", request)

    async def move_min_async(
            self,
            wait_until_idle: bool = True,
            velocity: float = 0,
            velocity_unit: VelocityUnits = Units.NATIVE,
            acceleration: float = 0,
            acceleration_unit: AccelerationUnits = Units.NATIVE
    ) -> None:
        """
        Moves the axes to the minimum valid position.
        The axes in the lockstep group maintain their offsets throughout movement.
        Respects lim.min for all axes in the group.

        Args:
            wait_until_idle: Determines whether function should return after the movement is finished or just started.
            velocity: Movement velocity.
                Default value of 0 indicates that the maxspeed setting is used instead.
                Requires at least Firmware 7.25.
            velocity_unit: Units of velocity.
            acceleration: Movement acceleration.
                Default value of 0 indicates that the accel setting is used instead.
                Requires at least Firmware 7.25.
            acceleration_unit: Units of acceleration.
        """
        request = main_pb2.LockstepMoveRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.type = main_pb2.LockstepMoveRequest.MIN
        request.wait_until_idle = wait_until_idle
        request.velocity = velocity
        request.velocity_unit = units_from_literals(velocity_unit).value
        request.acceleration = acceleration
        request.acceleration_unit = units_from_literals(acceleration_unit).value
        await call_async("device/lockstep_move", request)

    def wait_until_idle(
            self,
            throw_error_on_fault: bool = True
    ) -> None:
        """
        Waits until the lockstep group stops moving.

        Args:
            throw_error_on_fault: Determines whether to throw error when fault is observed.
        """
        request = main_pb2.LockstepWaitUntilIdleRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.throw_error_on_fault = throw_error_on_fault
        call("device/lockstep_wait_until_idle", request)

    async def wait_until_idle_async(
            self,
            throw_error_on_fault: bool = True
    ) -> None:
        """
        Waits until the lockstep group stops moving.

        Args:
            throw_error_on_fault: Determines whether to throw error when fault is observed.
        """
        request = main_pb2.LockstepWaitUntilIdleRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.throw_error_on_fault = throw_error_on_fault
        await call_async("device/lockstep_wait_until_idle", request)

    def is_busy(
            self
    ) -> bool:
        """
        Returns bool indicating whether the lockstep group is executing a motion command.

        Returns:
            True if the axes are currently executing a motion command.
        """
        request = main_pb2.LockstepEmptyRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        response = main_pb2.BoolResponse()
        call("device/lockstep_is_busy", request, response)
        return response.value

    async def is_busy_async(
            self
    ) -> bool:
        """
        Returns bool indicating whether the lockstep group is executing a motion command.

        Returns:
            True if the axes are currently executing a motion command.
        """
        request = main_pb2.LockstepEmptyRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        response = main_pb2.BoolResponse()
        await call_async("device/lockstep_is_busy", request, response)
        return response.value

    def get_axes(
            self
    ) -> LockstepAxes:
        """
        Deprecated: Use GetAxisNumbers instead.

        Gets the axes of the lockstep group.

        Returns:
            LockstepAxes instance which contains the axes numbers of the lockstep group.
        """
        request = main_pb2.LockstepEmptyRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        response = main_pb2.LockstepAxes()
        call("device/lockstep_get_axes", request, response)
        return LockstepAxes.from_protobuf(response)

    async def get_axes_async(
            self
    ) -> LockstepAxes:
        """
        Deprecated: Use GetAxisNumbers instead.

        Gets the axes of the lockstep group.

        Returns:
            LockstepAxes instance which contains the axes numbers of the lockstep group.
        """
        request = main_pb2.LockstepEmptyRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        response = main_pb2.LockstepAxes()
        await call_async("device/lockstep_get_axes", request, response)
        return LockstepAxes.from_protobuf(response)

    def get_axis_numbers(
            self
    ) -> List[int]:
        """
        Gets the axis numbers of the lockstep group.

        Returns:
            Axis numbers in order specified when enabling lockstep.
        """
        request = main_pb2.LockstepEmptyRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        response = main_pb2.LockstepGetAxisNumbersResponse()
        call("device/lockstep_get_axis_numbers", request, response)
        return list(response.axes)

    async def get_axis_numbers_async(
            self
    ) -> List[int]:
        """
        Gets the axis numbers of the lockstep group.

        Returns:
            Axis numbers in order specified when enabling lockstep.
        """
        request = main_pb2.LockstepEmptyRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        response = main_pb2.LockstepGetAxisNumbersResponse()
        await call_async("device/lockstep_get_axis_numbers", request, response)
        return list(response.axes)

    def get_offsets(
            self,
            unit: LengthUnits = Units.NATIVE
    ) -> List[float]:
        """
        Gets the initial offsets of secondary axes of an enabled lockstep group.

        Args:
            unit: Units of position.
                Uses primary axis unit conversion.

        Returns:
            Initial offset for each axis of the lockstep group.
        """
        request = main_pb2.LockstepGetRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.unit = units_from_literals(unit).value
        response = main_pb2.DoubleArrayResponse()
        call("device/lockstep_get_offsets", request, response)
        return list(response.values)

    async def get_offsets_async(
            self,
            unit: LengthUnits = Units.NATIVE
    ) -> List[float]:
        """
        Gets the initial offsets of secondary axes of an enabled lockstep group.

        Args:
            unit: Units of position.
                Uses primary axis unit conversion.

        Returns:
            Initial offset for each axis of the lockstep group.
        """
        request = main_pb2.LockstepGetRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.unit = units_from_literals(unit).value
        response = main_pb2.DoubleArrayResponse()
        await call_async("device/lockstep_get_offsets", request, response)
        return list(response.values)

    def get_twists(
            self,
            unit: LengthUnits = Units.NATIVE
    ) -> List[float]:
        """
        Gets the twists of secondary axes of an enabled lockstep group.

        Args:
            unit: Units of position.
                Uses primary axis unit conversion.

        Returns:
            Difference between the initial offset and the actual offset for each axis of the lockstep group.
        """
        request = main_pb2.LockstepGetRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.unit = units_from_literals(unit).value
        response = main_pb2.DoubleArrayResponse()
        call("device/lockstep_get_twists", request, response)
        return list(response.values)

    async def get_twists_async(
            self,
            unit: LengthUnits = Units.NATIVE
    ) -> List[float]:
        """
        Gets the twists of secondary axes of an enabled lockstep group.

        Args:
            unit: Units of position.
                Uses primary axis unit conversion.

        Returns:
            Difference between the initial offset and the actual offset for each axis of the lockstep group.
        """
        request = main_pb2.LockstepGetRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.unit = units_from_literals(unit).value
        response = main_pb2.DoubleArrayResponse()
        await call_async("device/lockstep_get_twists", request, response)
        return list(response.values)

    def get_position(
            self,
            unit: LengthUnits = Units.NATIVE
    ) -> float:
        """
        Returns current position of the primary axis.

        Args:
            unit: Units of the position.

        Returns:
            Primary axis position.
        """
        request = main_pb2.LockstepGetRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.unit = units_from_literals(unit).value
        response = main_pb2.DoubleResponse()
        call("device/lockstep_get_pos", request, response)
        return response.value

    async def get_position_async(
            self,
            unit: LengthUnits = Units.NATIVE
    ) -> float:
        """
        Returns current position of the primary axis.

        Args:
            unit: Units of the position.

        Returns:
            Primary axis position.
        """
        request = main_pb2.LockstepGetRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.unit = units_from_literals(unit).value
        response = main_pb2.DoubleResponse()
        await call_async("device/lockstep_get_pos", request, response)
        return response.value

    def set_tolerance(
            self,
            tolerance: float,
            unit: LengthUnits = Units.NATIVE,
            axis_index: int = 0
    ) -> None:
        """
        Sets lockstep twist tolerance.
        Twist tolerances that do not match the system configuration can reduce performance or damage the system.

        Args:
            tolerance: Twist tolerance.
            unit: Units of the tolerance.
                Uses primary axis unit conversion when setting to all axes,
                otherwise uses specified secondary axis unit conversion.
            axis_index: Optional index of a secondary axis to set the tolerance for.
                If left empty or set to 0, the tolerance is set to all the secondary axes.
        """
        request = main_pb2.LockstepSetRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.value = tolerance
        request.unit = units_from_literals(unit).value
        request.axis_index = axis_index
        call("device/lockstep_set_tolerance", request)

    async def set_tolerance_async(
            self,
            tolerance: float,
            unit: LengthUnits = Units.NATIVE,
            axis_index: int = 0
    ) -> None:
        """
        Sets lockstep twist tolerance.
        Twist tolerances that do not match the system configuration can reduce performance or damage the system.

        Args:
            tolerance: Twist tolerance.
            unit: Units of the tolerance.
                Uses primary axis unit conversion when setting to all axes,
                otherwise uses specified secondary axis unit conversion.
            axis_index: Optional index of a secondary axis to set the tolerance for.
                If left empty or set to 0, the tolerance is set to all the secondary axes.
        """
        request = main_pb2.LockstepSetRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        request.value = tolerance
        request.unit = units_from_literals(unit).value
        request.axis_index = axis_index
        await call_async("device/lockstep_set_tolerance", request)

    def is_enabled(
            self
    ) -> bool:
        """
        Checks if the lockstep group is currently enabled on the device.

        Returns:
            True if a lockstep group with this ID is enabled on the device.
        """
        request = main_pb2.LockstepEmptyRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        response = main_pb2.BoolResponse()
        call("device/lockstep_is_enabled", request, response)
        return response.value

    async def is_enabled_async(
            self
    ) -> bool:
        """
        Checks if the lockstep group is currently enabled on the device.

        Returns:
            True if a lockstep group with this ID is enabled on the device.
        """
        request = main_pb2.LockstepEmptyRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        response = main_pb2.BoolResponse()
        await call_async("device/lockstep_is_enabled", request, response)
        return response.value

    def __repr__(
            self
    ) -> str:
        """
        Returns a string which represents the enabled lockstep group.

        Returns:
            String which represents the enabled lockstep group.
        """
        request = main_pb2.LockstepEmptyRequest()
        request.interface_id = self.device.connection.interface_id
        request.device = self.device.device_address
        request.lockstep_group_id = self.lockstep_group_id
        response = main_pb2.StringResponse()
        call_sync("device/lockstep_to_string", request, response)
        return response.value
