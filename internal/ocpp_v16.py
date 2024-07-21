import logging
from datetime import datetime

from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call_result, call
from ocpp.v16.enums import (
    Action,
    AuthorizationStatus,
    ChargePointErrorCode,
    ChargePointStatus,
    DataTransferStatus,
    RegistrationStatus,
    ResetStatus,
    ResetType,
)
from ocpp.v16.datatypes import (
    IdTagInfo,
)

logging.basicConfig(level=logging.INFO)


class ChargePoint16(cp):
    websocket = None

    @on(Action.Authorize)
    def on_authorize(self, **kwargs):
        id_tag_info = IdTagInfo(status=AuthorizationStatus.accepted)
        return call_result.Authorize(id_tag_info=id_tag_info)

    @on(Action.BootNotification)
    def on_boot_notification(
        self,
        charge_point_vendor: str,
        charge_point_model: str,
        **kwargs
    ):
        return call_result.BootNotification(
            current_time=datetime.utcnow().isoformat(),
            interval=900,
            status=RegistrationStatus.accepted,
        )

    @on(Action.DataTransfer)
    def on_data_transfer(self, **kwargs):
        _ = call.DataTransfer(**kwargs)
        return call_result.DataTransfer(
                status=DataTransferStatus.unknown_vendor_id,
                data="Please implement me"
        )

    @on(Action.Heartbeat)
    def on_heartbeat(self, **kwargs):
        return call_result.Heartbeat(
            current_time=datetime.utcnow().isoformat(),
        )

    @on(Action.MeterValues)
    def on_meter_values(self, **kwargs):
        return call_result.MeterValues()

    @on(Action.StatusNotification)
    def on_status_notification(
        self,
        connector_id: int,
        error_code: ChargePointErrorCode,
        status: ChargePointStatus,
        **kwargs
    ):
        return call_result.StatusNotification()

    @on(Action.StartTransaction)
    def on_start_transaction(self, **kwargs):
        id_tag_info = IdTagInfo(status=AuthorizationStatus.accepted)
        return call_result.StartTransaction(transaction_id=1,
                                            id_tag_info=id_tag_info)

    @on(Action.StopTransaction)
    def on_stop_transaction(self, **kwargs):
        return call_result.StopTransaction()

    async def request_reset(self, **kwargs):
        request = call.Reset(ResetType.hard)
        response = await self.call(request)

        if response.status == ResetStatus.accepted:
            logging.info("Reset requested")

    async def request_get_configuration(self, **kwargs):
        payload = call.GetConfiguration(**kwargs)
        return await self.call(payload)

    async def request_change_configuration(self, **kwargs):
        payload = call.ChangeConfiguration(**kwargs)
        return await self.call(payload)

    async def request_remote_start_transaction(self, **kwargs):
        payload = call.RemoteStartTransaction(**kwargs)
        return await self.call(payload)

    async def request_remote_stop_transaction(self, **kwargs):
        payload = call.RemoteStopTransaction(**kwargs)
        return await self.call(payload)

    async def request_update_firmware(self, **kwargs):
        payload = call.UpdateFirmware(**kwargs)
        return await self.call(payload)
