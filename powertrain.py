class Powertrain:
    def __init__(self, battery, motor, propeller):
        self.battery = battery
        self.motor = motor
        self.propeller = propeller
        self.capacity_history = [battery.capacity()]
        self.runtime = None
        self.net_thrust = None  # Initialize net_thrust attribute

    def simulate(self, time_step=1):
        """Simulate the powertrain operation over time and calculate net thrust."""
        self.runtime = self.battery.runtime(self.motor)
        time = 0

        while time < self.runtime:
            time += time_step
            remaining_capacity = self.capacity_history[-1] - self.motor.motor_power * time_step
            self.capacity_history.append(remaining_capacity)

        # Calculate and store net thrust at the end of the simulation
        static_thrust = self.propeller.static_thrust(self.motor)
        self.net_thrust = static_thrust - self.battery.mass * 9.81

    def get_time_history(self):
        """Return the time history of the simulation."""
        return [i for i in range(len(self.capacity_history))]
