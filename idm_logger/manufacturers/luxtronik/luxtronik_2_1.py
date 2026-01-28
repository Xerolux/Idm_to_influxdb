# SPDX-License-Identifier: MIT
"""
Luxtronik 2.1 Heat Pump Driver (TCP).
Used by Bosch, Alpha Innotec, Novelan, etc.
"""

import socket
import struct
import logging
import time
from typing import List, Dict, Any, Optional

from ..base import (
    HeatpumpDriver,
    SensorDefinition,
    SensorCategory,
    DataType,
    AccessMode,
    HeatpumpCapabilities,
)
from .. import ManufacturerRegistry

logger = logging.getLogger(__name__)


class LuxtronikClientAdapter:
    """
    Adapter to make Luxtronik 2.1 protocol look like a Modbus client.
    Implements a subset of the pymodbus client interface.
    """

    def __init__(self, host: str, port: int = 8889, timeout: float = 10.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket = None
        self._connected = False

    def connect(self) -> bool:
        """Establish connection to the heat pump."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            self._connected = True
            return True
        except Exception as e:
            logger.error(f"Luxtronik connect error: {e}")
            self._connected = False
            return False

    def close(self):
        """Close the connection."""
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
        self.socket = None
        self._connected = False

    def is_socket_open(self) -> bool:
        """Check if socket is connected."""
        return self._connected

    def read_holding_registers(self, address: int, count: int = 1, **kwargs) -> Any:
        """
        Mimic Modbus read_holding_registers.
        For Luxtronik, 'address' corresponds to the parameter/calc index.

        Since Luxtronik protocol reads bulk data (e.g. all calculations),
        we perform a full read and extract the requested values.
        """
        # Return object that mimics pymodbus response
        class Response:
            def __init__(self, registers, is_error=False):
                self.registers = registers
                self._is_error = is_error

            def isError(self):
                return self._is_error

        if not self._connected:
            return Response([], is_error=True)

        try:
            # Luxtronik request calculations (CMD 3004)
            # This returns the block of "Calculations" which contains most temperatures/statuses
            # Ideally we would cache this for the duration of a "read_all" cycle,
            # but for this adapter we fetch fresh.

            # Send CMD 3004 (Read Calculations)
            # Protocol: [3004][0] (4-byte integers big-endian)
            req = struct.pack(">II", 3004, 0)
            self.socket.sendall(req)

            # Read CMD echo
            cmd_echo_raw = self._recv_exact(4)
            cmd_echo = struct.unpack(">I", cmd_echo_raw)[0]
            if cmd_echo != 3004:
                logger.error(f"Luxtronik protocol error: Expected 3004, got {cmd_echo}")
                return Response([], is_error=True)

            # Read status
            stat_raw = self._recv_exact(4)
            # stat = struct.unpack(">I", stat_raw)[0]

            # Read count
            count_raw = self._recv_exact(4)
            num_values = struct.unpack(">I", count_raw)[0]

            # Read all values (4 bytes each)
            payload_size = num_values * 4
            payload_raw = self._recv_exact(payload_size)

            values = []
            for i in range(num_values):
                val = struct.unpack(">i", payload_raw[i * 4 : (i + 1) * 4])[0]
                values.append(val)

            # Map requested 'address' to our values array.
            # address is the index in the returned array.
            if address + count <= len(values):
                result = values[address : address + count]
                return Response(result)
            else:
                logger.warning(
                    f"Luxtronik read out of bounds: {address}+{count} > {len(values)}"
                )
                return Response([], is_error=True)

        except Exception as e:
            logger.error(f"Luxtronik read error: {e}")
            self.close()
            return Response([], is_error=True)

    def write_registers(self, address: int, values: List[int], **kwargs) -> Any:
        """
        Mimic Modbus write_registers.
        Not implemented for now - Luxtronik write requires different commands (3002).
        """
        class Response:
            def __init__(self, is_error=False):
                self._is_error = is_error

            def isError(self):
                return self._is_error

        logger.warning("Luxtronik write not yet implemented")
        return Response(is_error=True)

    def _recv_exact(self, size: int) -> bytes:
        """Receive exact number of bytes."""
        data = b""
        while len(data) < size:
            chunk = self.socket.recv(size - len(data))
            if not chunk:
                raise ConnectionError("Socket connection broken")
            data += chunk
        return data


@ManufacturerRegistry.register
class Luxtronik21Driver(HeatpumpDriver):
    """
    Luxtronik 2.1 Controller - used by:
    - Bosch
    - Alpha Innotec
    - Novelan
    - Siemens Novelan
    """

    MANUFACTURER = "luxtronik"
    MODEL = "luxtronik_2_1"
    DISPLAY_NAME = "Luxtronik 2.1 (Bosch, Alpha Innotec)"
    PROTOCOL = "Luxtronik TCP"
    DEFAULT_PORT = 8889

    # Mapping of logical sensor IDs to array indices in the "Calculations" block (CMD 3004)
    # Based on Luxtronik 2.0/2.1 documentation
    PARAMETERS = {
        "temp_outside": {
            "index": 15,
            "type": "temperature",
            "category": SensorCategory.TEMPERATURE,
            "name": "Außentemperatur",
        },
        "temp_outside_avg": {
            "index": 16,
            "type": "temperature",
            "category": SensorCategory.TEMPERATURE,
            "name": "Außentemperatur Mittel",
        },
        "temp_hot_water": {
            "index": 17,
            "type": "temperature",
            "category": SensorCategory.TEMPERATURE,
            "name": "Warmwasser Ist",
        },
        "temp_hot_water_target": {
            "index": 18,
            "type": "temperature",
            "category": SensorCategory.CONTROL,
            "name": "Warmwasser Soll",
        },
        "temp_source_in": {
            "index": 19,
            "type": "temperature",
            "category": SensorCategory.TEMPERATURE,
            "name": "Wärmequelle Ein",
        },
        "temp_source_out": {
            "index": 20,
            "type": "temperature",
            "category": SensorCategory.TEMPERATURE,
            "name": "Wärmequelle Aus",
        },
        "temp_flow": {
            "index": 10,
            "type": "temperature",
            "category": SensorCategory.TEMPERATURE,
            "name": "Vorlauf",
        },
        "temp_return": {
            "index": 11,
            "type": "temperature",
            "category": SensorCategory.TEMPERATURE,
            "name": "Rücklauf",
        },
        "heat_quantity_heating": {
            "index": 151,
            "type": "energy",
            "category": SensorCategory.ENERGY,
            "name": "Wärmemenge Heizen",
        },
        "heat_quantity_hot_water": {
            "index": 152,
            "type": "energy",
            "category": SensorCategory.ENERGY,
            "name": "Wärmemenge WW",
        },
        "error_code": {
            "index": 99,
            "type": "status",
            "category": SensorCategory.STATUS,
            "name": "Fehlercode",
        },
    }

    def get_sensors(self, config: Dict[str, Any]) -> List[SensorDefinition]:
        sensors = []
        for sensor_id, info in self.PARAMETERS.items():
            sensors.append(
                SensorDefinition(
                    id=sensor_id,
                    name=info["name"],
                    name_de=info["name"],
                    category=info["category"],
                    unit="°C"
                    if info["type"] == "temperature"
                    else ("kWh" if info["type"] == "energy" else ""),
                    address=info["index"],
                    datatype=DataType.INT32,  # Adapter returns native python ints, treated as INT32 registers effectively
                    access=AccessMode.READ_ONLY,
                    scale=0.1 if info["type"] == "temperature" else 1.0,
                )
            )
        return sensors

    def get_capabilities(self) -> HeatpumpCapabilities:
        return HeatpumpCapabilities(
            heating=True,
            cooling=True,
            hot_water=True,
            solar_integration=True,
            smart_grid=False,
            max_circuits=2,
            max_zones=2,
        )

    def requires_custom_client(self) -> bool:
        return True

    def create_client(self, config: Dict[str, Any]) -> Any:
        host = config.get("host")
        port = config.get("port", self.DEFAULT_PORT)
        return LuxtronikClientAdapter(host, port)

    def parse_value(self, sensor: SensorDefinition, raw_registers: List[int]) -> Any:
        # The adapter returns the raw integer value directly in the list
        if not raw_registers:
            return None
        val = raw_registers[0]
        return val * sensor.scale

    def get_dashboard_template(self) -> Dict[str, Any]:
        return {
            "name": "Luxtronik Dashboard",
            "charts": [
                {
                    "title": "Temperaturen",
                    "type": "line",
                    "queries": [
                        {"label": "Außen", "query": "temp_outside", "color": "#3b82f6"},
                        {
                            "label": "Vorlauf",
                            "query": "temp_flow",
                            "color": "#ef4444",
                        },
                        {
                            "label": "Rücklauf",
                            "query": "temp_return",
                            "color": "#10b981",
                        },
                        {
                            "label": "Warmwasser",
                            "query": "temp_hot_water",
                            "color": "#f59e0b",
                        },
                    ],
                    "hours": 24,
                },
                {
                    "title": "Energie",
                    "type": "line",
                    "queries": [
                        {"label": "Heizen (kWh)", "metric": "heat_quantity_heating"},
                        {"label": "WW (kWh)", "metric": "heat_quantity_hot_water"},
                    ],
                    "hours": 24,
                },
            ],
        }

    def get_setup_instructions(self) -> str:
        return """
        **Luxtronik 2.1 Setup**

        1.  Verbinden Sie die Wärmepumpe mit dem Netzwerk.
        2.  Stellen Sie sicher, dass Port 8889 erreichbar ist.
        3.  Konfigurieren Sie die IP-Adresse in den Einstellungen.

        *Unterstützte Geräte:*
        - Alpha Innotec (Luxtronik 2.0 / 2.1)
        - Bosch / Junkers (mit entsprechendem Modul)
        - Novelan
        - Roth
        """
