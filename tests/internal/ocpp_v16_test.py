import unittest
from unittest.mock import Mock, patch
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call_result, call
from ocpp.v16.enums import (
        AuthorizationStatus,
        RegistrationStatus,
        DataTransferStatus,
        ResetType,
        ResetStatus,
)
from internal.ocpp_v16 import ChargePoint16


class TestCp(unittest.TestCase):
    def setUp(self):
        self.cp = ChargePoint16("", None)

    def test_on_authorize(self):
        result = self.cp.on_authorize()
        self.assertIsInstance(result, call_result.Authorize)
        self.assertEqual(result.id_tag_info.status,
                         AuthorizationStatus.accepted)

    def test_on_boot_notification(self):
        result = self.cp.on_boot_notification('vendor', 'model')
        self.assertIsInstance(result, call_result.BootNotification)
        self.assertEqual(result.interval, 900)
        self.assertEqual(result.status, RegistrationStatus.accepted)

    def test_on_data_transfer(self):
        result = self.cp.on_data_transfer(
            vendor_id=DataTransferStatus.unknown_vendor_id)
        self.assertIsInstance(result, call_result.DataTransfer)
        self.assertEqual(result.status, DataTransferStatus.unknown_vendor_id)
        self.assertEqual(result.data, "Please implement me")


if __name__ == '__main__':
    unittest.main()
