from simulation.energy_model import calculate_energy
from simulation.carbon_model import calculate_carbon_emission

def test_simulation():

    cpu = 8
    utilization = 0.65

    energy = calculate_energy(cpu, utilization)
    carbon = calculate_carbon_emission(energy, region="india")

    print("Energy (kWh):", energy)
    print("Carbon (kg CO2):", carbon)


if __name__ == "__main__":
    test_simulation()
