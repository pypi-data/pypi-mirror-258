﻿# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from .call import call_sync
from .protobufs import main_pb2
from .log_output_mode import LogOutputMode
from .device_db_source_type import DeviceDbSourceType


class Library:
    """
    Access class to general library information and configuration.
    """

    @staticmethod
    def set_log_output(
            mode: LogOutputMode,
            file_path: str = ""
    ) -> None:
        """
        Sets library logging output.

        Args:
            mode: Logging output mode.
            file_path: Path of the file to open.
        """
        request = main_pb2.SetLogOutputRequest()
        request.mode = mode.value
        request.file_path = file_path
        call_sync("logging/set_output", request)

    @staticmethod
    def set_device_db_source(
            source_type: DeviceDbSourceType,
            url_or_file_path: str = ""
    ) -> None:
        """
        Sets source of Device DB data. Allows selection of a web service or a local file.

        Args:
            source_type: Source type.
            url_or_file_path: URL of the web service or path to the local file.
                Leave empty for the default URL of Zaber web service.
        """
        request = main_pb2.SetDeviceDbSourceRequest()
        request.source_type = source_type.value
        request.url_or_file_path = url_or_file_path
        call_sync("device_db/set_source", request)

    @staticmethod
    def enable_device_db_store(
            store_location: str = ""
    ) -> None:
        """
        Enables Device DB store.
        The store uses filesystem to save information obtained from the Device DB.
        The stored data are later used instead of the Device DB.

        Args:
            store_location: Specifies relative or absolute path of the folder used by the store.
                If left empty defaults to a folder in user home directory.
                Must be accessible by the process.
        """
        request = main_pb2.ToggleDeviceDbStoreRequest()
        request.toggle_on = True
        request.store_location = store_location
        call_sync("device_db/toggle_store", request)

    @staticmethod
    def disable_device_db_store() -> None:
        """
        Disables Device DB store.
        """
        request = main_pb2.ToggleDeviceDbStoreRequest()
        call_sync("device_db/toggle_store", request)

    @staticmethod
    def set_internal_mode(
            mode: bool
    ) -> None:
        """
        Disables certain customer checks (like FF flag).

        Args:
            mode: Whether to turn internal mode on or off.
        """
        request = main_pb2.SetInternalModeRequest()
        request.mode = mode
        call_sync("library/set_internal_mode", request)

    @staticmethod
    def set_idle_polling_period(
            period: int
    ) -> None:
        """
        Sets the period between polling for IDLE during movements.
        Caution: Setting the period too low may cause performance issues.

        Args:
            period: Period in milliseconds.
                Negative value restores the default period.
        """
        request = main_pb2.IntRequest()
        request.value = period
        call_sync("library/set_idle_polling_period", request)
