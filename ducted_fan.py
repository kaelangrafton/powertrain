import numpy as np
from powertrain_components import Propulsor

class DuctedFan(Propulsor):
    """
    A simple ducted fan model.

    This model uses basic momentum theory to calculate thrust and power required.
    More complex models could include blade element theory and compressibility effects.

    Attributes:
        diameter (float): Fan diameter in meters.
        max_rpm (float): Maximum fan speed in RPM.
        thrust_coefficient (float): Thrust coefficient of the fan.
        power_coefficient (float): Power coefficient of the fan.
        current_rpm (float): Current fan speed in RPM.
    """

    def __init__(self, fan_config):
        """
        Initialize the ducted fan with the given configuration.

        Args:
            fan_config (dict): Configuration parameters for the fan.
        """
        self.fan_config = fan_config
        self.initialize()

    def initialize(self):
        """Initialize fan parameters based on the configuration."""
        self.diameter = self.fan_config['diameter']
        self.max_rpm = self.fan_config['max_rpm']
        self.thrust_coefficient = self.fan_config['thrust_coefficient']
        self.power_coefficient = self.fan_config['power_coefficient']
        self.current_rpm = 0

    def update(self, t, rpm_demand):
        """
        Update the fan state based on the RPM demand.

        Args:
            t (float): Time step in seconds (not used in this simple model).
            rpm_demand (float): Demanded fan speed in RPM.
        """
        self.current_rpm = min(rpm_demand, self.max_rpm)

    def get_output(self):
        """
        Get the current thrust and power required by the fan.

        Returns:
            tuple: (thrust, power_required)
        """
        return self.get_thrust(), self.get_power_required()

    def get_thrust(self):
        """
        Calculate the current thrust output of the fan.

        This uses a simplified momentum theory approach.

        Returns:
            float: Current thrust in Newtons.
        """
        rho = 1.225  # Air density at sea level (kg/m^3)
        A = np.pi * (self.diameter / 2) ** 2
        n = self.current_rpm / 60  # Convert RPM to RPS
        return self.thrust_coefficient * rho * n**2 * self.diameter**4

    def get_power_required(self):
        """
        Calculate the current power required by the fan.

        This uses a simplified momentum theory approach.

        Returns:
            float: Current power required in Watts.
        """
        rho = 1.225  # Air density at sea level (kg/m^3)
        A = np.pi * (self.diameter / 2) ** 2
        n = self.current_rpm / 60  # Convert RPM to RPS
        return self.power_coefficient * rho * n**3 * self.diameter**5

    def get_state(self):
        """
        Get the current state of the ducted fan.

        Returns:
            dict: Current state including RPM, thrust, and power required.
        """
        return {
            'rpm': self.current_rpm,
            'thrust': self.get_thrust(),
            'power_required': self.get_power_required()
        }