import numpy as np
import matplotlib.pyplot as plt
from battery import Battery
from electric_motor import ElectricMotor
from ducted_fan import DuctedFan
from serial_hybrid_powertrain import SerialHybridPowertrain

def plot_results(time, states):
    """
    Plot the simulation results.

    Args:
        time (np.array): Array of time points.
        states (list): List of powertrain states at each time point.
    """
    fig, axs = plt.subplots(3, 2, figsize=(10, 10))
    
    # Battery plots
    axs[0, 0].plot(time/60, [s['battery']['voltage'] for s in states])
    axs[0, 0].set_ylabel('Battery Voltage (V)')
    axs[0, 1].plot(time/60, [s['battery']['current'] for s in states])
    axs[0, 1].set_ylabel('Battery Current (A)')
    
    # Motor plots
    axs[1, 0].plot(time/60, [s['motor']['power_output'] for s in states])
    axs[1, 0].set_ylabel('Motor Power (W)')
    axs[1, 1].plot(time/60, [s['motor']['efficiency'] for s in states])
    axs[1, 1].set_ylabel('Motor Efficiency')
    
    # Fan plots
    axs[2, 0].plot(time/60, [s['fan']['rpm'] for s in states])
    axs[2, 0].set_ylabel('Fan RPM')
    axs[2, 1].plot(time/60, [s['fan']['thrust'] for s in states])
    axs[2, 1].set_ylabel('Fan Thrust (N)')
    
    for ax in axs.flat:
        ax.set_xlabel('Time (min)')
        
    plt.tight_layout()
    plt.show()

def main():
    # Battery configuration
    cell_config = {
        'Q': 4.2,  # Ah
        'Vcharge': 4.2,  # V
        'Vcutoff': 2.5,  # V
        'Irated': 4.2,  # A
        'Vlin0': 4.1132,
        'K': -0.7593,
        'A': 0.1061,
        'B': 150,
        'C': 0.3329,
        'D': -0.0373,
        'E': -0.06,
        'F': 25.1328,
        'G': 0,
        'H': 14.9159,
        'R0': 0.0158,
        'Rslope': -0.0053,
        'RA': 0.0800,
        'RB': 47.6190
    }

    # Motor configuration
    motor_config = {
        'max_power': 100000,  # 100 kW
        'efficiency': 0.95,
    }

    # Fan configuration
    fan_config = {
        'diameter': 1.0,  # m
        'max_rpm': 5000,
        'thrust_coefficient': 0.08,
        'power_coefficient': 0.05,
    }

    # Create powertrain components
    battery = Battery(cell_config, num_cells_series=100, num_cells_parallel=10)
    motor = ElectricMotor(motor_config)
    fan = DuctedFan(fan_config)

    # Create powertrain
    powertrain = SerialHybridPowertrain(battery, motor, fan)

    # Simulate a simple mission
    t_end = 600  # 10 minutes
    dt = 1  # 1 second time step
    time = np.arange(0, t_end + dt, dt)
    
    # Adjust thrust profile to be more realistic
    max_thrust = fan.thrust_coefficient * 1.225 * (fan.max_rpm/60)**2 * fan.diameter**4
    thrust_profile = (np.sin(time / 60) * 0.4 + 0.6) * max_thrust  # Varying between 20% and 100% of max thrust

    # Run simulation
    states = powertrain.simulate(time, thrust_profile)

    # Plot results
    plot_results(time, states)

if __name__ == "__main__":
    main()
