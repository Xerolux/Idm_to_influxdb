# SPDX-License-Identifier: MIT
"""Tests for Luxtronik driver and adapter."""

import unittest
from unittest.mock import MagicMock, patch
import struct
import socket
from idm_logger.manufacturers.luxtronik.luxtronik_2_1 import (
    Luxtronik21Driver,
    LuxtronikClientAdapter,
)


class TestLuxtronikAdapter(unittest.TestCase):
    def test_connect_success(self):
        adapter = LuxtronikClientAdapter("1.2.3.4")
        with patch("socket.socket") as mock_socket_cls:
            mock_socket = MagicMock()
            mock_socket_cls.return_value = mock_socket

            self.assertTrue(adapter.connect())
            mock_socket.connect.assert_called_with(("1.2.3.4", 8889))
            self.assertTrue(adapter.is_socket_open())

    def test_connect_fail(self):
        adapter = LuxtronikClientAdapter("1.2.3.4")
        with patch("socket.socket") as mock_socket_cls:
            mock_socket = MagicMock()
            mock_socket.connect.side_effect = Exception("Connection refused")
            mock_socket_cls.return_value = mock_socket

            self.assertFalse(adapter.connect())
            self.assertFalse(adapter.is_socket_open())

    def test_read_holding_registers(self):
        adapter = LuxtronikClientAdapter("1.2.3.4")

        # Mock socket interactions
        with patch("socket.socket") as mock_socket_cls:
            mock_socket = MagicMock()
            mock_socket_cls.return_value = mock_socket
            adapter.connect()

            # Prepare mock response data for CMD 3004
            # 1. Echo CMD: 3004 (4 bytes)
            # 2. Status: 0 (4 bytes)
            # 3. Count: 20 (4 bytes)
            # 4. Payload: 20 integers (4 bytes each)

            mock_payload = []
            mock_payload.append(struct.pack(">I", 3004))  # Echo
            mock_payload.append(struct.pack(">I", 0))     # Status
            mock_payload.append(struct.pack(">I", 20))    # Count

            # Values: index 0..19 = 0, 10, 20... 190
            values = list(range(0, 200, 10))
            for v in values:
                mock_payload.append(struct.pack(">i", v))

            # Flatten to bytes
            response_data = b"".join(mock_payload)

            # Set recv side effect to return chunks
            # We need to simulate recv calls. The adapter calls _recv_exact multiple times.
            # 1. cmd (4)
            # 2. stat (4)
            # 3. count (4)
            # 4. payload (size)

            # Instead of complex side_effect, let's just make it return the slices requested
            # Since _recv_exact loops until size is met, we can just feed it data.
            # A simpler way is to mock _recv_exact if we want to test logic ABOVE it,
            # or mock socket.recv to return everything in one go (but logic might request specific sizes).

            # Let's mock socket.recv to pop bytes from our buffer
            buffer = bytearray(response_data)

            def side_effect_recv(bufsize):
                nonlocal buffer
                if not buffer:
                    return b""
                chunk = buffer[:bufsize]
                buffer = buffer[bufsize:]
                return bytes(chunk)

            mock_socket.recv.side_effect = side_effect_recv

            # Test reading index 15 (temp_outside)
            # Expected value at index 15 is 150
            response = adapter.read_holding_registers(15, 1)

            self.assertFalse(response.isError())
            self.assertEqual(len(response.registers), 1)
            self.assertEqual(response.registers[0], 150)


class TestLuxtronikDriver(unittest.TestCase):
    def setUp(self):
        self.driver = Luxtronik21Driver()
        self.config = {}

    def test_sensor_definitions(self):
        sensors = self.driver.get_sensors(self.config)
        self.assertTrue(len(sensors) > 5)

        # Check specific sensor
        temp_outside = next((s for s in sensors if s.id == "temp_outside"), None)
        self.assertIsNotNone(temp_outside)
        self.assertEqual(temp_outside.address, 15)
        self.assertEqual(temp_outside.scale, 0.1)

    def test_create_client(self):
        config = {"host": "10.0.0.1", "port": 1234}
        client = self.driver.create_client(config)
        self.assertIsInstance(client, LuxtronikClientAdapter)
        self.assertEqual(client.host, "10.0.0.1")
        self.assertEqual(client.port, 1234)

    def test_parse_value(self):
        # Driver creates sensors
        sensors = self.driver.get_sensors({})
        temp_sensor = next(s for s in sensors if s.id == "temp_outside")

        # Adapter returns [150] (raw int from socket)
        # Driver should scale by 0.1 -> 15.0
        val = self.driver.parse_value(temp_sensor, [150])
        self.assertAlmostEqual(val, 15.0)


if __name__ == "__main__":
    unittest.main()
