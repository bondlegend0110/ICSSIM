"""
ICSSIM wrapper that talks to the already‑running OpenPLC (Modbus/TCP on port 502)
and exposes the same 5 holding registers + 2 coils used by your Mars irrigation demo.

Container entrypoint:  python plc_openplc.py
"""

import logging
from ics_sim.Device import PLC, SensorConnector, ActuatorConnector
from ics_sim.configs import SpeedConfig

# ---------- 1.  Tag definitions ------------------------------------------------
#   id = word index  (ICSSIM converts id -> holding‑register address automatically)
TAG_SOIL_MOISTURE      = "soil_moisture"
TAG_TEMPERATURE        = "temperature"
TAG_HUMIDITY           = "humidity"
TAG_WATER_FLOW         = "water_flow"
TAG_PRESSURE           = "pressure"

TAG_PUMP_CONTROL       = "pump_control"
TAG_VALVE_CONTROL      = "valve_control"

TAG_LIST = {
    TAG_SOIL_MOISTURE : { "id": 0, "type": "input",  "plc": 10, "fault": 0.0 },
    TAG_TEMPERATURE   : { "id": 1, "type": "input",  "plc": 10, "fault": 0.0 },
    TAG_HUMIDITY      : { "id": 2, "type": "input",  "plc": 10, "fault": 0.0 },
    TAG_WATER_FLOW    : { "id": 3, "type": "input",  "plc": 10, "fault": 0.0 },
    TAG_PRESSURE      : { "id": 4, "type": "input",  "plc": 10, "fault": 0.0 },

    TAG_PUMP_CONTROL  : { "id": 0, "type": "output", "plc": 10, "fault": 0.0 },
    TAG_VALVE_CONTROL : { "id": 1, "type": "output", "plc": 10, "fault": 0.0 },
}

# --------- 2.  Controller / connection map -------------------------------------
Controllers = {
    "PLCs": {
        10: {               # logical PLC id inside ICSSIM
            "name":  "OpenPLC‑Irrigation",
            "ip":    "openplc",   # hostname from docker‑compose
            "port":  502,
            "protocol": "ModbusWriteRequest-TCP",
        }
    }
}

# ICSSIM “connection” that tells SensorConnector / ActuatorConnector
# to talk to real hardware via Modbus (type=hardware).
Connection = {
    "CONNECTION": {
        "name":  "openplc_mem",
        "type":  "hardware",
        "path":  "openplc:502"      # <host>:<port>
    }
}

# ---------- 3.  Wrapper class --------------------------------------------------
class PLCOpenPLC(PLC):
    def __init__(self):
        sensor_connector   = SensorConnector(Connection["CONNECTION"])
        actuator_connector = ActuatorConnector(Connection["CONNECTION"])
        super().__init__(10,                   # plc_id inside ICSSIM
                         sensor_connector,
                         actuator_connector,
                         TAG_LIST,
                         Controllers["PLCs"],
                         loop=SpeedConfig.DEFAULT_PLC_PERIOD_MS)

    # No control logic – this PLC is just a bridge to existing ladder logic
    def _logic(self):
        # Example: read soil moisture and log it
        sm = self._get(TAG_SOIL_MOISTURE)
        self.report(f"Soil moisture from OpenPLC: {sm}", logging.DEBUG)

if __name__ == "__main__":
    plc = PLCOpenPLC()
    plc.set_record_variables(True)
    plc.start()
