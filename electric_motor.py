from powertrain_components import PowerConverter

class ElectricMotor(PowerConverter):
    """
    A simple electric motor model.

    This model assumes a constant efficiency and a maximum power output.
    More complex models could include efficiency maps and thermal effects.

    Attributes:
        max_power (float): Maximum power output in Watts.
        efficiency (float): Motor efficiency as a value between 0 and 1.
        current_power (float): Current power output in Watts.
    """

    def __init__(self, motor_config):
        """
        Initialize the electric motor with the given configuration.

        Args:
            motor_config (dict): Configuration parameters for the motor.
        """
        self.motor_config = motor_config
        self.initialize()

    def initialize(self):
        """Initialize motor parameters based on the configuration."""
        self.max_power = self.motor_config['max_power']
        self.efficiency = self.motor_config['efficiency']
        self.current_power = 0

    def update(self, t, power_demand):
        """
        Update the motor state based on the power demand.

        Args:
            t (float): Time step in seconds (not used in this simple model).
            power_demand (float): Demanded power output in Watts.
        """
        self.current_power = min(power_demand, self.max_power)

    def get_output(self):
        """
        Get the current power output of the motor.

        Returns:
            float: Current power output in Watts.
        """
        return self.current_power * self.efficiency

    def get_efficiency(self):
        """
        Get the current efficiency of the motor.

        Returns:
            float: Motor efficiency as a value between 0 and 1.
        """
        return self.efficiency

    def get_power_output(self):
        """
        Get the current power output of the motor.

        Returns:
            float: Current power output in Watts.
        """
        return self.current_power * self.efficiency

    def get_state(self):
        """
        Get the current state of the motor.

        Returns:
            dict: Current state including power output and efficiency.
        """
        return {
            'power_output': self.get_power_output(),
            'efficiency': self.get_efficiency(),
            'power_demand': self.current_power
        }