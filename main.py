# main.py
import matplotlib.pyplot as plt

from lithium_ion_battery import LithiumIonBattery
from inverter import Inverter
from esc import ESC
from electric_motor import ElectricMotor
from ducted_propeller import DuctedPropeller
from powertrain import Powertrain

def main():
    # Battery Inputs
    battery_mass = 10  # kg
    specific_energy = 200  # Wh/kg

    # Motor Inputs
    motor_power = 20000  # W

    # Propeller Inputs
    propeller_diameter = .4 # m
    hub_diameter = 0.1 # m
    diffuser_expansion_ratio = 0.9

    motor = ElectricMotor(motor_power=motor_power, rpm=12000)
    battery = LithiumIonBattery(mass=battery_mass, specific_energy=specific_energy)
    propeller = DuctedPropeller(propeller_diameter=propeller_diameter, hub_diameter=hub_diameter,diffuser_expansion_ratio=diffuser_expansion_ratio, air_density=1.225, correction_factor=0.95)

    # Create a Powertrain object and simulate its operation
    train = Powertrain(battery, motor, propeller)
    train.simulate(time_step=0.05)
  #  print(f"Thrust runtime: {battery.runtime(motor)*60} min")
   # print(f"Total runtime: {train.runtime} hours")

    # Get data for plotting
    times = train.get_time_history()
    capacities = train.capacity_history

    thrust = propeller.static_thrust(motor)
    print(f"Static Thrust: {thrust/9.91} kgf")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(times, capacities, '-o', label='Battery Capacity')
    plt.title('Battery Capacity vs Time')
    plt.xlabel('Time (hours)')
    plt.ylabel('Battery Capacity (Wh)')
    plt.legend()
    plt.grid(True)
    
    
    # Return data for report
    return {
        'motor': motor,
        'battery': battery,
        'propeller': propeller,
        'train': train
    }

if __name__ == "__main__":
    main()
    plt.show()
    