"""
Carbon Emission Model
---------------------
Responsible for converting energy usage (kWh)
into carbon emissions (kg CO2).
"""

from simulation.constants import (
    CARBON_INTENSITY_GLOBAL,
    CARBON_INTENSITY_BY_REGION
)


def get_carbon_intensity(region: str = "default") -> float:
    """
    Get carbon intensity based on region.

    Args:
        region (str): Cloud region

    Returns:
        float: Carbon intensity value
    """
    return CARBON_INTENSITY_BY_REGION.get(region.lower(),
                                          CARBON_INTENSITY_GLOBAL)


def calculate_carbon_emission(energy_kwh: float,
                              region: str = "default") -> float:
    """
    Convert energy consumption to carbon emissions.

    Formula:
    CO2 = Energy × Carbon_Intensity

    Args:
        energy_kwh (float): Energy in kWh
        region (str): Deployment region

    Returns:
        float: Carbon emissions in kg
    """

    if energy_kwh < 0:
        raise ValueError("Energy cannot be negative.")

    carbon_intensity = get_carbon_intensity(region)

    carbon_emission = energy_kwh * carbon_intensity

    return round(carbon_emission, 4)
