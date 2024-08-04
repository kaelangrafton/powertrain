import numpy as np

class SerialHybridPowertrain:
    """
    A serial hybrid powertrain model for a VTOL aircraft.

    This model integrates a battery, electric motor, and ducted fan to simulate
    the powertrain of a serial hybrid electric VTOL aircraft.

    Attributes:
        battery (Battery): The battery model.
        motor (ElectricMotor): The electric motor model.
        fan (DuctedFan): The ducted fan model.
    """

    def __init__(self, battery, motor, fan):
        """
        Initialize the serial hybrid powertrain with the given components.

        Args:
            battery (Battery): The battery model.
            motor (ElectricMotor): The electric motor model.
            fan (DuctedFan): The ducted fan model.
        """
        self.battery = battery
        self.motor = motor
        self.fan = fan

    def update(self, t, thrust_demand):
        """
        Update the powertrain state based on the thrust demand.

        This method simulates the power flow from the battery through the motor to the fan,
        updating each component's state along the way.

        Args:
            t (float): Time step in seconds.
            thrust_demand (float): Demanded thrust in Newtons.
        """
         # Calculate required fan RPM for demanded thrust
        required_rpm = self.calculate_required_rpm(thrust_demand)
        
        # Update fan
        self.fan.update(t, required_rpm)
        
        # Calculate power required by the fan
        power_required = self.fan.get_power_required()
        
        # Update motor
        self.motor.update(t, power_required)
        
        # Calculate current draw from the battery
        motor_input_power = self.motor.get_power_output() / self.motor.get_efficiency()
        battery_voltage, _ = self.battery.get_output()
        battery_current = motor_input_power / battery_voltage if battery_voltage > 0 else 0
        
        # Update battery
        self.battery.update(t, battery_current)
        
        # Update battery
        self.battery.update(t, battery_current)

    def calculate_required_rpm(self, thrust_demand):
        """
        Calculate the fan RPM required to produce the demanded thrust.

        This is a simplified calculation and assumes a quadratic relationship
        between RPM and thrust. In reality, this relationship would be more complex.

        Args:
            thrust_demand (float): Demanded thrust in Newtons.

        Returns:
            float: Required fan RPM.
        """
        # Simplified calculation - adjust as needed
        max_thrust = self.fan.thrust_coefficient * 1.225 * (self.fan.max_rpm/60)**2 * self.fan.diameter**4
        return min(max(0, (thrust_demand / max_thrust)**0.5 * self.fan.max_rpm), self.fan.max_rpm)

    def get_state(self):
        """
        Get the current state of the entire powertrain.

        Returns:
            dict: Current state of all powertrain components.
        """
        return {
            'battery': self.battery.get_state(),
            'motor': self.motor.get_state(),
            'fan': self.fan.get_state()
        }

    def simulate(self, time_array, thrust_profile):
        """
        Simulate the powertrain over a given time period and thrust profile.

        Args:
            time_array (np.array): Array of time points for the simulation.
            thrust_profile (np.array): Array of thrust demands corresponding to the time points.

        Returns:
            list: List of powertrain states at each time point.
        """
        states = [self.get_state()]  # Include initial state
        for i in range(1, len(time_array)):
            t = time_array[i] - time_array[i-1]
            self.update(t, thrust_profile[i])
            states.append(self.get_state())
        return states