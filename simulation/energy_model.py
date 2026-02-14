"""
Energy Consumption Model
------------------------
Responsible for estimating energy usage (kWh)
based on CPU allocation and predicted utilization.
"""

from simulation.constants import POWER_PER_CPU_CORE_KWH, DEFAULT_HOURS


def calculate_energy(cpu_cores: int,
                     utilization: float,
                     hours: int = DEFAULT_HOURS) -> float:
    """
    Calculate total energy consumption in kWh.

    Formula:
    Energy = CPU × Utilization × Power_per_core × Hours

    Args:
        cpu_cores (int): Number of CPU cores allocated
        utilization (float): Predicted utilization (0–1)
        hours (int): Simulation time in hours

    Returns:
        float: Total energy consumption in kWh
    """

    if cpu_cores <= 0:
        raise ValueError("CPU cores must be positive.")

    if not (0 <= utilization <= 1):
        raise ValueError("Utilization must be between 0 and 1.")

    energy_kwh = cpu_cores * utilization * POWER_PER_CPU_CORE_KWH * hours

    return round(energy_kwh, 4)
