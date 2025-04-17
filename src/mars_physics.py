"""
MarsIrrigationPhysics — fast‑forward sol (24.65 h) into 20 min
Registers (same as OpenPLC):
    0 Soil‑moisture (0‑1000)
    1 Temperature  (°C)
    2 Humidity     (%)
    3 Water‑flow   (0‑1000)
    4 Pressure     (kPa)
Coils written by PLC remain unchanged.
"""

import math, random, time
from ics_sim.Device import HIL
from Configs import Connection           # reuse Connection.CONNECTION from your wrapper
from Configs import TAG                  # TAG constants reused below

ACCEL = 88740 / 1200         # 1 real sec = 73.95 simulated seconds

class MarsIrrigationPhysics(HIL):
    def __init__(self):
        super().__init__("MarsPhysics", Connection.CONNECTION, loop=100)  # 10 Hz
        self._start = time.time()
        self._soil   = 500

    # -----------------------------------------------------------------
    def _logic(self):
        sim_now = (time.time() - self._start) * ACCEL      # seconds in sol
        sol_hour = (sim_now / 3600.0) % 24.65

        # Temperature sinusoid
        temp = 25 + 15 * math.sin((2*math.pi / 24.65)*(sol_hour - 6)) + random.uniform(-2,2)
        self._set(TAG.TAG_TEMPERATURE, temp)

        # Humidity cosine
        hum  = 50 + 30 * math.cos((2*math.pi / 24.65)*(sol_hour - 6)) + random.uniform(-5,5)
        hum  = max(0, min(100, hum))
        self._set(TAG.TAG_HUMIDITY, hum)

        # Pump/valve status from PLC
        pump  = self._get(TAG.TAG_PUMP_CONTROL)
        valve = self._get(TAG.TAG_VALVE_CONTROL)

        # Soil moisture dynamics
        evap = 0.02 * self._loop     # per loop real‑ms
        irrig= 0.10 * self._loop     # per loop if pump+valve
        self._soil -= evap
        if pump and valve: self._soil += irrig
        self._soil = max(0, min(1000, self._soil))
        self._set(TAG.TAG_SOIL_MOISTURE, self._soil)

        # Water‑flow
        flow = random.uniform(550,650) if pump and valve else random.uniform(0,5)
        self._set(TAG.TAG_WATER_FLOW, flow)

        # Pressure mild fluctuation
        pres = 80 + 30 * math.sin((2*math.pi / 24.65)*sol_hour) + random.uniform(-5,5)
        pres = max(40, min(160, pres))
        self._set(TAG.TAG_PRESSURE, pres)
