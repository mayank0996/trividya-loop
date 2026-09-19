"""
Trividya-Loop engineering baseline parameters - VERSION 1.0 (2026-09-19)
All values are ASSUMPTIONS unless marked [MEASURE] (requires Mayank's hardware data).
Every simulated result derived from this file is a MODEL OUTPUT, not physical test data.
"""
import json

P = {
  "version": "1.0",
  "date": "2026-09-19",
  "status": "ASSUMED BASELINE - no measured hardware values yet",
  # Route
  "route_length_km":      {"nom": 1450.0, "lo": 1150.0, "hi": 1450.0, "unit": "km",
    "note": "1450 km inherited from project deck; Delhi-Mumbai great-circle ~1150 km [MEASURE/ALIGN]"},
  # Pod (single-patient medical pod; built mockup dimensions unknown)
  "pod_mass_kg":          {"nom": 750.0, "lo": 400.0, "hi": 1500.0, "unit": "kg", "note": "loaded mass [MEASURE]"},
  "pod_length_m":         {"nom": 3.5, "unit": "m", "note": "[MEASURE from mockup]"},
  "pod_diameter_m":       {"nom": 1.30, "unit": "m", "note": "[MEASURE from mockup]"},
  "pod_frontal_area_m2":  {"nom": 1.327, "unit": "m2", "note": "pi*(d/2)^2"},
  "pod_surface_area_m2":  {"nom": 15.0, "lo": 10.0, "hi": 20.0, "unit": "m2", "note": "cylinder+nose estimate"},
  # Tube
  "tube_inner_diameter_m":{"nom": 4.0, "lo": 3.0, "hi": 5.0, "unit": "m"},
  "tube_pressure_Pa":     {"nom": 100.0, "lo": 10.0, "hi": 1000.0, "unit": "Pa", "note": "~1/1000 atm nominal"},
  "tube_temperature_K":   {"nom": 300.0, "unit": "K"},
  # Aerodynamics
  "drag_coefficient":     {"nom": 0.3, "lo": 0.2, "hi": 1.0, "unit": "-", "note": "streamlined body, continuum flow"},
  "gas_constant_J_kgK":   {"nom": 287.0, "unit": "J/(kg K)"},
  # Motion limits (patient comfort baseline)
  "accel_max_m_s2":       {"nom": 1.0, "lo": 0.5, "hi": 2.0, "unit": "m/s2", "note": "~0.1 g nominal"},
  "jerk_max_m_s3":        {"nom": 0.5, "lo": 0.25, "hi": 1.0, "unit": "m/s3"},
  "emergency_decel_m_s2": {"nom": 3.0, "lo": 2.0, "hi": 5.0, "unit": "m/s2", "note": "~0.3 g"},
  "cruise_speed_kmh":     {"nom": 1165.0, "lo": 200.0, "hi": 1165.0, "unit": "km/h",
    "note": "1165 inherited from deck; 200 = demonstrator target; 600 = interim"},
  # Powertrain
  "motor_efficiency":     {"nom": 0.90, "lo": 0.85, "hi": 0.95, "unit": "-", "note": "LSM + inverter"},
  "regen_recovery":       {"nom": 0.60, "lo": 0.40, "hi": 0.70, "unit": "-"},
  "levitation_power_kW_per_t": {"nom": 1.0, "lo": 0.5, "hi": 3.0, "unit": "kW/t",
    "note": "EMS-class specific levitation+guidance power assumption"},
  "aux_load_kW":          {"nom": 1.0, "lo": 0.5, "hi": 2.5, "unit": "kW",
    "note": "medical devices 0.3 + life support 0.5 + comms 0.1 + misc 0.1"},
  # Thermal
  "pod_emissivity":       {"nom": 0.85, "unit": "-"},
  "pod_skin_max_C":       {"nom": 40.0, "unit": "degC", "note": "touch-safe / electronics-friendly"},
  # Operations
  "headway_margin_s":     {"nom": 20.0, "unit": "s"},
  # Medical data workflow
  "ecg_bitrate_kbps":     {"nom": 96.0, "unit": "kbps", "note": "12-lead, 500 Hz, 16 bit"},
  "video_bitrate_Mbps":   {"nom": 4.0, "unit": "Mbps", "note": "2x 1080p H.264"},
  "other_telemetry_kbps": {"nom": 50.0, "unit": "kbps", "note": "SpO2, NIBP, capno, pod state"},
}
if __name__ == "__main__":
    print(json.dumps(P, indent=1))
