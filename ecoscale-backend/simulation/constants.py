"""
Constants used across energy and carbon models.
Modify these if needed to simulate different environments.
"""

# Power consumption assumptions
POWER_PER_CPU_CORE_KWH = 0.065   # kWh per core per hour (avg estimate)
DEFAULT_HOURS = 24               # Daily simulation

# Carbon intensity (kg CO2 per kWh)
CARBON_INTENSITY_GLOBAL = 0.475

CARBON_INTENSITY_BY_REGION = {
    "us": 0.4,
    "india": 0.7,
    "europe": 0.25,
    "default": 0.475
}
